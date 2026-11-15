#!/usr/bin/env python3
"""Report static context-cost and overlap signals for skills in this repository."""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import defaultdict
from pathlib import Path

STOPWORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "into", "is", "it",
    "of", "on", "or", "the", "to", "use", "when", "with",
}


def frontmatter(text: str) -> tuple[str, str, bool]:
    """Return name, description, and declared explicit-only status."""
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not match:
        return "", "", False

    lines = match.group(1).splitlines()
    name = ""
    description = ""
    explicit_only = False
    for i, line in enumerate(lines):
        name_match = re.match(r"^name:\s*(.*?)\s*$", line)
        if name_match:
            name = name_match.group(1).strip("\"'")
        if re.match(r"^disable-model-invocation:\s*true\s*$", line):
            explicit_only = True
        desc_match = re.match(r"^description:\s*(.*)$", line)
        if desc_match:
            value = desc_match.group(1).strip()
            if value in {">", "|-", "|", ">-", ">+", "|+"}:
                parts = []
                for continuation in lines[i + 1 :]:
                    if continuation and not continuation[0].isspace():
                        break
                    if continuation.strip():
                        parts.append(continuation.strip())
                description = " ".join(parts)
            else:
                description = value.strip("\"'")

    body = match.group(2)
    return name, description, explicit_only


def estimate_tokens(text: str) -> int:
    """Use a rough four-characters-per-token estimate; no tokenizer dependency."""
    return math.ceil(len(text) / 4)


def catalog_names(root: Path) -> set[str]:
    names: set[str] = set()
    upstreams = root / "upstreams"
    if not upstreams.is_dir():
        return names
    for manifest in upstreams.glob("*/SKILL_NAMES.txt"):
        names.update(line.strip() for line in manifest.read_text().splitlines() if line.strip() and not line.startswith("#"))
    for manifest in upstreams.glob("*/LOCAL_SKILLS.txt"):
        names.update(line.strip() for line in manifest.read_text().splitlines() if line.strip() and not line.startswith("#"))
    return names


def install_profiles(root: Path, entries: list[dict]) -> dict[str, list[dict]]:
    optional_file = root / "profiles" / "optional.txt"
    optional = (
        {
            line.strip()
            for line in optional_file.read_text().splitlines()
            if line.strip() and not line.startswith("#")
        }
        if optional_file.is_file()
        else set()
    )
    default_catalogs: set[str] = set()
    for config_file in (root / "upstreams").glob("*/source.json"):
        config = json.loads(config_file.read_text())
        if config.get("install_profile") == "science":
            continue
        for manifest_name in ("SKILL_NAMES.txt", "LOCAL_SKILLS.txt"):
            manifest = config_file.parent / manifest_name
            if manifest.is_file():
                default_catalogs.update(
                    line.strip()
                    for line in manifest.read_text().splitlines()
                    if line.strip() and not line.startswith("#")
                )
    default = [
        entry
        for entry in entries
        if (entry["catalog"] and entry["name"] in default_catalogs)
        or (not entry["catalog"] and entry["name"] not in optional)
    ]
    return {"default": default, "all": entries}


def repeated_sentences(name: str, body: str, index: dict[str, set[str]]) -> None:
    body = re.sub(r"```.*?```|~~~.*?~~~", " ", body, flags=re.DOTALL)
    body = re.sub(r"`[^`]*`", " ", body)
    body = re.sub(r"\[[^\]]+\]\([^)]+\)", " ", body)
    for sentence in re.findall(r"[^.!?]+[.!?]", body):
        sentence = re.sub(r"^\s*(?:[-*+]\s+|\d+[.)]\s+)", "", sentence).strip()
        normalized = re.sub(r"\s+", " ", sentence).lower()
        if 60 <= len(normalized) <= 280 and not normalized.startswith("#"):
            index[normalized].add(name)


def similar_descriptions(entries: list[dict]) -> list[tuple[float, dict, dict]]:
    candidates = []
    for index, left in enumerate(entries):
        left_words = set(re.findall(r"[a-z0-9]+", left["description"].lower())) - STOPWORDS
        if len(left_words) < 5:
            continue
        for right in entries[index + 1 :]:
            right_words = set(re.findall(r"[a-z0-9]+", right["description"].lower())) - STOPWORDS
            if len(right_words) < 5:
                continue
            shared = left_words & right_words
            score = len(shared) / len(left_words | right_words)
            if len(shared) >= 5 and score >= 0.35:
                candidates.append((score, left, right))
    return sorted(candidates, key=lambda item: item[0], reverse=True)


