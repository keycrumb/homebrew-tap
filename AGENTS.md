# KeyCrumb tap

This public repository owns the Homebrew cask, its checks, and the portable
`skills/keycrumb-sheets` authoring skill and skills-only plugin. The app is
distributed from `downloads.keycrumb.com`; app source and signing credentials do
not belong here.

- Track only published releases. Verify the immutable DMG against its checksum.
- Preserve Apple silicon and macOS 15+ requirements until wider support is verified.
- Keep Sparkle enabled and `auto_updates true`. Do not bypass Gatekeeper.
- Never delete preferences or user sheets during uninstall; do not add `zap` paths.
- Use Homebrew's cask DSL and tools; avoid custom cask release scripts or dependencies.
- Run `brew style --cask keycrumb/tap/keycrumb`,
  `brew audit --cask --online keycrumb/tap/keycrumb` and the installation workflow.
- Keep the README's installation and release-maintenance instructions accurate.

## Agent skills

- Keep the skill independently usable offline with bundled references and examples.
- Keep MIT licensing scoped to new skill/schema/examples/validator material; the app remains proprietary.
- Never include private source links, personal paths, app source or credentials.
- Update the schema, provenance hash, format guide and examples together. Public CI must not depend on a private repository.
- Run the skills tests and deterministic packaging checks from the README before a skills release.
- Skills tags use `skills-v<VERSION>` independently of the cask/app. Do not change the cask for a skills-only release.
