# Brief: OpenCode Agents & Skills

- **Audience:** junior developers in our Code-Sessions group, new to AI coding agents
- **Time:** 8 minutes
- **Goal:** explain what OpenCode agents and skills are, and show Deck Squad as a working example

## Must include

- Two agent types: **primary** (switch with Tab) and **subagent** (called by the task tool or `@mention`).
- Built-in agents: Build and Plan (primary); General, Explore and Scout (subagents).
- Agents are markdown files in `.opencode/agents/`; the file name is the agent name.
- Frontmatter keys: `description` (required), `mode`, `temperature`, `steps`, `permission`, `color`.
- Permissions are `allow` / `ask` / `deny`, can use glob patterns, and the last matching rule wins.
- `permission.task` controls which subagents an agent may launch.
- Skills live in `.opencode/skills/<name>/SKILL.md`, need `name` + `description`, and are loaded on demand by the `skill` tool — so they cost no context until used.
- Skill names: lowercase, hyphen-separated, must match the folder name.
- Demo: Deck Squad = `deck-director` (primary) → `deck-writer` → `deck-reviewer`, with a 2-loop revise gate.

## Close with

"Give each agent one job and the fewest permissions it needs."
