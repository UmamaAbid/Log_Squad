import json
import os
import sys
import time
from pathlib import Path

import yaml
from openai import OpenAI

from skills.loader import SKILLS, SKILL_SCHEMAS

BASE_DIR = Path(__file__).resolve().parent
SUBAGENTS_DIR = BASE_DIR / "subagents"
REPORT_PATH = BASE_DIR / "incident_report.md"

MODEL = "openai/gpt-oss-120b"
BASE_URL = "https://api.groq.com/openai/v1"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GEMINI_MODEL = "gemini-3.6-flash"
TEMPERATURE = 0.2

CHARS_HEAD = 4000
CHARS_TAIL = 4000
CHARS_MAX = CHARS_HEAD + CHARS_TAIL
MIN_SIGNIFICANT_LINES = 3

EMPTY_LOG_MESSAGE = "No significant log activity found — nothing to report."
FAILED_OUTPUT = "Could not complete analysis."
PIPELINE_FAILED_MESSAGE = "Pipeline failed: no subagent completed successfully."

PIPELINE = [
    ("anomaly_detector", "Anomaly Detector"),
    ("root_cause_analyzer", "Root Cause Analyzer"),
    ("severity_classifier", "Severity Classifier"),
    ("incident_writer", "Incident Writer"),
]

TOOL_AGENTS = {"anomaly_detector", "severity_classifier", "incident_writer"}
MAX_TOOL_TURNS = 4
TOOL_TURN_LIMITS = {"anomaly_detector": 8}


def agent_rel_path(path: Path) -> str:
    return f"subagents/{path.parent.name}/AGENT.md"


def parse_agent_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8").strip()
    rel = agent_rel_path(path)
    if not text.startswith("---"):
        raise ValueError(
            f"Failed to parse frontmatter in {rel} — frontmatter block is missing"
        )
    _, _, rest = text.partition("---")
    frontmatter_text, _, body = rest.partition("---")
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        raise ValueError(
            f"Failed to parse frontmatter in {rel} — check for unescaped colons "
            f"or quotes in the description field ({e})"
        ) from e
    if not isinstance(frontmatter, dict):
        raise ValueError(
            f"Failed to parse frontmatter in {rel} — expected a mapping of keys"
        )
    return {
        "name": frontmatter.get("name"),
        "description": frontmatter.get("description"),
        "persona": body.strip(),
    }


def load_subagents() -> dict:
    agents = {}
    for name, _ in PIPELINE:
        md = SUBAGENTS_DIR / name / "AGENT.md"
        if not md.exists():
            raise FileNotFoundError(f"Missing {agent_rel_path(md)}")
        agents[name] = parse_agent_md(md)
    return agents


def significant_line_count(lines: list) -> int:
    return sum(1 for line in lines if line.strip())


def cap_text(text: str, max_chars: int = 3000, head_chars: int = 1500, tail_chars: int = 1500) -> str:
    if len(text) <= max_chars:
        return text
    head = text[:head_chars]
    tail = text[-tail_chars:]
    omitted = len(text) - head_chars - tail_chars
    note = f"\n[... {omitted} characters omitted ...]\n"
    return f"{head}{note}{tail}"


def render_log(path: Path, lines: list) -> str:
    total_lines = len(lines)
    content = "\n".join(lines)
    header = f"{path.name} ({total_lines} lines, {len(content)} characters)"
    if len(content) <= CHARS_MAX:
        return f"{header}\n\n{content}"
    head = content[:CHARS_HEAD]
    tail = content[-CHARS_TAIL:]
    omitted = len(content) - CHARS_MAX
    note = f"\n[... {omitted} characters omitted ...]\n"
    return (
        f"{header} (showing first {CHARS_HEAD} and last {CHARS_TAIL} characters)\n\n"
        f"{head}{note}{tail}"
    )


def is_rate_limit_error(e: Exception) -> bool:
    return getattr(e, "status_code", None) == 429 or getattr(e, "code", "") == "rate_limit_exceeded"


def serialize_tool_calls(tool_calls) -> list:
    payload = []
    for tc in tool_calls:
        tc_dict = {"id": tc.id, "type": "function", "function": tc.function}
        extra = getattr(tc, "extra_content", None)
        if extra:
            tc_dict["extra_content"] = extra
        payload.append(tc_dict)
    return payload


def _call_gemini(messages: list, use_tools: bool):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "Groq is rate-limited but GEMINI_API_KEY is not set; cannot fall back to Gemini"
        )
    print("[Groq quota exhausted, falling back to Gemini for this call]", file=sys.stderr)
    gemini_client = OpenAI(api_key=api_key, base_url=GEMINI_BASE_URL)
    kwargs = {
        "model": GEMINI_MODEL,
        "temperature": TEMPERATURE,
        "messages": messages,
    }
    if use_tools:
        kwargs["tools"] = SKILL_SCHEMAS
    last_error = None
    for attempt in range(3):
        try:
            return gemini_client.chat.completions.create(**kwargs)
        except Exception as e:
            last_error = e
            if not is_rate_limit_error(e):
                raise
            if attempt < 2:
                time.sleep(10)
    raise last_error


