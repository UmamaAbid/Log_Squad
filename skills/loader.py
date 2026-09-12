import importlib.util
import inspect
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

import yaml

SKILLS_DIR = Path(__file__).resolve().parent

_TYPE_MAP = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
}


def load_skill_dir(skill_dir: Path) -> Tuple[Dict[str, Any], Callable]:
    """Read SKILL.md frontmatter and dynamically import skill.py's run().

    Returns (frontmatter meta, run function) for one skill folder.
    """
    meta = _read_frontmatter(skill_dir / "SKILL.md")
    run_func = _import_run(skill_dir / "skill.py", skill_dir.name)
    return meta, run_func


def _read_frontmatter(md_path: Path) -> Dict[str, Any]:
    text = md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    _, frontmatter, _ = text.split("---", 2)
    return yaml.safe_load(frontmatter) or {}


def _import_run(py_path: Path, folder_name: str) -> Callable:
    module_name = f"_skill_{folder_name}"
    spec = importlib.util.spec_from_file_location(module_name, py_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module.run


def _build_parameters(run_func: Callable) -> Dict[str, Any]:
    """Derive an OpenAI JSON-schema `parameters` block from run()'s signature.

    Positional params without defaults are required; annotated types map to
    JSON types; everything else defaults to string.
    """
    properties: Dict[str, Any] = {}
    required: List[str] = []
    for name, param in inspect.signature(run_func).parameters.items():
        if param.kind in (param.VAR_POSITIONAL, param.VAR_KEYWORD):
            continue
        ann = param.annotation
        json_type = _TYPE_MAP.get(ann, "string")
        properties[name] = {"type": json_type}
        if param.default is inspect.Parameter.empty:
            required.append(name)
    schema: Dict[str, Any] = {"type": "object", "properties": properties}
    if required:
        schema["required"] = required
    return schema


def load_skills() -> Tuple[Dict[str, Callable], List[Dict[str, Any]]]:
    """Scan every skills/<skill>/ folder and build SKILLS and SKILL_SCHEMAS.

    A folder is only registered if it contains both SKILL.md (YAML frontmatter
    with name and description) and a skill.py exposing run(...). The tool
    parameters schema is inferred from the run() signature.
    """
    skills: Dict[str, Callable] = {}
    schemas: List[Dict[str, Any]] = []

    for child in sorted(SKILLS_DIR.iterdir()):
        if not child.is_dir():
            continue
        if not (child / "SKILL.md").exists() or not (child / "skill.py").exists():
            continue

        meta, run_func = load_skill_dir(child)
        name = meta.get("name") or child.name
        skills[name] = run_func
        schemas.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": meta.get("description", ""),
                    "parameters": _build_parameters(run_func),
                },
            }
        )

    return skills, schemas


SKILLS, SKILL_SCHEMAS = load_skills()