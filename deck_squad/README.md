# deck_squad

A multi-agent system for turning a presentation brief into a finished slide deck.
Built **natively on OpenCode** — no Python, no orchestrator script: just markdown
agent files and `SKILL.md` skills that OpenCode discovers from disk.

## What this is

Three agents — one **primary** lead and two **subagents** — each doing a single job.
The lead plans the storyline and delegates; the specialists write and review.
Each agent's identity lives in a plain markdown file — no code changes needed to
modify behavior.

This is the OpenCode-native sibling of **log_squad**: where log_squad parses
`subagents/*/AGENT.md` with its own `orchestrator.py`, deck_squad lets OpenCode do
the orchestration through its **Task tool**, **permissions** and **skill tool**.

## Architecture

- Agents live in `.opencode/agents/*.md`. The **file name is the agent name**; the
  frontmatter sets `mode`, `temperature`, `steps`, `color` and `permission`; the
  body is the system prompt.
- Skills live in `.opencode/skills/<name>/SKILL.md`. Agents only see each skill's
  `name` + `description` until they call `skill({ name })`, so skills cost no
  context until they are needed.
- `permission.task` on the director allows it to launch **only** `deck-writer` and
  `deck-reviewer`.
- `permission.skill` gives each agent **only** the skill it needs.
- Subagents start with fresh context; the director hands each one just the outline,
  audience, path and (for revisions) the findings — not the whole conversation.

### Pipeline flow

```
             brief (sample_briefs/*.md)
                       |
                       v
┌──────────────────────────────────────┐
│   deck-director   (primary)          │  skill: slide-outline
│   reads brief, writes outline,       │  shows outline to user
│   delegates via the Task tool        │
└──────────────────────────────────────┘
                       |
                       v
┌──────────────────────────────────────┐
│   deck-writer     (subagent)         │  skill: marp-slides
│   writes decks/<topic>.md            │
└──────────────────────────────────────┘
                       |
                       v
┌──────────────────────────────────────┐
│   deck-reviewer   (subagent, R/O)    │  skill: deck-review-checklist
│   verdict: pass | revise + findings  │
└──────────────────────────────────────┘
          |                     |
        pass             revise (max 2 loops)
          |                     └──────> back to deck-writer
          v
   decks/<topic>.md  →  Marp preview / PDF / PPTX
```

## Agents

| Agent | Mode | Job | Permissions (key ones) |
|---|---|---|---|
| `deck-director` | primary | Reads the brief, outlines the storyline, delegates, runs the revise gate, delivers. | edit `decks/*` only · bash deny · task: writer + reviewer only |
| `deck-writer` | subagent | Writes or revises Marp slides from the outline / findings. Returns a YAML contract. | edit `decks/*` only · bash, webfetch, task deny |
| `deck-reviewer` | subagent | Audits the deck with the 7-point checklist, returns `pass`/`revise` + per-slide findings. | **read-only** · edit, bash, task deny |

## Skills

| Skill | Used by | What it holds |
|---|---|---|
| `slide-outline` | deck-director | Storyline arc, slide-count rule, full-sentence headlines, outline format |
| `marp-slides` | deck-writer | Exact Marp file format, text limits, speaker-note rule |
| `deck-review-checklist` | deck-reviewer | 7 checks with blocker/major/minor severities and the verdict rule |

## Layout

```
Deck_Squad/
├── .opencode/
│   ├── agents/
│   │   ├── deck-director.md
│   │   ├── deck-writer.md
│   │   └── deck-reviewer.md
│   └── skills/
│       ├── slide-outline/SKILL.md
│       ├── marp-slides/SKILL.md
│       └── deck-review-checklist/SKILL.md
├── decks/                      # output decks (sample included)
├── sample_briefs/
│   └── opencode_agents_talk.md
├── opencode.json
└── README.md
```

## Setup

```bash
# install OpenCode (see https://opencode.ai/docs/) and connect a provider
cd Deck_Squad
opencode
```

Then in the TUI:

1. Press **Tab** until `deck-director` is active (it is also the `default_agent`).
2. Type: `Make a deck from sample_briefs/opencode_agents_talk.md`
3. Watch the subagent sessions with **<Leader>+Down**, cycle with **Left/Right**,
   go back with **Up**.

You can also call a specialist directly: `@deck-reviewer check decks/opencode-agents-and-skills.md`.

## Presenting the output

```bash
npx @marp-team/marp-cli decks/opencode-agents-and-skills.md --pdf
# or --pptx, or open it in VS Code with the "Marp for VS Code" extension
```

## Notes

- Works on **any** brief — drop a new file in `sample_briefs/` or describe the talk in chat.
- No model is pinned: the director uses your global model and subagents inherit it.
  Add `model: provider/model-id` to any agent's frontmatter to override.
- Sample output: `decks/opencode-agents-and-skills.md` — a 10-slide deck explaining
  this very project, ready to present.
