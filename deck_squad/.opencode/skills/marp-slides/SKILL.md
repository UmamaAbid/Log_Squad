---
name: marp-slides
description: Write slide decks as Marp markdown (front matter, --- slide breaks, speaker notes in HTML comments) so they render in the Marp VS Code extension or export to PDF/PPTX with marp-cli.
license: MIT
compatibility: opencode
metadata:
  squad: deck-squad
  used-by: deck-writer
---

# marp-slides

## What I do

Define the exact file format for every deck in `decks/`.

## When to use me

- Writing a new deck file.
- Editing slides in an existing deck.

## File format

```markdown
---
marp: true
theme: default
paginate: true
title: <deck title>
---

<!-- _class: lead -->
# <Deck title>
<subtitle · presenter · date>

---

## <Headline sentence from the outline>

- Bullet one
- Bullet two

<!--
Speaker notes: what to say for this slide, 2–4 sentences.
-->
```

## Rules

- Slides are separated by a line containing only `---`.
- First slide uses `<!-- _class: lead -->`.
- Headline = `##` + the outline's full-sentence headline.
- Max 6 bullets, max 12 words per bullet. Prefer a short code block or a
  2-column table over a 7th bullet.
- Code blocks: max 12 lines, tagged with a language.
- Speaker notes go in an HTML comment at the end of the slide.
- No raw HTML other than comments. No external images unless the brief gives a URL.

## Presenting

- VS Code: install "Marp for VS Code", open the file, click preview.
- CLI: `npx @marp-team/marp-cli decks/<file>.md --pdf` (or `--pptx`).