def unlinked_markdown(root: Path) -> list[str]:
    candidates = []
    for skill_dir in sorted(path for path in (root / "skills").iterdir() if path.is_dir()):
        markdown = list(skill_dir.glob("*.md"))
        references = skill_dir / "references"
        if references.is_dir():
            markdown.extend(references.rglob("*.md"))
        markdown = [path for path in markdown if path.name not in {"SKILL.md", "UPSTREAM.md"}]
        linked: set[Path] = set()
        sources = markdown + [skill_dir / "SKILL.md"]
        source_text = {}
        for source in sources:
            if not source.is_file():
                continue
            text = source.read_text(errors="replace")
            source_text[source] = text.lower()
            text = re.sub(r"```.*?```|~~~.*?~~~", " ", text, flags=re.DOTALL)
            for target in re.findall(r"(?<!!)\[[^\]]*\]\(([^)\s]+)", text):
                if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith(("#", "/")):
                    continue
                resolved = (source.parent / target.split("#", 1)[0]).resolve()
                if skill_dir.resolve() in resolved.parents and resolved.is_file():
                    linked.add(resolved)
        for path in markdown:
            relative = path.relative_to(skill_dir).as_posix().lower()
            basename = path.name.lower()
            if path.resolve() in linked:
                continue
            if any(source != path and (relative in text or basename in text) for source, text in source_text.items()):
                continue
            candidates.append(path.relative_to(root).as_posix())
    return candidates


def collect(root: Path) -> tuple[list[dict], dict[str, set[str]]]:
    catalog = catalog_names(root)
    entries = []
    repeated: dict[str, set[str]] = defaultdict(set)
    for skill_md in sorted((root / "skills").glob("*/SKILL.md")):
        text = skill_md.read_text(errors="replace")
        match = re.match(r"^---\n.*?\n---\n?(.*)$", text, re.DOTALL)
        body = match.group(1) if match else text
        name, description, explicit_only = frontmatter(text)
        openai = skill_md.parent / "agents" / "openai.yaml"
        if openai.is_file() and re.search(r"^\s*allow_implicit_invocation:\s*false\s*$", openai.read_text(), re.MULTILINE):
            explicit_only = True
        entries.append(
            {
                "name": name or skill_md.parent.name,
                "catalog": skill_md.parent.name in catalog,
                "description": description,
                "description_chars": len(description),
                "description_tokens": estimate_tokens(description),
                "body": body,
                "body_chars": len(body),
                "body_tokens": estimate_tokens(body),
                "body_lines": len(body.splitlines()),
                "host_skill_calls": len(re.findall(r"\bSkill\s*\(\s*skill\s*=", body)),
                "explicit_only": explicit_only,
                "path": skill_md.relative_to(root).as_posix(),
            }
        )
        repeated_sentences(skill_md.parent.name, body, repeated)
    return entries, repeated


