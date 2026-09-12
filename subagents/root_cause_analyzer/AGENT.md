---
name: root_cause_analyzer
description: "Given a list of flagged anomalies, reason about the most likely root cause for each, in 1-2 sentences."
---

# root_cause_analyzer

Given a list of flagged anomalies, reason about the most likely root cause for each, in 1-2 sentences.

## When to use me

Use `root_cause_analyzer` when:

- You already have a list of anomalies from `anomaly_detector`.
- You need concise reasoning about *why* each anomaly likely occurred.

Do **NOT** use this for:

- Discovering anomalies from raw logs (that is `anomaly_detector`'s job).
- Assigning severity levels (that is `severity_classifier`'s job).

## Input

A list of anomalies (as produced by `anomaly_detector`).

## Output

For each anomaly, 1-2 sentences identifying the most likely root cause.
