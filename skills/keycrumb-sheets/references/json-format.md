# JSON cheat sheets, version 1

Put UTF-8 `.keycrumb.json` files at the top level of the selected library, at most
2 MiB each. Hidden and symlinked sheets are unsuitable. The bundled
[schema](keycrumb-sheet.schema.json) is self-contained. KeyCrumb validates locally
and displays content without executing shortcuts or rewriting files.

## Contract

| Object | Required fields | Optional fields |
| --- | --- | --- |
| Sheet | `schemaVersion`, `title`, `sections` | `description`, `icon` |
| Section | `id`, `title`, `entries` | `description`, `icon` |
| Entry | `id`, `title`, `shortcuts` | `text` |
| Shortcut alternative | `steps` | none |
| Step | `modifiers`, `key` | none |

`schemaVersion` is exactly `1`. JSON text is plain text, not Markdown. Entry
explanations use `text`, not `description`. Icons exist only on sheets and
sections. Optional `description`, `text` and `icon` fields may be omitted or null.
Unknown properties are ignored by the app; do not invent layout, entry images,
verification badges or metadata fields. Columns are chosen by the viewer.

Titles contain non-whitespace text, at most 200 Unicode scalars. U+200B alone
also counts as empty under the native whitespace rule. IDs contain
non-whitespace text, at most 128 scalars. Section IDs are unique within the sheet;
entry IDs are unique across all sections. Descriptions and entry text are at most
4000 scalars. A sheet has 1–100 sections, at most 200 entries per section and 2000
overall. A section may be empty. An entry has 0–4 alternative shortcuts; an empty
`shortcuts` array creates a text-only row. Each alternative has 1–8 sequential
steps. Every step has `modifiers` (possibly empty) and `key`.

Modifiers are `function`, `control`, `option`, `shift`, `command`, without repeats.
They display in that order regardless of array order. Keys are case-sensitive:
`f1`–`f24`, one printable non-whitespace Unicode scalar (for example `é`, `[` or
`+`), or one of:

`return`, `enter`, `tab`, `escape`, `space`, `delete`, `forwardDelete`, `capsLock`,
`arrowLeft`, `arrowRight`, `arrowUp`, `arrowDown`, `home`, `end`, `pageUp`, `pageDown`.

Alternative objects display with `/`; steps in one alternative display with `→`.
A sequence separator is distinct from the `arrowRight` key. Neither triggers a
shortcut. See the [complete example](../assets/example-library/editor.keycrumb.json)
for alternatives, a sequence, descriptions, entry text and a text-only row.
Example key bindings are illustrative, not verified against a particular editor.

## Local images

```text
My Library/
  commands.md
  editor.keycrumb.json
  icons/editor.png
  images/workflow.png
```

Use `"icon": "icons/editor.png"`. Resolve paths from the selected library root,
never the installed skill or current working directory. `icons/` and `images/`
are conventions. Include every referenced asset, preserve existing destination
files, and omit optional icons when no suitable artwork is available.

Raw icon paths are at most 1024 UTF-8 bytes, before path normalization.
JSON icons must be static PNGs, exactly **256 × 256 pixels**, at most **262144
bytes**, preferably transparent. A renamed JPEG is not PNG. Remote, absolute and
escaping paths are rejected. Invalid or missing icons yield a neutral placeholder
and warning; they do not hide valid sheet content. Fix warnings or remove the
optional field before delivering clean output. Markdown images instead accept
local decodable files up to 10 MiB; JSON icon dimensions do not apply to them.
Moving a library must move its assets alongside its sheets.

## Optional validator

Python 3.11+ and the pinned dependencies in
[requirements.txt](../scripts/requirements.txt) are optional authoring tools.
Create an isolated environment and install them there:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r scripts/requirements.txt
.venv/bin/python scripts/validate_sheet.py <sheet.keycrumb.json> --library-root <directory>
```

Run from the installed skill folder, or use absolute script/requirements paths.
The validator reads the bundled schema offline and never writes the library. Exit
0 means structurally valid (possibly with icon warnings), 1 means invalid content,
and 2 means invocation or dependency failure. Diagnostics include file and JSON
field path. It checks extra runtime constraints such as duplicate IDs, 2000 total
entries, file boundaries and decoded icons. It does not verify shortcut accuracy,
Markdown prose, native image-decoder equivalence, rendering, selection or copying.
If dependencies cannot be installed, report checks performed and incomplete
validation; do not invent a pass. Test in KeyCrumb when available.
