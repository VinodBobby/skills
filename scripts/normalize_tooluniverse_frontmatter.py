#!/usr/bin/env python3
"""Keep known ToolUniverse descriptions with unquoted colons parseable as YAML."""

from pathlib import Path
import sys

SKILLS_WITH_PLAIN_SCALAR_COLONS = (
    "tooluniverse-fastq-qc",
    "tooluniverse-molecular-cloning",
    "tooluniverse-phewas",
)


def normalize(skill_root: Path) -> None:
    for name in SKILLS_WITH_PLAIN_SCALAR_COLONS:
        path = skill_root / name / "SKILL.md"
        if not path.is_file():
            raise SystemExit(f"Expected upstream skill is missing: {path}")
        lines = path.read_text().splitlines()
        if not lines or lines[0] != "---":
            raise SystemExit(f"Missing YAML frontmatter: {path}")
        try:
            end = lines.index("---", 1)
        except ValueError as error:
            raise SystemExit(f"Unclosed YAML frontmatter: {path}") from error

        description_index = next(
            (i for i, line in enumerate(lines[1:end], start=1)
             if line.startswith("description:")),
            None,
        )
        if description_index is None:
            raise SystemExit(f"Missing description field: {path}")

        value = lines[description_index][len("description:"):].strip()
        if value.startswith((">", "|", '"', "'")):
            continue
        lines[description_index:description_index + 1] = [
            "description: >-",
            f"  {value}",
        ]
        path.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("skills")
    normalize(root)
