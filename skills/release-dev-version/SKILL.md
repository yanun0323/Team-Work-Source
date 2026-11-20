---
name: release-dev-version
description: Build, verify, and publish a macOS App dev prerelease through the project's release script. Use when the user requests `release dev version`.
---

# Release dev version

A dev release is a signed, notarized distribution build published to the dev
update channel, not a local build with fewer checks. For local-only packages,
use [build-local](../build-local/SKILL.md).

1. Read [the shared release procedure](references/release-common.md). Complete its
   discovery, source and destination checks before choosing a version. Confirm
   the release script supports a dev or prerelease channel; if not, stop and ask.
2. Inspect local and remote tags, GitHub Releases, and the signed public update
   feed. Use numeric version ordering, not tag dates or lexical sorting.
   If the user supplies a version or dev number, validate it against all three.
   Otherwise continue the single active dev series newer than the latest stable
   version; if none exists, increment the latest stable patch version. If several
   series are active, records disagree, or remote inspection fails, stop and ask.
3. For the selected `X.Y.Z`, choose one more than the highest reserved or
   published dev number across those records, starting at 1. Respect any range
   the project or build-version format imposes (for example `N` in `1..255`).
   Stop at exhaustion; never reuse a published number or move a tag.
   Derive the identities from the project's existing dev scheme in its script,
   tags and feed. A common Sparkle scheme is:
   - App version: `X.Y.Z`
   - Build version: `X.Y.ZdN`
   - Git tag: `vX.Y.Z-dev.N`

   If the project has no prior dev releases and its script does not define a
   scheme, propose one and get approval before using it.
4. Verify ordering with the updater's own version comparator (for example the
   bundled Sparkle comparator), not a generic SemVer parser: the proposed build
   must be newer than the latest stable and preceding dev build, and older than
   the eventual `X.Y.Z` stable build. If the comparator cannot be exercised, stop
   rather than assume the order.
5. Write dev notes in the project's release notes directory and naming (for
   example `ReleaseNotes/X.Y.Z-dev.N.md`), in the language existing notes use.
   Describe changes since the preceding dev release of this series, or the latest
   stable release for the first dev build. Identify known limitations and
   required upgrade steps; distinguish fixed-output tests from real-world
   validation. Keep stable notes unchanged unless independently inaccurate.
6. Complete the shared preparation, approval, and tag checks, then publish using
   the project's release command, for example:

   ```sh
   make release VERSION=X.Y.Z CHANNEL=dev DEV_BUILD=N \
     TAG=vX.Y.Z-dev.N BUILD_VERSION=X.Y.ZdN \
     RELEASE_NOTES_FILE=<notes-dir>/X.Y.Z-dev.N.md
   ```

   Use the argument names the script actually accepts.
7. Complete shared artifact and public-feed verification. Additionally verify
   that GitHub marks this release as a prerelease, the previous latest stable
   release remains latest, and the new feed item is restricted to the dev channel
   (for Sparkle, `sparkle:channel` equal to `dev`). Compare against the saved
   pre-release feed: its stable item and download URL must remain available.
   Check stable/dev channel selection using the App's existing updater
   integration; do not change the user's saved update channel.

Complete only when the downloaded artifacts and public dev feed pass verification.
Report the commit, App/build versions, tag, URL, SHA-256 values, and validation
limits. Follow the shared partial-publication rules if any later check fails.
