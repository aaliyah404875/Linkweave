"""Command-line interface for linkweave."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .graph import LinkGraph
from .parser import find_notes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="linkweave",
        description="Build and inspect a link graph from a folder of Markdown notes.",
    )
    parser.add_argument("path", type=Path, help="Path to a folder of .md notes")
    parser.add_argument(
        "--dot",
        type=Path,
        default=None,
        help="Write a Graphviz .dot export of the graph to this path",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Number of most-linked notes to display (default: 10)",
    )
    return parser


def run(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if not args.path.exists() or not args.path.is_dir():
        print(f"error: '{args.path}' is not a directory", file=sys.stderr)
        return 1

    notes = find_notes(args.path)
    if not notes:
        print(f"No Markdown notes found under {args.path}")
        return 0

    graph = LinkGraph(notes)
    stats = graph.stats()

    print(f"Linkweave report for: {args.path}\n")
    print(f"  Notes scanned:   {stats.total_notes}")
    print(f"  Links found:     {stats.total_links}")
    print(f"  Broken links:    {len(stats.broken_links)}")
    print(f"  Orphan notes:    {len(stats.orphan_notes)}")

    if stats.most_linked:
        print(f"\nMost-linked notes (top {args.top}):")
        for slug, count in stats.most_linked[: args.top]:
            title = graph.notes[slug].title
            print(f"  {count:>3}  {title}  ({slug})")

    if stats.orphan_notes:
        print("\nOrphan notes (no inbound links):")
        for slug in stats.orphan_notes:
            print(f"  - {graph.notes[slug].title}  ({slug})")

    if stats.broken_links:
        print("\nBroken links (target note not found):")
        for src, tgt in stats.broken_links:
            src_title = graph.notes[src].title
            print(f"  - {src_title} -> [[{tgt}]]")

    if args.dot:
        args.dot.write_text(graph.to_dot(), encoding="utf-8")
        print(f"\nGraphviz export written to {args.dot}")

    return 0


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
