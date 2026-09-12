import re


def run(log_text: str, pattern: str) -> str:
    if not log_text:
        return "Count: 0 — log text is empty."
    if not pattern:
        return "Error: pattern is required"
    try:
        expr = re.compile(re.escape(pattern), re.IGNORECASE)
    except re.error as e:
        return f"Error: invalid pattern: {e}"
    matches = []
    lines = log_text.splitlines()
    for i, line in enumerate(lines, 1):
        if expr.search(line):
            matches.append(i)
    return (
        f"Count: {len(matches)} case-insensitive occurrence(s) of {pattern!r} "
        f"across {len(lines)} lines.\n"
        f"Matching line numbers: {matches}"
    )