---
name: writing-for-agents
description: Write, edit, review, or clean up agent instructions in skills, AGENTS.md, CLAUDE.md, and supporting files.
---

## Highest principle

Use the fewest words needed for clear understanding and correct execution. This governs both documents and messages to the user; every rule below serves it.

## Read before editing

Read the whole document and its supporting files, not just the changed passages. For skills, also read [SKILL-MECHANICS.md](SKILL-MECHANICS.md) for settings, who can start them, and when to create a separate skill.

## Write plainly

- Use familiar words and concrete actions, not jargon. Use the same word for the same idea.
- When rewriting, preserve meaning, required behavior, and firm boundaries.
- Keep file names, commands, and code identifiers exact; explain them when needed.
- Say what to do. Keep explicit prohibitions for firm boundaries and give an allowed alternative when possible.

## Organize around the task

Put actions in execution order, with definitions, exceptions, and short explanations beside the actions they support. Do not invent steps for reference-only documents.

Keep instructions needed on every run in the main file. Split out task-specific details only when this lets the agent read less, not merely to shorten the main file. Each split adds a file to find and maintain. Leave choices requiring judgment to the user; otherwise, tell the agent what to read.

For skill descriptions and file references:

- Put the task or subject first and say when to use the skill or file.
- Cover each distinct situation; combine equivalent phrases and omit details clear from the name.
- Keep always-loaded descriptions short. Files without references rely on the user remembering them.

Example: “Before changing an Apple app screen, read `DESIGN.md` for layout and interaction rules.”

If the agent skips a required file, clarify when to read it. Only if that fails, move essential rules into the main document rather than copying them.

## Make completion checkable

For each step, define its full scope and what must be true before moving on. For reference-only documents, state which rules to check and what they apply to.

- Replace “understand the changes” with “identify every changed model and its affected callers.”
- Replace “check the rules” with “check every rule against the changed code and report each violation.”

If the agent rushes, clarify the completion condition first. If it cannot be made precise and rushing continues, consider a separate agent or handoff that withholds later steps. Another heading or file in the same conversation does not hide them.

## Clean up and verify

Apply this check to every writing or editing task, including cleanup-only requests. Fix problems directly unless the user asked for findings only.

1. Remove repeated meanings, even when worded differently. Give each rule one authoritative home and link to it elsewhere.
2. Delete filler, unrelated explanations, and instructions that do not change behavior. Let project files supply commands, settings, and directory contents unless looking them up is genuinely costly. Record what they cannot explain: unwritten conventions, reasons for choices, and useful surprises.
3. Resolve conflicts using applicable instruction priority and the user's stated intent. If the intended behavior remains unclear, ask before changing it. Correct unclear or outdated wording.
4. Reread the full result and supporting files. Fix remaining repetition, unnecessary content, and conflicts; verify settings and file references. Report blocked decisions rather than claiming completion.
5. Briefly report what you removed or combined, any conflicts resolved, and what you checked.

If an instruction's value is uncertain, try the task with and without it. Judge results, not forceful wording.