def render(root: Path) -> str:
    entries, repeated = collect(root)
    first_party = [entry for entry in entries if not entry["catalog"]]
    catalog = [entry for entry in entries if entry["catalog"]]
    profiles = install_profiles(root, entries)
    unlinked = unlinked_markdown(root)
    description_chars = sum(entry["description_chars"] for entry in entries)
    description_tokens = sum(entry["description_tokens"] for entry in entries)
    body_chars = sum(entry["body_chars"] for entry in entries)
    body_tokens = sum(entry["body_tokens"] for entry in entries)

    lines = [
        "# Skill Doctor: static inventory",
        "",
        f"Skills: **{len(entries)}** total ({len(first_party)} repository-managed, {len(catalog)} catalog).",
        f"All skill descriptions: **{description_chars:,} characters**, roughly **{description_tokens:,} tokens**; **{sum(entry['explicit_only'] for entry in entries)}** skills are marked explicit-only.",
        f"Entrypoint bodies: **{body_chars:,} characters**, roughly **{body_tokens:,} tokens** if every skill were loaded.",
        f"Host-specific `Skill(skill=...)` calls: **{sum(entry['host_skill_calls'] for entry in entries)}**.",
        f"Explicit-only declarations found: **{sum(entry['explicit_only'] for entry in entries)}**.",
        "",
        "Token counts use a four-character estimate. Hosts load skill descriptions and bodies differently; references are excluded. This report measures static size, not observed usage or outcome quality.",
    ]
    lines.extend(
        [
            "",
            "## Install-profile discovery cost",
            "",
            "| Profile | Skills | Implicit skills | Implicit description chars | Rough tokens | Explicit-only skills |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for profile, selected in profiles.items():
        implicit = [entry for entry in selected if not entry["explicit_only"]]
        chars = sum(entry["description_chars"] for entry in implicit)
        tokens = sum(entry["description_tokens"] for entry in implicit)
        explicit_only = len(selected) - len(implicit)
        lines.append(f"| `{profile}` | {len(selected)} | {len(implicit)} | {chars:,} | {tokens:,} | {explicit_only} |")
    lines.extend(
        [
            "",
            "Estimates assume a host loads every implicitly invocable description and none marked explicit-only. Confirm host behavior before treating them as actual prompt cost.",
            "",
            "## Largest descriptions",
            "",
            "| Skill | Characters | Rough tokens |",
            "| --- | ---: | ---: |",
        ]
    )
    for entry in sorted(entries, key=lambda item: item["description_chars"], reverse=True)[:10]:
        lines.append(f"| `{entry['name']}` | {entry['description_chars']} | {entry['description_tokens']} |")

    lines.extend(["", "## Largest entrypoints", "", "| Skill | Lines | Characters | Rough tokens |", "| --- | ---: | ---: | ---: |"])
    for entry in sorted(entries, key=lambda item: item["body_chars"], reverse=True)[:10]:
        lines.append(f"| `{entry['name']}` | {entry['body_lines']} | {entry['body_chars']} | {entry['body_tokens']} |")

    host_calls = [entry for entry in entries if entry["host_skill_calls"]]
    lines.extend(["", "## Host-specific skill calls", ""])
    if host_calls:
        lines.extend(["| Skill | Calls |", "| --- | ---: |"])
        for entry in sorted(host_calls, key=lambda item: item["host_skill_calls"], reverse=True)[:10]:
            lines.append(f"| `{entry['name']}` | {entry['host_skill_calls']} |")
    else:
        lines.append("No `Skill(skill=...)` calls found.")

    lines.extend(["", "## Unlinked Markdown candidates", ""])
    if unlinked:
        lines.append(f"{len(unlinked)} root or reference Markdown files are not linked or mentioned elsewhere in their skill package; confirm whether each is still needed.")
        lines.extend(["", "| File |", "| --- |"])
        lines.extend(f"| `{path}` |" for path in unlinked[:12])
        if len(unlinked) > 12:
            lines.append(f"| ... and {len(unlinked) - 12} more |")
    else:
        lines.append("All package Markdown files are linked from another file or are entrypoints.")

    duplicates = [(sentence, names) for sentence, names in repeated.items() if len(names) >= 3]
    lines.extend(["", "## Repeated instruction candidates", ""])
    if duplicates:
        lines.append("Exact prose appearing in three or more skills; inspect before editing because shared wording can still express required constraints.")
        lines.extend(["", "| Skills | Repeated text |", "| --- | --- |"])
        for sentence, names in sorted(duplicates, key=lambda item: (-len(item[1]), item[0]))[:12]:
            excerpt = sentence.replace("|", "\\|")
            if len(excerpt) > 180:
                excerpt = excerpt[:177] + "..."
            ordered = sorted(names)
            sample = ", ".join(f"`{name}`" for name in ordered[:5])
            if len(ordered) > 5:
                sample += f", and {len(ordered) - 5} more"
            lines.append(f"| {len(names)} skills: {sample} | {excerpt} |")
        if len(duplicates) > 12:
            lines.append(f"| ... | {len(duplicates) - 12} additional repeated sentences omitted |")
    else:
        lines.append("No exact sentence repeats across three or more skills.")

    similar = similar_descriptions(entries)
    lines.extend(["", "## Similar description candidates", ""])
    if similar:
        lines.append("Word overlap is only a routing-review signal; similar wording does not prove the workflows are redundant.")
        lines.extend(["", "| Similarity | Skills | Shared terms |", "| ---: | --- | --- |"])
        for score, left, right in similar[:8]:
            left_words = set(re.findall(r"[a-z0-9]+", left["description"].lower())) - STOPWORDS
            right_words = set(re.findall(r"[a-z0-9]+", right["description"].lower())) - STOPWORDS
            shared = sorted(left_words & right_words)
            terms = ", ".join(shared[:8])
            lines.append(f"| {score:.2f} | `{left['name']}` / `{right['name']}` | {terms} |")
        if len(similar) > 8:
            lines.append(f"| ... | {len(similar) - 8} additional pairs omitted |")
    else:
        lines.append("No description pairs passed the lexical-overlap threshold.")

    lines.extend(
        [
            "",
            "## Review rule",
            "",
            "Use this inventory to choose candidates. Keep, tighten, merge, or retire only after checking the skill's unique behavior, install profile, references, source ownership, and available outcome evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3], help="Repository root")
    parser.add_argument("--output", type=Path, help="Write Markdown report to this path instead of stdout")
    args = parser.parse_args()
    report = render(args.root.resolve())
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report)
    else:
        print(report)


if __name__ == "__main__":
    main()
