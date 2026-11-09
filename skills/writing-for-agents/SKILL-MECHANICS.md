# Skill settings and use

When creating, editing, or reviewing a skill, use this file for settings and selection rules, and [SKILL.md](SKILL.md) for writing and review rules.

## Choose who can start it

Set these fields at the top of `SKILL.md`.

### Agent or user

Use this when the agent should recognize the task or another skill needs to call it. The user can also request it by name.

- Omit `disable-model-invocation`.
- Write a `description` stating the task and when to use the skill.

### User only

Use this when the skill should run only on an explicit request by name.

- Set `disable-model-invocation: true`.
- Keep `description` to a one-line summary for the user; automatic-selection triggers are unnecessary.

The description is not offered to the agent for automatic selection. The user must remember the skill; other skills cannot start it. To share rules between user-only skills, link both to a reference file instead of making one start the other.

## Decide whether to create another skill

Create a separate, automatically selectable skill for a distinct task that should start independently or be called by another skill. Name it after requests people actually make. Otherwise, keep related material together: each skill adds a description for the agent to consider.

If user-only skills become hard to remember, create one user-only skill listing them and when to use each. It helps the user choose what to request next; it does not start them.
