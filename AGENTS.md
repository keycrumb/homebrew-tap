# KeyCrumb tap

This public repository owns only the Homebrew cask and its checks. The app is
distributed from `downloads.keycrumb.com`; app source and signing credentials do
not belong here.

- Track only published releases. Verify the immutable DMG against its checksum.
- Preserve Apple silicon and macOS 15+ requirements until wider support is verified.
- Keep Sparkle enabled and `auto_updates true`. Do not bypass Gatekeeper.
- Never delete preferences or user sheets during uninstall; do not add `zap` paths.
- Use Homebrew's cask DSL and tools; avoid custom release scripts or dependencies.
- Run `brew style --cask keycrumb/tap/keycrumb`,
  `brew audit --cask --online keycrumb/tap/keycrumb` and the installation workflow.
- Keep the README's installation and release-maintenance instructions accurate.
