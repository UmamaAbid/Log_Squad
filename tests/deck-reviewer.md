Short answer: **no — not safely.** Testing an agent without inspecting its responses tells you very little, and can actively hide problems. Here's why:

## What goes wrong when you don't check responses

- **Silent failures look like passes.** An agent can return a plausible, well-formatted answer that is factually wrong, or pick the wrong tool and still "complete" the task. Without checking, your test harness reports success.
- **Side effects happen regardless.** Agents don't just produce text — they call tools, write files, run commands, hit APIs. An unchecked test run can delete data, send messages, or spend money while the harness logs "✅ passed."
- **Right answer, wrong reason.** An agent may reach the correct output via a broken chain (hallucinated a tool result, skipped a step). It works today and breaks the moment inputs shift slightly — and you'd never know without inspecting the trajectory.
- **No regression signal.** If you never record what the agent actually said/did, you can't compare runs, so "it still works" after a change is unverifiable.

## What safe testing looks like instead

1. **Sandbox everything** — no real credentials, filesystem, or network in test mode; use mocks/dry-run for side-effectful tools.
2. **Assert on the trajectory, not just the final answer** — which tools were called, with what arguments, in what order.
3. **Grade responses** — automated checks (schema, facts, refusal behavior) plus sampled human review.
4. **Log full transcripts** so failures are debuggable and runs are comparable.

If the agent is read-only or fully sandboxed, the *risk* drops a lot — but you still learn almost nothing about quality without checking responses. Unchecked testing is fine for smoke-testing "does it crash"; it's not fine for "does it work."
Deck loaded. Now running the mechanical checks and looking for the outline to verify storyline.
Mechanical checks done: `marp: true` present, no TODOs, and 13 exact `---` lines — but 2 of those are inside slide 4's fenced code block, so the real count is 9 separators after front matter = **10 slides**. No outline file exists in the repo, so let me check for the brief and cross-check the deck's factual claims against the actual agent/skill files it describes.
The skill file itself lives under `.opencode/skills/`, so my glob pattern may have missed dot-directories. Let me retry with broader patterns and check the workspace root too.
There's a `sample_briefs/` folder and `.opencode/`. Glob seems to skip dot-directories, so I'll read them directly.
Found the brief. Reading it plus the agent definitions to verify storyline, facts, and timing.
The brief confirms: 8-minute talk, and the closing line matches slide 10 exactly. Now cross-checking the deck's claims about the squad against the actual agent files and skills.
All cross-checks against the brief and the actual squad files are done. One claim in the deck isn't sourced from the brief: slide 8's speaker notes reference a "Leader plus Down" keybind for subagent sessions. Let me verify that against OpenCode's docs before classifying it.
Verification complete — the OpenCode docs confirm the deck's claims (Tab cycles primary agents, leader+Down enters subagent child sessions, built-ins are Build/Plan + General/Explore/Scout). Here is the audit.

```yaml
verdict: pass
summary: "Deck matches the brief's order, facts, and closing line with clean density and notes; three polish-level findings, none blocking."
findings:
  - slide: 9
    check: "one-message-per-slide"
    severity: major
    fix: "Replace the label headline 'Recap' with the slide's message, e.g. 'One job per agent, fewest permissions, plain markdown files'."
  - slide: 7
    check: "facts"
    severity: minor
    fix: "Mode column says 'subagent' for deck-writer/deck-reviewer, but both agent files use 'mode: all' — label them 'all (runs as subagent)' or footnote that they are also @mentionable."
  - slide: 4
    check: "facts"
    severity: minor
    fix: "Brief's must-include lists 'steps' and 'color' frontmatter keys; add them to the example or mention them in the speaker notes."
```

**Checklist rundown**

| # | Check | Result |
|---|---|---|
| 1 | storyline | ✅ Slide order mirrors the brief's must-include sequence (types → files → permissions → skills → squad → gate); takeaway "Give each agent one job and the fewest permissions it needs" is slide 10's headline, verbatim from the brief |
| 2 | one-message-per-slide | ⚠️ 1 major — slide 9's "Recap" is a label headline; all other headlines are assertions |
| 3 | text-density | ✅ Max 4 bullets/slide, longest bullet 9 words; tables are compact |
| 4 | speaker-notes | ✅ All content slides (2–10) have `<!-- -->` notes; title slide exempt |
| 5 | facts | ✅/⚠️ No TODOs; every claim traces to the brief or was verified against opencode.ai docs (incl. the "Leader plus Down" demo tip on slide 8, confirmed as `session_child_first`); 2 minor gaps above |
| 6 | format | ✅ `marp: true` present, separators clean, code block tagged `markdown` |
| 7 | timing | ✅ 10 slides vs 8-minute brief — exactly at the minutes+2 ceiling, not over |

**Note for the director:** a naive grep counts 13 `---` lines, but 2 sit inside slide 4's fenced code block — the deck is 10 slides, not 11. Marp parses it correctly; nothing to fix.

**Verdict: pass** — the deck is deliverable as-is; the three findings are cheap polish if the writer wants to burn a revision loop on them.
