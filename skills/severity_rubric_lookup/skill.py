RUBRIC = [
    ("exhausted", "Critical", "pool or resource exhausted/capacity maxed"),
    ("oom", "Critical", "out-of-memory condition"),
    ("memory", "Critical", "memory threshold breached"),
    ("timeout", "High", "request hit an upstream timeout"),
    ("503", "High", "service unavailable / upstream timeout"),
    ("500", "High", "internal server error"),
    ("429", "Medium", "rate limit exceeded"),
    ("rate limit", "Medium", "throttling / rate limit exceeded"),
    ("connection refused", "Medium", "exporter/connection refused"),
]

DEFAULT_SEVERITY = "Medium"
DEFAULT_REASON = "no rubric rule matched this keyword"


def run(keyword: str) -> str:
    if not keyword or not keyword.strip():
        return (
            f"Suggested severity: {DEFAULT_SEVERITY} — "
            f"default rule ({DEFAULT_REASON})."
        )
    low = keyword.strip().lower()
    for rule, severity, reason in RUBRIC:
        if rule in low:
            return (
                f"Suggested severity: {severity} — "
                f"matched rule {rule!r} ({reason})."
            )
    return (
        f"Suggested severity: {DEFAULT_SEVERITY} — "
        f"default rule ({DEFAULT_REASON})."
    )