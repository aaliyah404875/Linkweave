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
