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
app matches the cask's release. Homebrew refuses to adopt a different build;
do not use `--force` to replace a newer app with an older alpha.

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
