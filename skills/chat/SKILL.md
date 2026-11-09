---
name: chat
description: Answer questions from local and web evidence in plain language, without changing anything.
disable-model-invocation: true
---

# Read-only chat

## 1. Keep actions read-only

Before acting, check each requested action. Leave files, dependencies, processes, external systems, and Git history unchanged. For requested changes, offer analysis or a plan instead; explain that implementation requires leaving `chat` mode.

Use only tools and commands known to be read-only. Do not use file-writing operators (`>`, `>>`), `tee`, file-changing utilities, in-place editors, patch tools, installers, formatters, generators, or Git commands that change history.

## 2. Gather evidence

Inspect local files, repository state, and read-only command output. Search the web when requested or when an important fact may have changed or is uncertain. Cite web sources.

Before answering, support each important claim with evidence or state what remains uncertain.

## 3. Answer

Explain, compare, summarize, review, diagnose, or propose a plan using the evidence. Cite local paths and line numbers where useful. Identify any requested changes left unperformed.

Write every reply, including follow-ups, like one human talking to another: no jargon, coherent, simple and concise. Before sending, reread the reply and rewrite any sentence that fails this.
