---
marp: true
theme: default
paginate: true
title: OpenCode Agents & Skills
---

<!-- _class: lead -->
# OpenCode Agents & Skills
Building a 3-agent squad · Code-Sessions

---

## One big agent with every tool gets messy fast

- One prompt tries to plan, write and review
- Every tool is allowed, so mistakes cost more
- Context fills with things the task never needed

<!--
Speaker notes: Start with the problem. A single agent doing everything mixes jobs, has too much power, and wastes its context window. Agents and skills are OpenCode's answer.
-->

---

## OpenCode has two kinds of agents

| Primary | Subagent |
|---|---|
| You talk to it directly | Called by another agent |
| Switch with **Tab** | Task tool or `@mention` |
| Build, Plan | General, Explore, Scout |

<!--
Speaker notes: Primary agents run the main conversation; you cycle them with Tab. Subagents are specialists a primary agent launches for one job, or that you call with an @mention. These five are built in.
-->

---

## An agent is just a markdown file

```markdown
---
description: Reviews decks, never edits
mode: subagent
temperature: 0.1
permission:
  edit: deny
---
You are the quality gate...
```

<!--
Speaker notes: Put the file in .opencode/agents. The file name becomes the agent name. Frontmatter is configuration; the body is the system prompt. Description is the only required key.
-->

---

## Permissions give each agent only what it needs

- Values: `allow`, `ask`, `deny`
- Glob patterns, e.g. `"decks/*": allow`
- Last matching rule wins — put `"*"` first
- `permission.task` limits which subagents it can launch

<!--
Speaker notes: This is the safety layer. Our writer can only edit inside decks, our reviewer cannot edit at all, and the director can only launch our two subagents.
-->

---

## Skills are instructions loaded only when needed

- Path: `.opencode/skills/<name>/SKILL.md`
- Needs `name` and `description` in frontmatter
- Name: lowercase, hyphens, matches folder
- The `skill` tool loads the body on demand

<!--
Speaker notes: An agent only sees each skill's name and description until it decides to load one. That keeps the context small, which is the same problem the team asked about with large codebases.
-->

---

## Deck Squad: one lead, two specialists

| Agent | Mode | Job | Can edit? |
|---|---|---|---|
| deck-director | primary | Outline + delegate | `decks/` only |
| deck-writer | subagent | Write Marp slides | `decks/` only |
| deck-reviewer | subagent | 7-point audit | No |

<!--
Speaker notes: Each agent has one job and one skill. The director uses slide-outline, the writer uses marp-slides, the reviewer uses deck-review-checklist.
-->

---

## A review gate keeps quality up without looping forever

- Director outlines, writer drafts the deck
- Reviewer returns `pass` or `revise` with findings
- At most 2 revise loops, then deliver with notes

<!--
Speaker notes: Demo time. Run opencode in the repo, Tab to deck-director, and give it the sample brief. Show the subagent sessions with Leader plus Down.
-->

---

## Recap

- Primary agents lead; subagents specialise
- Permissions limit power; skills limit context
- Agents and skills are plain markdown files

<!--
Speaker notes: Three things to remember. Then open for questions.
-->

---

<!-- _class: lead -->
## Give each agent one job and the fewest permissions it needs

Questions?

<!--
Speaker notes: Close with the line from the brief and take questions.
-->
