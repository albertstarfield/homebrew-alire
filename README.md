# Alire tap

This tap is maintained by `albertstarfield` as a redistribution convenience. The upstream owner is `alire-project/alire`; the binaries here are the release assets that project builds for Linux and macOS. Homebrew installs a ready-made executable rather than building Alire from source.

## One-line install

```
brew tap albertstarfield/alire && brew install alr
```

## Add the tap

```
brew tap albertstarfield/alire
```

Homebrew shortens `homebrew-alire` to `alire` in tap commands. If you are working from a local checkout instead, use `brew tap albertstarfield/alire ./Alire`.

## Install

```
brew install alr
```

Once the tap is added, the short name is enough. To be explicit about where the formula comes from:

```
brew install albertstarfield/alire/alr
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
brew untap albertstarfield/alire
```

## FAQ

**Why does Homebrew say the tap is untrusted?**

`brew tap` adds the files, but Homebrew will not load formulae from a new tap until you trust it. Run `brew trust albertstarfield/alire` (or `brew trust albertstarfield/gnatstudio`) and try again.

**Why does `brew audit Formula/alr.rb` fail with "Calling brew audit [path ...] is disabled"?**

Newer Homebrew versions want a token, not a path. Tap the checkout, trust it, then audit by name: `brew audit --strict --online albertstarfield/alire/alr`. The CI workflow does exactly that.

**Why does the daily job fail with HTTP 403 "rate limit exceeded"?**

The GitHub release API rejects unauthenticated calls when runners share an IP. The workflow passes `GH_TOKEN` to the Python script, which sends it as a bearer token. If you run the script by hand, export `GH_TOKEN` first.

**Why did no pull request appear after a release?**

The SPARK check refuses half-complete releases. Look at the job log for `NO_NEW_VERSION`, `MISSING_LINUX_AARCH64`, `MISSING_LINUX_X86_64` or `MISSING_MACOS_DMG`. A DMG that SourceForge has not published yet gives `MISSING_MACOS_DMG`.

**Why did the scheduled workflow stop running?**

GitHub disables schedules in public repos after 60 days without activity, and can delay runs near the top of the hour. Both workflows use an off-hour cron time. A small commit or `workflow_dispatch` run reactivates the schedule.

**Why does `brew install --cask gnatstudio` say cask conflicts exist?**

Another tap may already define a cask with the same name. Uninstall it first, then install from this tap explicitly: `brew uninstall --cask gnatstudio && brew install --cask albertstarfield/gnatstudio/gnatstudio`.

**Why does the formula version look doubled in `brew info`?**

Homebrew derives the formula version from the URL. The updater keeps `# updater-version:` as a comment so it can detect changes without triggering the "version is redundant" audit error. Do not turn that comment back into a `version` stanza.

**Why does `alr --version` still use `/usr/local/bin/alr`?**

Homebrew found another `alr` earlier in your `PATH`. The installed copy is `/opt/homebrew/bin/alr`; run that path directly, or remove the older `/usr/local/bin/alr` if you want the Homebrew one to win. Check with `which alr`.

**Why does `gprbuild` fail in a fresh CI job?**

The Ubuntu runner starts without Ada tools. The workflow installs both `gnat` and `gprbuild`. Install both locally if you want to run the decision binary before pushing.

## Upstream owner

The tap owner is `albertstarfield`. That is just the Homebrew channel. The software owner is `alire-project/alire`, whose release assets are listed in `evidence/alire-releases.json`. This tap redistributes those assets; it does not build or sign them.

## Layout

- `Formula/alr.rb` - the installable formula
- `src/updater.ads`, `src/updater.adb` - SPARK release-readiness logic
- `src/main.adb` - stdin/stdout boundary
- `scripts/update_alr.py` - fetches releases and renders the formula
- `.github/workflows/update.yml` - daily check
- `.github/workflows/ci.yml` - style and audit on pushes and pull requests
- `evidence/` - raw release JSON and the copied Homebrew documentation

The owner is `albertstarfield`.
