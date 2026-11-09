---
name: project-cleanup
description: Clean up an existing project by removing unused or obsolete files, code, and dependencies, and merging overlapping docs. Use when asked to tidy a project or consolidate documentation.
---

# Project cleanup

Reduce clutter without losing useful information or changing intended behavior. Inspect first; change only an approved list. Do not turn cleanup into a redesign.

## 1. Set scope

- Read project instructions and inspect Git status. Use the requested scope; otherwise inspect the current repository.
- Inventory tracked files and relevant untracked files. Identify documentation, source, configuration, scripts, dependencies, and generated output.
- Exclude version-control internals, installed dependencies, vendored code, caches, and generated output from content review. Consider generated output for removal only when its regeneration and consumers are known.
- Leave existing user changes and untracked files untouched. Do not read secret values or remove credentials, local data, licenses, or required legal records.
- Find the project's existing build, test, and documentation checks. Do not install cleanup tools just to perform this task.

## 2. Establish evidence

Read each candidate text file completely before judging it. For binary files, inspect metadata and consumers. Inspect related callers, configuration, and documents as needed.

For each candidate, choose **delete**, **merge**, **update**, or **keep**:

- **Unused files or code:** check entry points, imports, dynamic loading, file discovery, build/package rules, scripts, CI, tests, and documented external use. No search matches alone is not proof of non-use.
- **Dependencies:** check application code, development tools, scripts, configuration, and platform-specific use. Identify required manifest and lockfile updates.
- **Outdated docs:** verify claims against current code and supported workflows. Distinguish current instructions from historical decisions and future requirements. An implementation disagreement does not by itself make a requirement obsolete.
- **Overlapping docs:** read all proposed sources, identify their unique useful content, and choose one existing home where possible. Keep separate audiences and translations separate unless they truly duplicate the same purpose.
- **Completed plans and reports:** move still-useful decisions, constraints, and procedures into their lasting home before removing the temporary record. Preserve records with an explicit audit, legal, operational, or historical purpose.

Age, filename, size, and tool warnings are leads, not deletion evidence. Keep uncertain items and state what could not be verified. Do not delete tests merely because they fail or appear repetitive; identify the coverage that remains.

## 3. Get approval — stop here

Report in the conversation, not a new file:

- Scope inspected and anything excluded or not inspected.
- Each proposed action, exact paths, supporting evidence, and risk.
- For merges, the destination and unique content to preserve.
- Validation commands and how the original content can be recovered.
- Uncertain items left unchanged.

Ask for approval of the specific list and wait. A request to clean up is not approval of unseen deletions. If the user requested an audit only, finish here.

## 4. Apply the approved list

- Recheck Git status and candidate contents. If they changed since review, reassess affected actions and seek approval for changes to the list.
- Run relevant checks before editing to establish existing failures. Confirm recovery through committed history or an approved backup; do not delete content that cannot be recovered.
- Work in small, related batches. Preserve useful content in the merge destination before deleting its sources. Resolve factual conflicts from evidence; leave unresolved conflicts for the user rather than guessing.
- Update affected links, indexes, imports, scripts, manifests, and lockfiles in the same batch. Keep documentation changes limited to the cleanup's effects.
- Use Git history instead of creating archives unless continued access to an archive serves an explicit need. Do not create cleanup reports, replacement summaries, or redirect files just to record the work.
- Do not use blanket deletion commands such as `git clean`, overwrite user work, commit, or push. New cleanup candidates require a new approval.

## 5. Verify and finish

- Inspect the full diff: only approved changes and their necessary reference updates should remain.
- Search for removed paths and names; fix stale references. Check affected links and anchors, and reread merged documents for omissions, repetition, and contradictions.
- Rerun the relevant build, test, and documentation checks. Add regression tests only where cleanup creates a meaningful coverage gap; do not weaken tests to get a pass.
- If a batch introduces a failure, fix it within scope or undo only that batch's own changes. Report existing failures and checks that could not run; do not claim success from incomplete verification.
- Briefly report what was removed or merged, verification results, and anything left unresolved. Leave the changes uncommitted for review.
