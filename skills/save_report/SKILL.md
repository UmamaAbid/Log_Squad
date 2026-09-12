---
name: save_report
description: Write the given content to a file named filename (stored under the log_squad/ folder) and return a confirmation with the saved path. Use to persist the final markdown incident report, e.g. save_report(content=<full report>, filename="incident_report.md").
---

# save_report

Write provided content to a file under the log_squad folder and confirm.

## When to use me

Use `save_report` when the incident report is final and must be saved to disk:

- "save this report to incident_report.md"
- "persist the write-up"

Do **NOT** use this for:

- Analysis, counting, or severity decisions (use the other skills).

## Steps

1. Build the complete markdown report as a single `content` string.
2. Call `save_report(content=<report text>, filename="incident_report.md")`.
3. Report the confirmation returned.

## Expected output

E.g. `Report saved to incident_report.md.`