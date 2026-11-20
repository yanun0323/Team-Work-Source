---
name: build-local
description: Build and verify a local macOS App bundle and ZIP package for the current project. Use when the user requests `build local` or before publishing a stable or dev release.
---

# Build local

## Discover the project's packaging

Before building, read the project's build entry points (`Makefile`, package
scripts, `Scripts/` or similar, README and contributor docs) and establish:

- The test command(s) that apply to the changed code.
- The packaging command (for example `make package`) and the variables it
  accepts, such as App version, build version, build flavor, or notary profile.
- The App bundle and ZIP paths it produces.
- Any existing package verification script; prefer it over ad-hoc checks.
- The localizations the App ships and how resources are loaded at startup
  (for example SwiftPM `Bundle.module` versus `Contents/Resources`).

If the project has no packaging command, stop and ask rather than invent one.

## Build and verify

1. Run the applicable tests.
2. Run the project's packaging command. When called from a release procedure,
   pass the explicit App and build versions it supplies.
3. Verify the App with `codesign --verify --deep --strict`.
4. Extract the ZIP to a new temporary directory. Verify the extracted App again.
5. Start the packaged App in an isolated check that denies access to the
   project's build directory (for example `.build` or `DerivedData`). Confirm
   that the App stays open and does not crash or trap during startup, including
   localization and resource-bundle initialization.
6. Confirm that the packaged App loads every shipped localization from inside
   its own bundle, not from the build machine.

The packaged App must not require an absolute path from the build machine.
Keep local packaging on the local machine. Do not create a tag, notarize an
artifact, or upload an artifact.

`build local` is complete only when the App and the extracted ZIP pass all
checks. Report the artifact paths, the checks run, and any check that could not
run.
