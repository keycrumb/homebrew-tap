# KeyCrumb Homebrew tap

Install [KeyCrumb](https://keycrumb.com/), a macOS menu bar reference viewer for
local cheat sheets. This tap tracks the current public alpha. The app is free
and proprietary; this repository contains its Homebrew installation definition,
not the app source.

Requires Apple silicon and macOS 15 (Sequoia) or newer. Intel is untested and is
not enabled in this cask.

## Install

```sh
brew install --cask keycrumb/tap/keycrumb
```

Homebrew adds the tap automatically. If your Homebrew version asks you to trust
this third-party cask, review `Casks/keycrumb.rb`, then run:

```sh
brew trust --cask keycrumb/tap/keycrumb
brew install --cask keycrumb/tap/keycrumb
```

Launch KeyCrumb from Applications. If you already installed it manually, quit it
and use `brew install --cask --adopt keycrumb/tap/keycrumb` only when the installed
app matches the cask's release. Check its version and build in About KeyCrumb
first: Homebrew may adopt a different build when an app has its own updater.
Do not use `--force` to replace a newer app with an older alpha.

## Updates and removal

KeyCrumb keeps its signed Sparkle updater. Homebrew's normal bulk upgrade can skip
apps with their own updater. To request a Homebrew upgrade explicitly:

```sh
brew update
brew upgrade --cask keycrumb/tap/keycrumb
```

```sh
brew uninstall --cask keycrumb/tap/keycrumb
```

Ordinary uninstall removes the app and retains preferences and your local sheets.
This tap does not define a `zap` operation for deleting user data.

## Maintaining a release

After the app release pipeline has published and verified its final DMG and
signed appcast:

1. Run `brew livecheck --cask keycrumb/tap/keycrumb` to read the public feed.
2. Download the immutable `https://downloads.keycrumb.com/v<VERSION>/KeyCrumb-<VERSION>.dmg`
   and its `.sha256` file. Verify the actual DMG with `shasum -a 256`.
3. Open a cask update with the verified version and checksum:

   ```sh
   brew bump-cask-pr --no-fork --version='<VERSION>' --sha256='<SHA256>' keycrumb/tap/keycrumb
   ```

4. Review the diff and wait for **Cask checks** on that exact pull request commit
   before merging. The workflow checks style, online audit, installation,
   Gatekeeper assessment, launch, reinstall and preference retention on uninstall.
5. Check that the public tap serves the merged version and installation works.

The cask uses immutable versioned downloads, never `/latest/KeyCrumb.dmg`.
`livecheck` reads the alpha version from the public Sparkle feed; it does not
publish changes. Updates are manual initially, with no additional credentials,
scheduled jobs or changes to the app's signing pipeline.

For local validation, register this checkout as a tap, then run:

```sh
brew tap --custom-remote keycrumb/tap /absolute/path/to/homebrew-tap
brew trust --cask keycrumb/tap/keycrumb
brew style --cask keycrumb/tap/keycrumb
brew audit --cask --online keycrumb/tap/keycrumb
brew livecheck --cask keycrumb/tap/keycrumb
```

CI installs into Applications on a disposable runner. On a development Mac, use a
temporary `--appdir` when testing so an existing KeyCrumb installation is preserved.

Report app problems to [support@keycrumb.com](mailto:support@keycrumb.com).
Report packaging problems in this repository's issues.

## Create sheets with a coding agent

The portable **keycrumb-sheets** skill teaches an agent to create concise Markdown
references and version-1 JSON shortcut sheets, with complete local images. Skill
installation belongs to your coding agent. Generated sheets and their assets
still belong in a folder selected in KeyCrumb; installing the skill does not add
sheets to the app or grant access to your library.

Try:

> Create a concise Git Markdown sheet for KeyCrumb, with small Action/Command
> tables and no row numbers. Put it in a new deliverable folder.

> Create a KeyCrumb JSON sheet for my editor on macOS, with section descriptions,
> entry text, shortcut alternatives and a sequence. Include suitable local title
> icons if available, and identify the editor version and keymap you checked.

### Download and manual installation

Skills use independent versions. The version-0.1.0 assets are
[keycrumb-sheets-0.1.0.zip](https://github.com/keycrumb/homebrew-tap/releases/download/skills-v0.1.0/keycrumb-sheets-0.1.0.zip),
[keycrumb-skills-plugin-0.1.0.zip](https://github.com/keycrumb/homebrew-tap/releases/download/skills-v0.1.0/keycrumb-skills-plugin-0.1.0.zip)
and [SHA256SUMS](https://github.com/keycrumb/homebrew-tap/releases/download/skills-v0.1.0/SHA256SUMS)
on the [skills release page](https://github.com/keycrumb/homebrew-tap/releases/tag/skills-v0.1.0).
Until that tag is published, use this checkout's skill folder for local evaluation;
these links do not establish that a release exists.

Download the standalone ZIP and checksums into the same folder. Verify the
archive's listed SHA-256, then extract it. The ZIP contains a single
`keycrumb-sheets/` folder; copy that **whole folder**, including references,
scripts, examples and license, into an unused destination below. Run from your
project folder when using project installation.

| Host | Project destination | Personal destination | Invocation / discovery |
| --- | --- | --- | --- |
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `.agents/skills/keycrumb-sheets/` | `~/.agents/skills/keycrumb-sheets/` | Ask to use `$keycrumb-sheets`; check the skills picker |
| [Claude Code](https://code.claude.com/docs/en/skills) | `.claude/skills/keycrumb-sheets/` | `~/.claude/skills/keycrumb-sheets/` | `/keycrumb-sheets` or describe the sheet task |
| [Cursor](https://cursor.com/docs/skills) | `.cursor/skills/keycrumb-sheets/` | `~/.cursor/skills/keycrumb-sheets/` | Check Agent skills, then request the skill by name |
| [GitHub Copilot](https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/customize-cloud-agent/add-skills) | `.github/skills/keycrumb-sheets/` | `~/.copilot/skills/keycrumb-sheets/` | Ask the supported Copilot agent to use `keycrumb-sheets` |

These paths were checked against host documentation on 2026-10-23. Copilot's
supported local CLI/editor and cloud-agent surfaces also document `.agents/skills`
for project skills. For repository/cloud execution, commit the project skill
folder to the repository the agent uses; personal local installation does not
transfer automatically. Host/version support varies; this table is documentation
compatibility, not a claim that every host has been executed in testing.

Codex's built-in skill installer, when available, can install from repository
`keycrumb/homebrew-tap`, path `skills/keycrumb-sheets`, ref `skills-v0.1.0`. Ask:

```text
Use $skill-installer to install https://github.com/keycrumb/homebrew-tap/tree/skills-v0.1.0/skills/keycrumb-sheets
```

The plugin ZIP uses the [portable Agent Plugins format](https://developers.openai.com/plugins/build/plugins)
with root `plugin.json` and bundled `skills/`; it declares no MCP server, account,
hook or credentials. Import it only in a host that supports that package format
and exposes a ZIP/import flow. It is not a Claude Code plugin package. Marketplace
listing and universal host support are not claimed; manual skill installation
works independently of plugin import.

### Optional third-party installer

The [skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md)
requires Node.js/npm. Its [documented telemetry](https://www.skills.sh/docs/cli)
is enabled by default; `DISABLE_TELEMETRY=1` opts out. Run from your project folder,
review its prompts, and select project installation:

```sh
DISABLE_TELEMETRY=1 npx skills add https://github.com/keycrumb/homebrew-tap/tree/skills-v0.1.0/skills/keycrumb-sheets --skill keycrumb-sheets --agent codex
```

Use `claude-code`, `cursor` or `github-copilot` in place of `codex` for those hosts.
Add `--global` only when you explicitly want personal installation. The manual
ZIP route above needs neither Node nor this installer. The release-tag command
requires the published tag; it must not be used as proof of release availability.

### Use, update and remove

Restart or refresh the host's skill discovery after copying. If the skill is
missing, check that `SKILL.md` is exactly one folder below the host's `skills/`
directory and that the supporting folders came with it. Check the host's current
version/documentation if skills or ZIP import are unavailable; use the manual
folder route on a supported surface.

For an update, compare the new release and checksum, preserve local customizations
and replace only the installed `keycrumb-sheets` folder after reviewing conflicts.
For removal, remove that folder or uninstall through the same installer/plugin
manager used to install it. Generated library sheets remain separate.

Use the bundled [Markdown guide](skills/keycrumb-sheets/references/markdown.md),
[JSON format guide](skills/keycrumb-sheets/references/json-format.md),
[JSON schema](skills/keycrumb-sheets/references/keycrumb-sheet.schema.json) and
[example library](skills/keycrumb-sheets/assets/example-library). Copy both example
sheets and `icons/`/`images/` into a fresh folder, then select it in KeyCrumb. Images
resolve from that library's root. The optional Python validator checks structure
and icon files; format checks do not verify shortcut accuracy or native rendering.

### Maintaining skills releases

The [MIT license](skills/keycrumb-sheets/LICENSE.txt) covers the new skill, schema,
examples, artwork and validator. The KeyCrumb application remains proprietary.
The plugin manifest and packaging helper are also MIT licensed; see their
[license](LICENSE-skills.txt).

1. When the app format changes, update the schema, public guide, examples and
   provenance together. Compare the schema byte hash to its source and record
   the source commit in `format-provenance.json`. Keep private source and links
   outside this public repository; public CI uses only the bundled schema.
2. Use Python 3.11+ in an isolated environment. Install
   `skills/keycrumb-sheets/scripts/requirements.txt` and `PyYAML==6.0.3` for tests.
   Run `python3 -m unittest discover -s tests -v` and `git diff --check`.
3. Build with `python3 scripts/build_skills.py --version 0.1.0 --output-dir dist`.
   The version must match `plugin.json`. Archives use fixed timestamps, modes and
   an explicit resource allowlist. Extract them in empty directories and validate
   the moved example libraries. Recheck native rendering, image warnings, copy
   behavior, existing-file preservation and real host discovery/invocation.
4. Wait for **Skills checks** at the reviewed commit. Publish a reviewed
   `skills-v<VERSION>` tag through **Release agent skills**. Its shared verification
   runs before packaging; only its release job can write, and the release is
   marked non-latest. Cask checks remain scoped to actual cask/workflow changes.
5. Download the published archives anonymously, verify `SHA256SUMS`, extract and
   rerun validation. Check the tagged skill source and advertised install routes.
   Record actual host versions and distinguish file placement from invocation.
   Update download/install versions together. Do not infer release success from
   a local build or publish an app/cask release just for a skill change.
