"""Repository-level checks for Agent Skills metadata and local Markdown links.

The official skills-ref CLI validates the Agent Skills format. This script adds
repository-specific checks without requiring third-party Python dependencies.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
SKILLS_ROOT = ROOT / "skills"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")


def fail(message: str) -> None:
    print(f"::error::{message}")
    raise SystemExit(1)


def skill_directories() -> list[Path]:
    if not SKILLS_ROOT.is_dir():
        fail("The repository must contain a skills/ directory.")
    directories = sorted(path.parent for path in SKILLS_ROOT.rglob("SKILL.md"))
    if not directories:
        fail("No SKILL.md files were found under skills/.")
    return directories


def validate_skill_metadata(skill_dir: Path) -> None:
    skill_file = skill_dir / "SKILL.md"
    content = skill_file.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        fail(f"{skill_file.relative_to(ROOT)} must start with YAML frontmatter.")
    parts = content.split("---", 2)
    if len(parts) != 3 or parts[0] != "":
        fail(f"{skill_file.relative_to(ROOT)} has an unclosed YAML frontmatter block.")
    frontmatter = parts[1]
    name_match = re.search(r"^name:\s*([^\n#]+)\s*$", frontmatter, re.MULTILINE)
    description_match = re.search(
        r"^description:\s*(.+?)\s*$", frontmatter, re.MULTILINE
    )
    if not name_match or not description_match:
        fail(
            f"{skill_file.relative_to(ROOT)} requires non-empty name and description fields."
        )
    name = name_match.group(1).strip().strip("'\"")
    description = description_match.group(1).strip().strip("'\"")
    if len(name) > 64 or not NAME_PATTERN.fullmatch(name):
        fail(f"Invalid skill name in {skill_file.relative_to(ROOT)}: {name!r}")
    if name != skill_dir.name:
        fail(f"Skill name {name!r} must match directory {skill_dir.name!r}.")
    if not description or len(description) > 1024:
        fail(
            f"Description in {skill_file.relative_to(ROOT)} must be 1-1024 characters."
        )
    print(f"PASS metadata: {skill_file.relative_to(ROOT)}")


def validate_markdown_links() -> None:
    markdown_files = sorted(
        path for path in ROOT.rglob("*.md") if ".git" not in path.parts
    )
    broken: list[str] = []
    for markdown_file in markdown_files:
        content = markdown_file.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(content):
            destination = match.group(1).strip()
            if not destination:
                continue
            raw_target = destination.split(maxsplit=1)[0].strip("<>")
            parsed = urlsplit(raw_target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            target = (markdown_file.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                broken.append(
                    f"{markdown_file.relative_to(ROOT)} -> {raw_target}"
                )
    if broken:
        fail("Broken local Markdown links:\n" + "\n".join(broken))
    print(f"PASS local Markdown links: {len(markdown_files)} files scanned")


def main() -> int:
    directories = skill_directories()
    for skill_dir in directories:
        validate_skill_metadata(skill_dir)
    validate_markdown_links()
    print(f"SUCCESS: repository checks passed for {len(directories)} skill(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
