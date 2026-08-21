"""Parsing utilities for extracting [[wiki-links]] and metadata from Markdown notes."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

# Matches [[Note Title]] or [[Note Title|Display Text]]
LINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

# Matches a leading "# Title" heading
TITLE_PATTERN = re.compile(r"^#\s+(.+)$", re.MULTILINE)


@dataclass
class Note:
    """Represents a single parsed Markdown note."""

    path: Path
    slug: str
    title: str
    links: list[str] = field(default_factory=list)
    word_count: int = 0

    def __hash__(self) -> int:
        return hash(self.slug)


def slugify(name: str) -> str:
    """Normalize a note title or filename stem into a comparable slug.

    Hyphens and underscores are treated as word separators (equivalent to
    spaces) so that a file named `reading-list.md` matches a link written
    as `[[Reading List]]`.
    """
    normalized = re.sub(r"[-_]+", " ", name.strip())
    return re.sub(r"\s+", " ", normalized).lower()


def parse_note(path: Path) -> Note:
    """Read a single Markdown file and extract its title, links, and word count."""
    text = path.read_text(encoding="utf-8", errors="ignore")

    title_match = TITLE_PATTERN.search(text)
    title = title_match.group(1).strip() if title_match else path.stem

    links = [slugify(m.group(1)) for m in LINK_PATTERN.finditer(text)]
    word_count = len(text.split())

    return Note(
        path=path,
        slug=slugify(path.stem),
        title=title,
        links=links,
        word_count=word_count,
    )


def find_notes(root: Path) -> list[Note]:
    """Recursively find and parse all Markdown files under root."""
    md_files = sorted(root.rglob("*.md"))
    return [parse_note(p) for p in md_files]
