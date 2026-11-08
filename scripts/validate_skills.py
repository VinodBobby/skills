#!/usr/bin/env python3
"""Validate every skill package against the Agent Skills format and repo conventions.

Requires PyYAML. Exits non-zero when any error is found; warnings do not fail.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
MAX_DESCRIPTION = 1024
MAX_BODY_LINES = 500


def catalog_names() -> set[str]:
    names: set[str] = set()
    for pattern in ("*/SKILL_NAMES.txt", "*/LOCAL_SKILLS.txt"):
        for manifest in (REPO / "upstreams").glob(pattern):
            names |= {line.strip() for line in manifest.read_text().splitlines() if line.strip()}
    return names


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError("missing or unclosed YAML frontmatter")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError("frontmatter is not a mapping")
    return data, match.group(2)


def broken_links(md: Path, skill_dir: Path) -> list[str]:
    text = INLINE_CODE_RE.sub("", FENCE_RE.sub("", md.read_text()))
    broken = []
    for target in LINK_RE.findall(text):
        if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith(("#", "/", "<")):
            continue
        resolved = (md.parent / target.split("#", 1)[0]).resolve()
        inside_repo_skills = SKILLS.resolve() in resolved.parents
        if not inside_repo_skills or not resolved.exists():
            broken.append(target)
    return broken


def validate() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    catalog = catalog_names()
    first_party: list[str] = []

    for skill_dir in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        name = skill_dir.name
        skill_md = skill_dir / "SKILL.md"
        where = f"skills/{name}"
        if not skill_md.is_file():
            errors.append(f"{where}: missing SKILL.md")
            continue
        if name not in catalog:
            first_party.append(name)

        try:
            meta, body = parse_frontmatter(skill_md)
        except (ValueError, yaml.YAMLError) as error:
            errors.append(f"{where}/SKILL.md: {error}")
            continue

        if meta.get("name") != name:
            errors.append(f"{where}: name {meta.get('name')!r} does not match directory")
        if not NAME_RE.match(name) or len(name) > 64:
            errors.append(f"{where}: name must be lowercase hyphenated and at most 64 characters")
        description = meta.get("description")
        if not isinstance(description, str) or not description.strip():
            errors.append(f"{where}: description is missing")
        elif len(description) > MAX_DESCRIPTION:
            errors.append(f"{where}: description is {len(description)} characters (limit {MAX_DESCRIPTION})")
        if body.count("\n") > MAX_BODY_LINES:
            warnings.append(f"{where}: body is {body.count(chr(10))} lines; move detail into references/")

        for nested in skill_dir.rglob("SKILL.md"):
            if nested != skill_md:
                errors.append(f"{nested.relative_to(REPO)}: nested SKILL.md; a package must have one manifest")

        openai_yaml = skill_dir / "agents" / "openai.yaml"
        if openai_yaml.is_file():
            try:
                yaml.safe_load(openai_yaml.read_text())
            except yaml.YAMLError as error:
                errors.append(f"{openai_yaml.relative_to(REPO)}: {error}")

        for md in sorted(skill_dir.rglob("*.md")):
            for target in broken_links(md, skill_dir):
                errors.append(f"{md.relative_to(REPO)}: broken link {target}")

    readme = (REPO / "README.md").read_text()
    for name in first_party:
        if f"(skills/{name}/SKILL.md)" not in readme:
            errors.append(f"README.md: first-party skill {name} is not listed")
    for listed in re.findall(r"\(skills/([^/)]+)/SKILL\.md\)", readme):
        if not (SKILLS / listed / "SKILL.md").is_file():
            errors.append(f"README.md: lists missing skill {listed}")

    optional = REPO / "profiles" / "optional.txt"
    if optional.is_file():
        for line in optional.read_text().splitlines():
            if line.strip() and not line.startswith("#") and not (SKILLS / line.strip()).is_dir():
                errors.append(f"profiles/optional.txt: unknown skill {line.strip()}")

    for message in warnings:
        print(f"warning: {message}")
    for message in errors:
        print(f"error: {message}")
    print(f"Checked {sum(1 for p in SKILLS.iterdir() if p.is_dir())} skills: {len(errors)} errors, {len(warnings)} warnings.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(validate())
