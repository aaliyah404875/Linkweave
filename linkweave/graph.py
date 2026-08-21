"""Build a link graph from parsed notes and compute useful statistics over it."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .parser import Note


@dataclass
class GraphStats:
    total_notes: int
    total_links: int
    broken_links: list[tuple[str, str]]  # (source_slug, target_slug)
    orphan_notes: list[str]  # notes with zero inbound links
    most_linked: list[tuple[str, int]]  # (slug, inbound_count), sorted desc


class LinkGraph:
    """A directed graph of notes connected by [[wiki-links]]."""

    def __init__(self, notes: list[Note]):
        self.notes: dict[str, Note] = {n.slug: n for n in notes}
        self.outbound: dict[str, list[str]] = defaultdict(list)
        self.inbound: dict[str, list[str]] = defaultdict(list)
        self._build()

    def _build(self) -> None:
        for note in self.notes.values():
            for target in note.links:
                self.outbound[note.slug].append(target)
                self.inbound[target].append(note.slug)

    def stats(self) -> GraphStats:
        total_links = sum(len(v) for v in self.outbound.values())

        broken = [
            (src, tgt)
            for src, targets in self.outbound.items()
            for tgt in targets
            if tgt not in self.notes
        ]

        orphans = [
            slug for slug in self.notes if len(self.inbound.get(slug, [])) == 0
        ]

        most_linked = sorted(
            ((slug, len(inbound)) for slug, inbound in self.inbound.items() if slug in self.notes),
            key=lambda pair: pair[1],
            reverse=True,
        )

        return GraphStats(
            total_notes=len(self.notes),
            total_links=total_links,
            broken_links=broken,
            orphan_notes=sorted(orphans),
            most_linked=most_linked[:10],
        )

    def to_dot(self) -> str:
        """Export the graph as Graphviz DOT format for visualization."""
        lines = ["digraph linkweave {", '  rankdir="LR";', "  node [shape=box, style=rounded];"]
        for slug, note in self.notes.items():
            label = note.title.replace('"', "'")
            lines.append(f'  "{slug}" [label="{label}"];')
        for src, targets in self.outbound.items():
            for tgt in targets:
                if tgt in self.notes:
                    lines.append(f'  "{src}" -> "{tgt}";')
        lines.append("}")
        return "\n".join(lines)
