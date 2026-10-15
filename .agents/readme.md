# Writing `README.md`

The root `README.md` is the landing page: what the project is, how to
set it up and run it, and where to read further. It is not a
reference; signatures, options, and edge cases belong in docstrings.

Top to bottom, it holds:

1. The title (`name` in `pyproject.toml`) and the badges.
2. The one-line description in italics: word for word the
   `description` in `pyproject.toml`, trailing punctuation included,
   under 120 characters. Change the two together.
3. Optionally, a short paragraph with no heading: two to four
   sentences on scope, background, or who the project is for.
4. The lead sections, in this order:
   - 📦 Setup: every step a fresh clone needs before the project runs:
     requirements (Python, hardware, drivers), `uv sync`, and one-time
     steps such as environment files or system libraries, each with its
     command.
   - 🚀 Usage: how to run the project: its commands, scripts, or entry
     points, and where their configuration lives.
   - 🗂️ Layout, once the tree no longer explains itself: one line per
     top-level directory a reader needs to find their way.

   The first entry in a section replaces its placeholder.
5. Project-specific sections, as the project needs them (a key
   concept, platform notes, acknowledgements), in the order a reader
   needs them, acknowledgements last.
6. The closing sections, always last and in this order:
   📋 TODO, 📜 Changelog, ⚖️ License.

- Every `##` heading starts with one emoji, as the template's do, and
  no two sections share one.
- Keep the template's sections, their names, and their order, and edit
  them in place; a project-specific section goes only where step 5
  puts it.
- No hand-written table of contents and no "back to top" links: GitHub
  gives every README an Outline button, and a root README long enough to
  need either is carrying material that belongs in a sub-README or in
  docstrings. Hand-made links to these headings also break silently: an
  emoji such as ⚖️ leaves an invisible U+FE0F in its anchor
  (`#️-license`).
- Keep the Python requirement in the badge and in 📦 Setup
  in step with `requires-python` in `pyproject.toml`.
- A badge for a dependency (a framework, a CUDA version) goes right
  after the Python badge and shows the minimum in `pyproject.toml`; it
  moves with that minimum.
- Every code example runs against the current code: a change that breaks
  one updates it in the same commit. Show the result when it is the
  point, as a trailing `# -> ...` comment.
- Links stay valid: a commit that moves, renames, or deletes a file or
  directory fixes every README link to it: the root's hub links and
  the sub-READMEs' relative ones. `git grep -n '<old path>' -- '*.md'`
  finds them.

## Sub-READMEs

A directory whose use outgrows its 🗂️ Layout entry gets its
own `README.md` next to its code. The root then acts as a hub: the
entry keeps its summary and links to that README, and examples specific
to it move there. A root README without 🗂️ Layout gains one for the
link.

A sub-README is shaped by what it documents (a file format, a family
of APIs, a pipeline step), so it has no fixed sections. It does keep to
these:

- The title names what it covers: the directory, or a package's import
  path in backticks.
- One or two sentences under the title say what it covers and when to
  reach for it.
- It may go deeper than the root (concepts, worked examples, choosing
  between APIs, pitfalls) but leaves signatures and parameter details
  to docstrings and does not repeat the root.
- Its code examples run, under the same rule as the root's.
- Headings carry no emoji, so their anchors stay plain.
- Once it runs past a couple of screens, it opens with a `## Contents`
  list: a plain bullet list linking each `##` section, never folded into
  `<details>`: a contents list helps only while it is in view.
- Keep `## Contents` in step with the headings: a commit that adds,
  removes, renames, or reorders a `##` section updates the list. An
  anchor is the heading lowercased, spaces turned into hyphens, and
  punctuation other than `-` and `_` dropped:
  `` ## Resolving conflicts: `on_conflict` `` links as
  `#resolving-conflicts-on_conflict`.
- No "back to top" links: GitHub's file view has its own Top button.
