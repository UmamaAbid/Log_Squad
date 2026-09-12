---
name: severity_rubric_lookup
description: Look up a suggested severity for a keyword or phrase using the fixed rubric (exhausted -> Critical, oom/memory -> Critical, timeout -> High, 503/500 -> High, 429/rate limit/connection refused -> Medium, default -> Medium). Returns the suggested severity plus the rule that matched. Use when assigning severities to anomalies instead of guessing from free-form reasoning.
---

# severity_rubric_lookup

Look up an anomaly keyword in the fixed severity rubric and return the
suggested severity with the matched rule.

## When to use me

Use `severity_rubric_lookup` whenever you need a severity label:

- "what severity for a connection pool that is exhausted?"
- "what does the rubric say for a 503 timeout?"
- "severity for OOM / memory threshold?"

Do **NOT** use this for:

- Counting occurrences (use `count_pattern`).
- Deciding the final label without considering the rubric result (call it
  first, then reason from the returned rule).

## Rubric

| Rule | Severity |
|---|---|
| `exhausted`, `oom`, `memory` | **Critical** |
| `timeout`, `503`, `500` | **High** |
| `429`, `rate limit`, `connection refused` | **Medium** |
| anything else | **Medium** |

## Steps

1. Call `severity_rubric_lookup(keyword=<anomaly keyword or phrase>)`.
2. Use the returned severity + rule as the basis for your one-line
   justification.

## Expected output

E.g. `Suggested severity: High — matched rule 'timeout' (request hit an
upstream timeout).`