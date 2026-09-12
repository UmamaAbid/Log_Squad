from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


def run(content: str, filename: str) -> str:
    if not filename:
        return "Error: filename is required"
    name = Path(filename).name
    path = (BASE_DIR / name).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return f"Report saved to {path.relative_to(BASE_DIR)}."