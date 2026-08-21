from linkweave.graph import LinkGraph
from linkweave.parser import Note
from pathlib import Path


def make_note(slug: str, title: str, links: list[str]) -> Note:
    return Note(path=Path(f"{slug}.md"), slug=slug, title=title, links=links, word_count=10)


def test_stats_counts_notes_and_links():
    notes = [
        make_note("a", "A", ["b", "c"]),
        make_note("b", "B", ["c"]),
        make_note("c", "C", []),
    ]
    graph = LinkGraph(notes)
    stats = graph.stats()

    assert stats.total_notes == 3
    assert stats.total_links == 3
    assert stats.broken_links == []


def test_stats_detects_orphans():
    notes = [
        make_note("a", "A", ["b"]),
        make_note("b", "B", []),
        make_note("c", "C", []),  # nothing links to c
    ]
    graph = LinkGraph(notes)
    stats = graph.stats()

    assert stats.orphan_notes == ["a", "c"]


def test_stats_detects_broken_links():
    notes = [make_note("a", "A", ["missing-note"])]
    graph = LinkGraph(notes)
    stats = graph.stats()

    assert stats.broken_links == [("a", "missing-note")]


def test_most_linked_ranks_by_inbound_count():
    notes = [
        make_note("a", "A", ["c"]),
        make_note("b", "B", ["c"]),
        make_note("c", "C", []),
    ]
    graph = LinkGraph(notes)
    stats = graph.stats()

    assert stats.most_linked[0] == ("c", 2)


def test_to_dot_includes_all_nodes_and_edges():
    notes = [make_note("a", "A", ["b"]), make_note("b", "B", [])]
    graph = LinkGraph(notes)
    dot = graph.to_dot()

    assert "digraph linkweave" in dot
    assert '"a" -> "b"' in dot
