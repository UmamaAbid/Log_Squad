---
name: count_pattern
description: Count how many times a pattern (status code, error keyword, word, or phrase) appears in log text, case-insensitively, and return the count plus the matching line numbers. Use whenever a subagent needs to quantify occurrences from the log (e.g. how many "500", "503", "[ERROR]", "timeout", or "exhausted" lines) instead of estimating from memory.
---

# count_pattern

Count case-insensitive occurrences of a literal pattern in the log text and
report the 1-based line numbers where it appears.

## When to use me

Use `count_pattern` when you need facts about the log:

- "how many 500 errors are there?"
- "which lines mention `timeout`?"
- "how many `[ERROR]` entries, and on which lines?"

Do **NOT** use this for:

- Judging severity (use `severity_rubric_lookup`).
- Free-form analysis that does not need a count.

## Before you start

- Pass the whole log text as `log_text` and the exact substring to find as
  `pattern`. Matching is case-insensitive and literal (no regex).

## Steps

1. Call `count_pattern(log_text=<the raw log>, pattern=<term>)`.
2. The skill returns the count and matching line numbers.
3. Use the real numbers in your answer — never guess counts.

## Expected output

E.g. `Count: 7 case-insensitive occurrence(s) of '500' across 24 lines.
Matching line numbers: [7, 8, 9, 11, 12, 16, 21]`