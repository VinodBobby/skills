#!/usr/bin/env python3
"""Mirror an upstream skill catalog into skills/ and re-apply local overrides.

Each upstream lives in upstreams/<key>/ with:
  source.json     repository, skills_path, license, license_target
  SKILL_NAMES.txt mirrored skill names (written by sync)
  SOURCE_COMMIT   mirrored upstream revision (written by sync)
  local-overrides/ optional whole files copied over mirrored skills, re-applied after every sync
  overrides.json  optional targeted edits, applied after local-overrides/
  overlay-bases.json  sha256 of each upstream file a local override replaces; sync stops when
                      upstream changes one, so the override is reconciled instead of masking it

Usage:
  sync_upstream.py sync KEY SOURCE_ROOT SOURCE_COMMIT
  sync_upstream.py apply-overrides KEY
  sync_upstream.py record-bases KEY SOURCE_ROOT
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"


def upstream_dir(key: str) -> Path:
    path = REPO / "upstreams" / key
    if not (path / "source.json").is_file():
        raise ValueError(f"Unknown upstream: {key}")
    return path


def read_manifest(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    return {line.strip() for line in path.read_text().splitlines() if line.strip() and not line.startswith("#")}


def all_manifests_except(key: str) -> set[str]:
    names: set[str] = set()
    for manifest in (REPO / "upstreams").glob("*/SKILL_NAMES.txt"):
        if manifest.parent.name != key:
            names |= read_manifest(manifest)
    return names


def frontmatter_name(skill_md: Path) -> str:
    parts = skill_md.read_text().split("---", 2)
    if len(parts) != 3 or parts[0].strip():
        raise ValueError(f"Invalid YAML frontmatter: {skill_md}")
    match = re.search(r"^name:\s*(.*?)\s*$", parts[1], flags=re.MULTILINE)
    if not match:
        raise ValueError(f"Missing name field: {skill_md}")
    return match.group(1).strip().strip("\"'")


def sync(key: str, source_root: Path, source_commit: str) -> None:
    config_dir = upstream_dir(key)
    config = json.loads((config_dir / "source.json").read_text())
    source_skills = source_root / config["skills_path"]
    manifest = config_dir / "SKILL_NAMES.txt"
    names = sorted(p.name for p in source_skills.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    if not names:
        raise ValueError(f"No skill folders found in {source_skills}")

    for name in names:
        skill_dir = source_skills / name
        if any(p.is_symlink() for p in skill_dir.rglob("*")):
            raise ValueError(f"Symlink found in upstream skill: {skill_dir}")
        if frontmatter_name(skill_dir / "SKILL.md") != name:
            raise ValueError(f"Skill name does not match its folder: {skill_dir}")

    previous = read_manifest(manifest)
    removed = sorted(previous - set(names))
    if removed:
        raise ValueError("Upstream removed skill(s); review and remove them manually before syncing: " + ", ".join(removed))

    other_upstreams = all_manifests_except(key)
    collisions = sorted(
        n for n in names if n in other_upstreams or ((SKILLS / n).exists() and n not in previous)
    )
    if collisions:
        raise ValueError("Upstream skill name collides with existing skill(s): " + ", ".join(collisions))

    for name in names:
        shutil.rmtree(SKILLS / name, ignore_errors=True)
        shutil.copytree(source_skills / name, SKILLS / name)

    check_overlay_bases(key, source_skills)

    license_source = source_root / config["license"]
    if not license_source.is_file():
        raise ValueError(f"Upstream license is missing: {license_source}")
    license_target = REPO / config["license_target"]
    license_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(license_source, license_target)

    manifest.write_text("\n".join(names) + "\n")
    (config_dir / "SOURCE_COMMIT").write_text(source_commit + "\n")
    apply_overrides(key)
    print(f"Mirrored {len(names)} skills from {config['repository']} at {source_commit}.")


def split_frontmatter(text: str, path: Path) -> tuple[list[str], list[str]]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise ValueError(f"Missing YAML frontmatter: {path}")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError(f"Unclosed YAML frontmatter: {path}") from error
    return lines[: end + 1], lines[end + 1 :]


def field_span(front: list[str], field: str) -> tuple[int, int] | None:
    for i, line in enumerate(front[1:-1], start=1):
        if line.startswith(f"{field}:"):
            end = i + 1
            while end < len(front) - 1 and (front[end].startswith((" ", "\t")) or not front[end].strip()):
                end += 1
            return i, end
    return None


def set_field(path: Path, field: str, value: object) -> None:
    front, body = split_frontmatter(path.read_text(), path)
    rendered = f"{field}: {json.dumps(value, ensure_ascii=False)}"
    span = field_span(front, field)
    if span:
        front[span[0] : span[1]] = [rendered]
    else:
        front.insert(len(front) - 1, rendered)
    path.write_text("\n".join(front + body) + "\n")


def quote_field(path: Path, field: str) -> None:
    front, _ = split_frontmatter(path.read_text(), path)
    span = field_span(front, field)
    if not span:
        raise ValueError(f"Missing {field} field: {path}")
    raw = front[span[0]][len(field) + 1 :].strip()
    if raw.startswith(('"', "'", ">", "|")):
        return
    continuation = " ".join(line.strip() for line in front[span[0] + 1 : span[1]] if line.strip())
    set_field(path, field, f"{raw} {continuation}".strip())


def replace_text(path: Path, old: str, new: str) -> None:
    text = path.read_text()
    if old in text:
        path.write_text(text.replace(old, new))
    elif new not in text:
        raise ValueError(f"Override anchor not found; upstream changed {path}: {old[:80]!r}")


def rename(skill_dir: Path, source: str, target: str) -> None:
    src, dst = skill_dir / source, skill_dir / target
    if src.exists():
        if dst.exists():
            dst.unlink()
        src.rename(dst)
    elif not dst.exists():
        raise ValueError(f"Rename source missing: {src}")


def overlay_files(key: str) -> list[Path]:
    root = upstream_dir(key) / "local-overrides"
    if not root.is_dir():
        return []
    return sorted(p.relative_to(root) for p in root.rglob("*") if p.is_file() and p.name != ".DS_Store")


def file_hash(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def record_bases(key: str, source_root: Path) -> None:
    config = json.loads((upstream_dir(key) / "source.json").read_text())
    source_skills = source_root / config["skills_path"]
    bases = {str(rel): file_hash(source_skills / rel) for rel in overlay_files(key)}
    (upstream_dir(key) / "overlay-bases.json").write_text(json.dumps(bases, indent=2, sort_keys=True) + "\n")
    print(f"Recorded {len(bases)} overlay bases for {key}.")


def check_overlay_bases(key: str, source_skills: Path) -> None:
    bases_file = upstream_dir(key) / "overlay-bases.json"
    bases = json.loads(bases_file.read_text()) if bases_file.is_file() else {}
    changed = [str(rel) for rel in overlay_files(key) if file_hash(source_skills / rel) != bases.get(str(rel))]
    if changed:
        raise ValueError(
            "Upstream changed files that local overrides replace; reconcile them, then run record-bases: "
            + ", ".join(changed)
        )


def apply_overrides(key: str) -> None:
    overlay_root = upstream_dir(key) / "local-overrides"
    for rel in overlay_files(key):
        target = SKILLS / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(overlay_root / rel, target)

    overrides_file = upstream_dir(key) / "overrides.json"
    if not overrides_file.is_file():
        return
    for override in json.loads(overrides_file.read_text()):
        skill_dir = SKILLS / override["skill"]
        path = skill_dir / override.get("file", "SKILL.md")
        op = override["op"]
        if op == "set":
            set_field(path, override["field"], override["value"])
        elif op == "quote":
            quote_field(path, override["field"])
        elif op == "replace":
            replace_text(path, override["old"], override["new"])
        elif op == "rename":
            rename(skill_dir, override["from"], override["to"])
        elif op == "delete":
            if path.exists():
                path.unlink()
        elif op == "write":
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(override["content"])
        else:
            raise ValueError(f"Unknown override op: {op}")
    print(f"Applied overrides for {key}.")


def main(argv: list[str]) -> None:
    if len(argv) == 5 and argv[1] == "sync":
        sync(argv[2], Path(argv[3]), argv[4])
    elif len(argv) == 3 and argv[1] == "apply-overrides":
        apply_overrides(argv[2])
    elif len(argv) == 4 and argv[1] == "record-bases":
        record_bases(argv[2], Path(argv[3]))
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    try:
        main(sys.argv)
    except (OSError, ValueError) as error:
        raise SystemExit(str(error)) from error
