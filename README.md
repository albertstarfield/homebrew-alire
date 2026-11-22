# Alire tap

This tap ships `alr`, the Alire package manager for Ada and SPARK, as a Homebrew formula. The formula points at the binaries that the Alire project builds for Linux and macOS, so Homebrew installs a ready-made executable rather than building Alire from source.

## Add the tap

```
brew tap <you>/alire
```

Homebrew shortens `homebrew-alire` to `alire` in tap commands. If you are working from a local checkout instead, use `brew tap <you>/alire ./Alire`.

## Install

```
brew install alr
```

Once the tap is added, the short name is enough. To be explicit about where the formula comes from:

```
brew install <you>/alire/alr
```

The formula picks the zip for your OS and CPU: `alr-2.1.1-bin-x86_64-linux.zip`, `alr-2.1.1-bin-aarch64-linux.zip`, `alr-2.1.1-bin-x86_64-macos.zip`, `alr-2.1.1-bin-aarch64-macos.zip` or `alr-2.1.1-bin-universal-macos.zip`. Each zip contains `bin/alr` and `LICENSE.txt`. Version and digests come from the upstream GitHub release, stored under `evidence/alire-releases.json`.

Check the install with:

```
alr --version
```

## Upgrade

```
brew update
brew upgrade alr
```

A daily GitHub Actions workflow checks the upstream release feed. When the release tag changes and all four platform assets are present, it opens a pull request with the new version and SHA-256 values. The release-check decision lives in the SPARK package `src/updater.ads`; `src/main.adb` only reads the facts on stdin. No pull request is opened when the tag is unchanged, the token is invalid, or one of the platform assets is missing.

To inspect the decision locally:

```
gprbuild -P updater.gpr
gnatprove --mode=all --level=4 -j0 -P updater.gpr
```

## Remove

```
brew uninstall alr
brew untap <you>/alire
```

## Layout

- `Formula/alr.rb` - the installable formula
- `src/updater.ads`, `src/updater.adb` - SPARK release-readiness logic
- `src/main.adb` - stdin/stdout boundary
- `scripts/update_alr.py` - fetches releases and renders the formula
- `.github/workflows/update.yml` - daily check
- `.github/workflows/ci.yml` - style and audit on pushes and pull requests
- `evidence/` - raw release JSON and the copied Homebrew documentation

Replace `<you>` with your GitHub owner or organisation name before publishing.
