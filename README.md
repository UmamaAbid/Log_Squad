# log_squad

A multi-agent system for reading raw log files and turning them into structured
incident reports. Built **from scratch** — no frameworks, no agent SDKs: just
standard Python, the `openai` client, and a plain HTTP API.

## What this is

Four specialized subagents run one after another, each one doing a single job,
plus an orchestrator that wires them together. Each subagent's identity lives
in a plain-text persona file — no code changes needed to modify behavior.

## Architecture

`orchestrator.py` chains the subagents in sequence:

- It parses each `subagents/*/AGENT.md`: the **frontmatter** (`name`,
  `description`) plus the **body text** below it, which is used verbatim as
  that subagent's system prompt.
- It reads the log file. Logs up to 300 lines are sent whole; larger logs are
  trimmed to the **first 100 + last 100 lines** with a
  `[... N lines omitted ...]` marker in between, so errors near the end of a
  huge log are not silently dropped.
- Logs with fewer than 3 non-empty lines skip the pipeline entirely and report
  "No significant log activity found — nothing to report."
- Each subagent gets the raw logs **plus a clearly labeled section with all
  previous subagents' outputs** accumulated so far, so later agents reason on
  earlier findings.

The `AGENT.md` convention deliberately mirrors the `SKILL.md` convention from
my other project, **mini_agent**: frontmatter metadata on top, human-readable
persona/instructions below, discovered from disk.

### Pipeline flow

```
                 log file
                    |
                    v
   ┌──────────────────────────────┐
   │      anomaly_detector        │  flags anomalies with log lines
   └──────────────────────────────┘
                    |
                    v
   ┌──────────────────────────────┐
   │    root_cause_analyzer       │  explains why, in 1-2 sentences each
   └──────────────────────────────┘
                    |
                    v
   ┌──────────────────────────────┐
   │     severity_classifier      │  Critical / High / Medium / Low
   └──────────────────────────────┘
                    |
                    v
   ┌──────────────────────────────┐
   │        incident_writer       │  structured markdown report
   └──────────────────────────────┘
                    |
                    v
   incident_report.md
```

Each agent's output is streamed to the terminal as it finishes, and the final
output is written to `incident_report.md`.

## Subagents

| Subagent | Persona (in `subagents/*/AGENT.md`) |
|---|---|
| `anomaly_detector` | Scans raw log lines and flags anomalies — error spikes, repeated failures, unusual status codes or response times — listing each with the relevant log line(s). |
| `root_cause_analyzer` | Given flagged anomalies, reasons about the most likely root cause for each in 1-2 sentences. |
| `severity_classifier` | Given anomalies + root causes, assigns each a severity — Critical, High, Medium, or Low — with a one-line justification. |
| `incident_writer` | Given anomalies + root causes + severities, writes a clean structured markdown incident report. |

## Setup

```bash
pip install -r requirements.txt
export GROQ_API_KEY=your-key-here
python3.11 orchestrator.py <logfile>
```

## Notes

- Works on **any** log file, not just `sample_logs/app.log` — pass any text
  log's path as the first argument.
- All LLM calls go to **Groq** (`openai/gpt-oss-120b`) via the OpenAI-compatible
  API.
- Sample input: `sample_logs/app.log` — run
  `python3.11 orchestrator.py sample_logs/app.log` to see the pipeline end to end.