def create_completion(client: OpenAI, messages: list, use_tools: bool):
    last_error = None
    kwargs = {
        "model": MODEL,
        "temperature": TEMPERATURE,
        "messages": messages,
    }
    if use_tools:
        kwargs["tools"] = SKILL_SCHEMAS
    for attempt in range(2):
        try:
            return client.chat.completions.create(**kwargs)
        except Exception as e:
            last_error = e
            if is_rate_limit_error(e):
                break
            if attempt == 0:
                time.sleep(2)

    if is_rate_limit_error(last_error):
        return _call_gemini(messages, use_tools)

    raise last_error


def call_subagent(client: OpenAI, persona: str, user_message: str, use_tools: bool, report_holder: dict, max_turns: int = MAX_TOOL_TURNS) -> str:
    report_holder["save_report_succeeded"] = False
    messages = [
        {"role": "system", "content": persona},
        {"role": "user", "content": user_message},
    ]
    for turn in range(max_turns):
        response = create_completion(client, messages, use_tools)
        message = response.choices[0].message
        if not message.tool_calls:
            return message.content

        messages.append({
            "role": "assistant",
            "content": message.content,
            "tool_calls": serialize_tool_calls(message.tool_calls),
        })
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            try:
                tool_input = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
            except json.JSONDecodeError:
                tool_input = {}
            print(f"🔧 Calling skill: {tool_name}", file=sys.stderr)
            if tool_name in SKILLS:
                try:
                    result = SKILLS[tool_name](**tool_input)
                except Exception as e:
                    result = f"Error: {e}"
            else:
                result = f"Error: Unknown tool '{tool_name}'"
            if tool_name == "save_report" and not str(result).startswith("Error"):
                report_holder["save_report_succeeded"] = True
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })
    return "Max tool turns reached without a final answer."


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python3.11 {sys.argv[0]} <logfile>")
        sys.exit(1)

    log_path = Path(sys.argv[1])
    if not log_path.exists():
        print(f"Error: log file not found: {log_path}")
        sys.exit(1)
    if log_path.is_dir():
        print(f"Error: {log_path} is a directory, please provide a log file.")
        sys.exit(1)

    lines = log_path.read_text(encoding="utf-8").splitlines()
    if significant_line_count(lines) < MIN_SIGNIFICANT_LINES:
        print(EMPTY_LOG_MESSAGE)
        REPORT_PATH.write_text(EMPTY_LOG_MESSAGE + "\n", encoding="utf-8")
        sys.exit(0)

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set")
        sys.exit(1)

    log_text = render_log(log_path, lines)

    try:
        agents = load_subagents()
    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    client = OpenAI(api_key=api_key, base_url=BASE_URL)

    outputs = {}
    failed = []
    save_report_flags = {}
    report_holder = {"save_report_succeeded": False}
    for name, label in PIPELINE:
        user_message = f"### Raw log contents\n```\n{log_text}\n```"
        if outputs:
            previous_blocks = []
            for prev_name, prev_label in PIPELINE:
                if prev_name in outputs:
                    previous_blocks.append(
                        f"===== {prev_label} ({prev_name}) =====\n{outputs[prev_name]}"
                    )
            previous_text = cap_text("\n\n".join(previous_blocks))
            user_message += "\n\n### Previous subagent outputs\n" + previous_text

        try:
            output = call_subagent(
                client,
                agents[name]["persona"],
                user_message,
                name in TOOL_AGENTS,
                report_holder,
                TOOL_TURN_LIMITS.get(name, MAX_TOOL_TURNS),
            )
        except Exception as e:
            print(f"[{label} failed after retry: {e}]")
            output = FAILED_OUTPUT
            failed.append(name)
        save_report_flags[name] = report_holder["save_report_succeeded"]
        outputs[name] = output
        print(f"[{label}]:\n{output}\n")

    writer_saved_report = save_report_flags.get("incident_writer", False)

    if len(failed) == len(PIPELINE):
        print(PIPELINE_FAILED_MESSAGE)
        if not writer_saved_report:
            REPORT_PATH.write_text(PIPELINE_FAILED_MESSAGE + "\n", encoding="utf-8")
        sys.exit(1)

    writer_output = outputs["incident_writer"]
    if writer_output != FAILED_OUTPUT:
        REPORT_PATH.write_text(writer_output.rstrip() + "\n", encoding="utf-8")
    elif not writer_saved_report:
        REPORT_PATH.write_text(FAILED_OUTPUT + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()