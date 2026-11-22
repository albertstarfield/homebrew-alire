#!/usr/bin/env python3
"""Fetch Alire releases and render Formula/alr.rb when the SPARK check says go."""

from __future__ import annotations

import json
import re
import subprocess
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
FORMULA = ROOT / "Formula" / "alr.rb"
DECISION = ROOT / "main"
RELEASES = "https://api.github.com/repos/alire-project/alire/releases?per_page=10"

PATTERNS = {
    "linux_x86_64": "alr-{v}-bin-x86_64-linux.zip",
    "linux_aarch64": "alr-{v}-bin-aarch64-linux.zip",
    "macos_x86_64": "alr-{v}-bin-x86_64-macos.zip",
    "macos_aarch64": "alr-{v}-bin-aarch64-macos.zip",
}

TEMPLATE = '''class Alr < Formula
  desc "Ada and SPARK package manager"
  homepage "https://alire.ada.dev/"
  version "{version}"

  on_macos do
    on_arm do
      url "{macos_aarch64_url}"
      sha256 "{macos_aarch64_sha}"
    end
    on_intel do
      url "{macos_x86_64_url}"
      sha256 "{macos_x86_64_sha}"
    end
  end

  on_linux do
    on_arm do
      url "{linux_aarch64_url}"
      sha256 "{linux_aarch64_sha}"
    end
    on_intel do
      url "{linux_x86_64_url}"
      sha256 "{linux_x86_64_sha}"
    end
  end

  def install
    bin.install "bin/alr"
  end

  test do
    assert_match "alr", shell_output("#{{bin}}/alr --version")
  end
end
'''


def fetch_releases() -> list[dict[str, Any]]:
    request = urllib.request.Request(RELEASES, headers={"User-Agent": "AdaHomebrew/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.load(response)
    if not isinstance(payload, list):
        raise TypeError("release endpoint did not return a list")
    return [item for item in payload if isinstance(item, dict)]


def version_key(version: str) -> tuple[int, int, int]:
    parts = version.split(".")
    if len(parts) != 3:
        return (0, 0, 0)
    try:
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except ValueError:
        return (0, 0, 0)


def current_version() -> str:
    if not FORMULA.exists():
        return ""
    match = re.search(r'version "([^"]+)"', FORMULA.read_text(encoding="utf-8"))
    return match.group(1) if match else ""


def asset_map(release: dict[str, Any]) -> dict[str, dict[str, Any]]:
    assets = release.get("assets", [])
    if not isinstance(assets, list):
        return {}
    return {str(a.get("name")): a for a in assets if isinstance(a, dict)}


def ask_decision(newer: bool, assets: dict[str, dict[str, Any]]) -> str:
    present = {name: name in assets for name in PATTERNS}
    facts = (
        "newer={newer}\n"
        "token=1\n"
        "linux_x86_64={linux_x86_64}\n"
        "linux_aarch64={linux_aarch64}\n"
        "macos_x86_64={macos_x86_64}\n"
        "macos_aarch64={macos_aarch64}\n"
    ).format(newer=int(newer), **{k: int(v) for k, v in present.items()})
    result = subprocess.run(
        [str(DECISION)], input=facts, text=True, capture_output=True, check=True
    )
    return result.stdout.strip()


def render(version: str, assets: dict[str, dict[str, Any]]) -> str:
    values: dict[str, str] = {"version": version}
    for key, pattern in PATTERNS.items():
        name = pattern.format(v=version)
        asset = assets[name]
        values[f"{key}_url"] = str(asset["browser_download_url"])
        digest = str(asset.get("digest", ""))
        values[f"{key}_sha"] = digest.removeprefix("sha256:")
    return TEMPLATE.format(**values)


def main() -> int:
    releases = fetch_releases()
    stable = [
        r
        for r in releases
        if re.fullmatch(r"v\d+\.\d+\.\d+", str(r.get("tag_name", "")))
        and not bool(r.get("prerelease", False))
    ]
    if not stable:
        print("no stable Alire release found")
        return 1
    latest = max(stable, key=lambda r: version_key(str(r["tag_name"])[1:]))
    version = str(latest["tag_name"])[1:]
    current = current_version()
    assets = asset_map(latest)
    missing = [p.format(v=version) for p in PATTERNS.values() if p.format(v=version) not in assets]
    decision = ask_decision(newer=version != current, assets=assets)
    if missing:
        print(f"missing assets: {', '.join(missing)}")
    if decision != "NONE":
        print(f"no update: {decision} (current={current or 'none'}, latest={version})")
        return 0
    FORMULA.write_text(render(version, assets), encoding="utf-8")
    print(f"updated Formula/alr.rb to {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
