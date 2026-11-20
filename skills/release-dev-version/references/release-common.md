# Shared release procedure

Read this file from either release skill. The calling skill supplies the channel,
version, build version, tag, and notes path. Follow these checks in order; the
project's release script remains the source of truth for commands and supported
arguments.

## Discover the project's release setup

Read the project's release entry points (`Makefile`, release, packaging and
verification scripts, README and contributor docs) and establish:

- The release command (for example `make release`) and its required arguments:
  version, build version, channel, dev number, tag, notes file.
- The GitHub repository it publishes to, and the push remote.
- The update feed, if any: for Sparkle, the `SUFeedURL` in `Info.plist` and how
  the feed is deployed (for example GitHub Pages or a `gh-pages` branch).
- The release notes directory and file naming, and the tag naming for stable
  and dev releases, from existing files and tags.
- The build flavor or configuration used for distribution builds.

If the project has no release script, or the script does not support the
requested channel, stop and ask. Do not assemble an ad-hoc publication pipeline.

## Prepare the source and destination

- Inspect the working tree, selected commit, remotes, target GitHub repository,
  and public feed. Confirm the push remote and release repository refer to the
  same project.
- List the proposed changes and any unrelated tracked or untracked work. Resolve
  release scope with the user before committing or packaging mixed work. Preserve
  unrelated changes; do not automatically stash, discard, or include them.
- Check that public documentation and any maintained local operations docs still
  match the release behavior. Prepare the calling skill's notes, commit only
  approved changes, and record the source commit. Require a clean checkout,
  including untracked files, before running the release script.
- Save the current latest stable release identity and the signed public feed for
  comparison after publication. An authentication, network, or verification
  failure is not evidence that a version or tag is unused.

Done when the source scope and destination are known and the notes match the
selected commit.

## Verify locally and check credentials

- Complete [build-local](../../build-local/SKILL.md) for the selected source and version.
  Pass explicit App and build versions to local packaging. Keep the notary
  profile unset for this local-only stage, restoring it only for release.
  If changing source after validation, rerun affected tests and packaging checks.
- Require an available Developer ID signing identity, authenticated `gh` for the
  target repository, the update-feed signing tools (for example Sparkle's), and a
  usable notary Keychain profile. Respect the current user's credential
  instructions. Use the explicitly configured or user-specified profile; if none
  is known, ask rather than guess. Check it with
  `xcrun notarytool history --keychain-profile "<profile>"`. If unavailable,
  stop; do not retrieve, print, or log credentials or switch profiles silently.
  The feed signing account and the notary profile are separate settings.
- Confirm the script builds the distribution flavor and verifies the signed,
  notarized App and ZIP before publication. Verification must cover signatures,
  notarization, every shipped localization, and startup without the project's
  build directory.

Done when local verification passes and release signing prerequisites are usable.

## Approve and publish

- Present repository, commit, channel, App/build versions, tag, notes, and the
  intended tag push, GitHub Release, and feed update. Obtain approval of this
  exact publication plan before creating/pushing the tag or publishing.
- Create the agreed tag at the verified commit and push only that tag. If a tag
  already exists locally or remotely, verify its peeled commit; never overwrite
  it. Stop on mismatch. An existing GitHub Release requires recovery, not another
  `gh release create`.
- Verify `HEAD`, the local tag, and the remote tag all resolve to the same commit
  and the checkout remains clean.
- Run the calling skill's release command with explicit channel, version, tag,
  build version, and notes path. Preserve the script's pre-upload checks and
  bounded feed-deployment wait. Stop on failure; no automatic retry loop or
  force push.

## Verify the published result

- Download the published ZIP and feed fresh from GitHub and the public feed URL;
  do not rely on local build files. Require downloaded archive verification to
  pass again, including notarization, localization, and isolated startup. Verify
  the feed signature, attachment identities, and checksums against the uploaded
  artifacts.
- Check the calling skill's GitHub prerelease/latest and update-channel rules.
  Verify the public feed actually serves the expected signed contents after
  deployment; a successful push to the deployment branch alone is insufficient.
- If `gh release create` fails partway (for example HTTP 500), it may leave a
  draft with attachments already uploaded. Inspect it with `gh release view`
  before any recovery; do not create it again.
- Report the source commit, versions, tag, release URL, SHA-256 of every
  downloaded attachment, and any checks that could not run. Keep validation
  records in the project's existing operations documentation when available.

Complete only when artifacts and public feed pass. If upload succeeds but download
verification, channel checks, or feed verification fails, report **partially
published**, with the exact completed stage. Preserve the existing tag and release;
inspect the remote state and obtain approval for a targeted recovery. Never delete,
replace, or recreate published artifacts merely to make a rerun pass.
