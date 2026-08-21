from pathlib import Path

from linkweave.parser import find_notes, parse_note, slugify


def test_slugify_normalizes_case_and_whitespace():
    assert slugify("  My   Note  ") == "my note"


def test_slugify_treats_hyphens_and_underscores_as_spaces():
    assert slugify("reading-list") == slugify("Reading List") == "reading list"
    assert slugify("my_note_name") == "my note name"


def test_parse_note_falls_back_to_filename_when_no_heading(tmp_path: Path):
    note_path = tmp_path / "untitled-thoughts.md"
    note_path.write_text("Just some text, no heading.")

    note = parse_note(note_path)

    assert note.title == "untitled-thoughts"


def test_parse_note_extracts_title_and_links(tmp_path: Path):
    note_path = tmp_path / "example.md"
    note_path.write_text(
        "# My Example Note\n\nThis links to [[Other Note]] and [[Other Note|a display alias]].\n"
    )

    note = parse_note(note_path)

    assert note.title == "My Example Note"
    assert note.slug == "example"
    assert note.links == ["other note", "other note"]
    assert note.word_count > 0


def test_find_notes_recurses_into_subfolders(tmp_path: Path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "a.md").write_text("# A\n[[B]]")
    (tmp_path / "sub" / "b.md").write_text("# B\nno links here")

    notes = find_notes(tmp_path)

    assert {n.slug for n in notes} == {"a", "b"}
