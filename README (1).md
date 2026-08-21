# Linkweave

A small CLI tool that scans a folder of Markdown notes, finds `[[wiki-style links]]`
between them, and reports on the shape of the resulting graph: how connected your
notes are, which ones are orphaned, which links are broken, and which notes are
the most-referenced hubs. It can also export the graph to Graphviz `.dot` format
for visualization.

If you keep a personal wiki, a Zettelkasten, or an Obsidian/Roam-style vault of
Markdown notes, Linkweave gives you a fast, dependency-light way to audit it from
the terminal — no app required.

## Why

Note-taking tools like Obsidian have a built-in graph view, but if your notes are
just plain `.md` files (in a git repo, synced folder, or anywhere else), you don't
always have that view available. Linkweave is a standalone way to get the same
insight anywhere your notes live, and to script/automate checks like "do I have
any broken links" as part of a CI pipeline for your notes repo.

## Install

```bash
git clone https://github.com/<your-username>/linkweave.git
cd linkweave
pip install -e .
```

Requires Python 3.10+. No third-party dependencies.

## Usage

```bash
linkweave path/to/notes
```

Example, using the sample vault included in this repo:

```bash
linkweave example_notes
```

```
Linkweave report for: example_notes

  Notes scanned:   5
  Links found:     6
  Broken links:    1
  Orphan notes:    1

Most-linked notes (top 10):
    2  Reading List  (reading list)
    1  Projects  (projects)
    1  Home  (home)
    1  Linkweave  (linkweave)

Orphan notes (no inbound links):
  - Stray Thought  (stray thought)

Broken links (target note not found):
  - Home -> [[nonexistent note]]
```

### Export to Graphviz

```bash
linkweave example_notes --dot graph.dot
dot -Tpng graph.dot -o graph.png   # requires Graphviz installed separately
```

### Options

| Flag | Description |
|---|---|
| `path` | Folder to scan recursively for `.md` files |
| `--dot PATH` | Write a Graphviz `.dot` export of the graph |
| `--top N` | Number of most-linked notes to show (default: 10) |

## How it works

- Notes are matched by filename slug (`My Note.md` → `my note`), so `[[My Note]]`
  and `[[my note]]` both resolve to the same note regardless of case/whitespace.
- A note's title is taken from its first `# Heading`, falling back to the filename.
- Links use the `[[Target]]` or `[[Target|Display text]]` syntax common to
  Obsidian, Roam, and similar tools.

## Development

```bash
pip install -e . pytest
pytest -v
```

## License

MIT — see [LICENSE](LICENSE).
