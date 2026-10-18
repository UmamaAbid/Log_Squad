---
name: deck-review-checklist
description: Fixed 7-point checklist for auditing a slide deck (storyline, one message per slide, text density, speaker notes, facts, format, timing) with blocker/major/minor severities. Use when reviewing any deck.
license: MIT
compatibility: opencode
metadata:
  squad: deck-squad
  used-by: deck-reviewer
---

# deck-review-checklist

## What I do

Give the reviewer a fixed checklist so every deck is judged the same way.

## When to use me

Whenever a deck in `decks/` needs a pass/revise verdict.

## Checklist

| # | Check | Fails when | Severity |
|---|---|---|---|
| 1 | `storyline` | Slide order does not match the outline, or takeaway is missing | blocker |
| 2 | `one-message-per-slide` | Headline is a label, or a slide argues two ideas | major |
| 3 | `text-density` | More than 6 bullets or a bullet over 12 words | major |
| 4 | `speaker-notes` | A content slide has no `<!-- -->` notes | major |
| 5 | `facts` | A number/claim not in the brief, or an unresolved `TODO` | blocker |
| 6 | `format` | Missing `marp: true`, broken `---` separators, untagged code block | minor |
| 7 | `timing` | Slide count > minutes + 2 | minor |

## Mechanical checks (use grep)

- Front matter: `grep -n "marp: true" <deck>`
- Open TODOs: `grep -n "TODO" <deck>`
- Count slides: number of lines that are exactly `---`, minus the front-matter pair.

## Verdict rule

`revise` if any **blocker** or more than **2 major** findings; otherwise `pass`.
