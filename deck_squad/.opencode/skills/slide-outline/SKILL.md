---
name: slide-outline
description: Turn a presentation brief into a storyline outline — one takeaway, a hook, one message per slide, and a closing call to action. Use before any slides are written.
license: MIT
compatibility: opencode
metadata:
  squad: deck-squad
  used-by: deck-director
---

# slide-outline

## What I do

Turn a brief (topic, audience, time, goal) into a slide-by-slide storyline.

## When to use me

- Starting a new deck from a brief.
- Restructuring a deck whose flow does not work.

Do **NOT** use me to write slide text — that is `marp-slides`.

## Steps

1. Write the **takeaway**: the one sentence the audience should remember.
2. Pick the **slide count**: about 1 slide per minute, never more than 12.
3. Use this arc:
   1. Title
   2. Hook — the problem or question
   3. Context — what the audience needs to know first
   4. Core slides — one idea each (most of the deck)
   5. Demo or example (if the brief has one)
   6. Recap — 3 points max
   7. Call to action / Q&A
4. Give every slide a **headline that is a full sentence** stating its message
   ("Subagents keep the main context small"), not a label ("Subagents").

## Output format

```
Title: <deck title>
Audience: <who> | Time: <minutes> | Takeaway: <one sentence>

1. <headline sentence> — <what goes on the slide, 1 line>
2. ...
```
