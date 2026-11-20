---
name: release-new-version
description: Build, verify, and publish a stable macOS App release through the project's release script. Use when the user requests `release new version`.
---

# Release new version

1. Read [the shared release procedure](references/release-common.md). Complete its
   discovery, source and destination checks before choosing a version.
2. If the user does not give a version, inspect local and remote stable tags
   (for example `vX.Y.Z`), GitHub Releases, and the signed public update feed;
   increment the latest stable patch version. Stop on conflicting records or if
   an active dev series makes the intended stable version unclear. Validate any
   supplied version and confirm that its tag and release are not already
   published.
3. Write or update the stable notes file in the project's release notes
   directory and naming (for example `ReleaseNotes/X.Y.Z.md`), in the language
   existing notes use, from changes since the previous stable release, including
   changes already shipped in dev builds. Summarize user-facing improvements,
   fixes, known limitations, breaking changes, and required upgrade steps.
4. Complete shared local verification, credential, approval, and tag checks, then
   publish with the project's release command and explicit stable settings,
   for example:

   ```sh
   make release VERSION=X.Y.Z CHANNEL=stable \
     TAG=vX.Y.Z BUILD_VERSION=X.Y.Z \
     RELEASE_NOTES_FILE=<notes-dir>/X.Y.Z.md
   ```

   Use the argument names the script actually accepts.
5. Complete shared artifact and public-feed verification. Verify the GitHub
   Release is not a prerelease and is the intended latest stable release. If the
   project has an update feed, check that the new item is available to the stable
   channel and that the updater (for example Sparkle) ranks it above preceding
   dev builds for the same version.

Complete only when downloaded release artifacts and the public stable feed pass
all checks. Report the shared evidence and follow its partial-publication rules
if any later check fails.
