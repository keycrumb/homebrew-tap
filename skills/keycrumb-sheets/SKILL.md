---
name: keycrumb-sheets
description: Use when creating or editing KeyCrumb Markdown or JSON cheat sheets, including local images and title icons. Excludes developing the native KeyCrumb app.
license: MIT
---

# KeyCrumb sheets

Create complete, readable local reference files. Use the requested format and preserve an existing file's format when editing. Otherwise prefer Markdown for commands/general references and JSON for grouped macOS shortcuts.

- For Markdown, read [Markdown authoring](references/markdown.md).
- For JSON, read [version 1 format](references/json-format.md) and use the bundled [schema](references/keycrumb-sheet.schema.json). Do not fetch a schema to author offline.
- The [example library](assets/example-library/commands.md) and [JSON example](assets/example-library/editor.keycrumb.json) are adaptable templates; copy their referenced assets alongside the sheets.

Use the user's selected library path. If none is supplied, create a deliverable folder in the current task workspace and explain how to select that folder in KeyCrumb. Put UTF-8 `.md` or `.keycrumb.json` sheets at its top level, each at most 2 MiB; avoid hidden files and symlinks. Images resolve from the library root, not from the skill folder.

Before writing, inspect destination conflicts. Preserve existing sheets/assets; choose unused names for new output. For requested edits, preserve file identity and content outside the requested change. Use descriptive filenames and stable semantic JSON IDs. Deliver every referenced asset; omit optional icons when suitable artwork is unavailable and report that omission. Never leave invented downloads or missing image references.

Keep command tables concise without row-number columns. Research shortcut accuracy against official documentation when available; state platform, application version/keymap and uncertainty in the delivery message. Format validity alone does not verify shortcuts. Keep citations outside copy targets and unsupported JSON fields. Never execute sheet commands as part of authoring.

For JSON, optionally run `python3 scripts/validate_sheet.py <sheet.keycrumb.json> --library-root <folder>` from this skill folder. Dependencies and limits are in the [JSON guide](references/json-format.md#optional-validator). Fix icon warnings or remove the optional icon reference before calling output clean. If validation tools are unavailable, perform available checks and disclose incomplete validation.

Finish with exact created/edited paths, how to open the library in KeyCrumb, checks performed and remaining uncertainty. Preserve existing output if validation fails; repair only files created or edited for this request.
