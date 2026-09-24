#!/usr/bin/env python3
"""Safely mirror the upstream ToolUniverse skills into this repository."""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path


def read_manifest(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    return {
        line.strip()
        for line in path.read_text().splitlines()
        if line.strip() and not line.startswith("#")
    }


def frontmatter_name(skill_md: Path) -> str:
    text = skill_md.read_text()
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"Invalid YAML frontmatter: {skill_md}")
    match = re.search(r"^name:\s*(.*?)\s*$", parts[1], flags=re.MULTILINE)
    if not match:
        raise ValueError(f"Missing name field: {skill_md}")
    return match.group(1).strip().strip("\"'")


def sync(source_root: Path, repo_root: Path, source_commit: str) -> None:
    source_skills = source_root / "skills"
    destination_skills = repo_root / "skills"
    manifest = repo_root / "upstreams" / "harvard-tooluniverse" / "SKILL_NAMES.txt"
    names = sorted(
        path.name
        for path in source_skills.iterdir()
        if path.is_dir() and (path / "SKILL.md").is_file()
    )
    if not names:
        raise ValueError(f"No skill folders found in {source_skills}")

    for name in names:
        skill_dir = source_skills / name
        if any(path.is_symlink() for path in skill_dir.rglob("*")):
            raise ValueError(f"Symlink found in upstream skill: {skill_dir}")
        if frontmatter_name(skill_dir / "SKILL.md") != name:
            raise ValueError(f"Skill name does not match its folder: {skill_dir}")

    previous = read_manifest(manifest)
    removed = sorted(previous - set(names))
    if removed:
        raise ValueError(
            "Upstream removed skill(s); review and remove them manually before syncing: "
            + ", ".join(removed)
        )

    collisions = sorted(
        name
        for name in names
        if (destination_skills / name).exists() and name not in previous
    )
    if collisions:
        raise ValueError("Upstream skill name collides with local skill(s): " + ", ".join(collisions))

    for name in names:
        shutil.copytree(source_skills / name, destination_skills / name, dirs_exist_ok=True)

    license_source = source_root / "LICENSE"
    if not license_source.is_file():
        raise ValueError(f"Upstream license is missing: {license_source}")
    license_target = repo_root / "third-party-licenses" / "harvard-tooluniverse-LICENSE.txt"
    license_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(license_source, license_target)

    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("\n".join(names) + "\n")
    (manifest.parent / "SOURCE_COMMIT").write_text(source_commit + "\n")

    sys.path.insert(0, str(repo_root / "scripts"))
    from normalize_tooluniverse_frontmatter import normalize

    normalize(destination_skills)
    print(f"Mirrored {len(names)} skills from ToolUniverse {source_commit}.")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: sync_tooluniverse_catalog.py SOURCE_ROOT REPO_ROOT SOURCE_COMMIT")
    try:
        sync(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3])
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
