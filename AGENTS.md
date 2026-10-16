# Agent guide: `cardiomyocytes-app`

Guidance for AI coding assistants working on this project.
`CLAUDE.md` loads this file via the `@AGENTS.md` import.

## Project

- Package: `iivs_cardio_app/`
- Python:  3.14+
- Kind:    application, not packaged for distribution

## Toolchain

The Astral toolchain. Keep it unless there is a clear reason to change:

- `uv`: environment, locking, running
- `ruff`: linting + formatting
- `ty`: type checking
- `pytest`: testing
- `pytest-cov`: coverage measurement and threshold gate

## Commands

```bash
uv sync --group dev      # create/refresh the environment
uv run ruff check .      # lint
uv run ruff format .     # format
uv run ty check          # type-check
uv run pytest            # run tests (coverage included by default)
uv run pytest --no-cov   # skip coverage for quick iteration
uv run pytest -m "not slow"  # skip tests marked slow
```

Coverage is measured by `pytest-cov` against `iivs_cardio_app/` with
branch tracking; the `fail_under` gate lives in `pyproject.toml`
(see `tests/AGENTS.md`).

## Task guides

Rules for one kind of task live in their own file. Read the guide
before you start that task:

| Before you ...                          | Read                      |
| --------------------------------------- | ------------------------- |
| write or change a test                  | `tests/AGENTS.md`         |
| commit (only when the user asks)        | `.agents/commits.md`      |
| add, remove, or upgrade a dependency    | `.agents/dependencies.md` |
| change the supported Python versions    | `.agents/dependencies.md` |
| edit `CHANGELOG.md`                     | `.agents/changelog.md`    |
| edit `README.md` or a sub-README        | `.agents/readme.md`       |
| add or remove a `TODO.md` item          | `.agents/todo.md`         |
| record a design decision                | `.agents/decisions.md`    |
| cut a release (only when the user asks) | `.agents/releases.md`     |

`tests/AGENTS.md` also loads on its own whenever you work in `tests/`.

## Workflow

A change is done when the gates pass. Before reporting it finished,
run them in this order and fix what they find:

```bash
uv run ruff format .
uv run ruff check --fix .
uv run ty check
uv run pytest
```

If one cannot run here (a test needing hardware or a service this
machine lacks), say which and why instead of skipping it silently. CI
runs the same gates, but it should confirm a change, not discover that
it is broken.

- Commit only when the user asks, then follow `.agents/commits.md`.
- Push only when the user asks; a release the user asked for includes
  its push and tag. Never force-push, rewrite pushed history, or move
  or delete a tag.
- Work on the current branch, usually `main`. Create a branch only when
  the user asks for one.
- Never skip git hooks (`--no-verify`).

### Secrets

- No token, password, or private key in code, docs, commit messages,
  or logs, nor a test or example value that is real somewhere.
- Code reads a secret from an environment variable. `.env` holds the
  local values and is never committed (`.gitignore` covers it); the
  README's 📦 Setup names each variable the project
  needs, never its value.
- If a secret has been committed, stop and tell the user before
  changing anything: removing it from history does not take it back.
  The credential has to be revoked and replaced.

## Code style

Run `uv run ruff format .` and `uv run ruff check --fix .` rather than
styling by hand. `ruff` enforces the import groups and order, the blank
lines around imports and definitions, the 88-column limit (`E501`),
`pathlib` over `os.path` (`PTH`), exception messages built in a `msg`
variable (`EM`), and `%`-style logging arguments (`G`). The rules
below are the ones it cannot check. *All Python code* covers tests
too; *Source code* does not. `tests/AGENTS.md` says
what tests do differently.

### All Python code

A module runs, top to bottom:

1. `from __future__ import annotations`, except in an `__init__.py`.
2. `__all__` as a tuple, where the module has one; in an `__init__.py`
   it comes before the re-exports.
3. Imports, then an optional `if TYPE_CHECKING:` block of type-only
   imports.
4. Constants, type aliases, functions, and classes.
5. An `if __name__ == "__main__":` guard, in a runnable script only.

- One blank line between `__all__` and the imports; `ruff` sets every
  other blank line between the parts above.
- Import by absolute path. A relative import is for the rare case an
  absolute one cannot work, with `# noqa: TID252` and the reason.
- Define a private helper above its first caller, so the module reads
  top-down; private and public definitions are not kept apart.
- `ruff format` wraps code past 88 columns; shorten or rewrap a
  docstring, comment, or string yourself.
- A call that does not fit on one line takes one argument per line,
  with a trailing comma so the formatter keeps that shape. Assign a
  setup call to a local rather than nesting it in another call.
- An import or `__all__` that fits on one line stays on one line, with
  no trailing comma to hold it open.
- A comprehension takes one `for`; write a loop for anything more.
- In a function body, a blank line separates logical groups; a body of
  one or two lines has none.
- Use builtin generics (`list`, `dict`), `X | None`, and PEP 695
  syntax (`type Alias = ...`, `def f[T](...)`, `class C[T]:`), never
  `TypeVar`, `TypeAlias`, `Optional`, or `Union`.
- Fix a `ruff` or `ty` finding rather than suppressing it. A justified
  suppression names the code and gives the reason in a comment:
  `# noqa: <code>`, or `# ty: ignore[<error-name>]` with `ty`'s own
  error names, never a bare one.
- In a long module, group related definitions under a boxed banner: a
  centred title-case title, 30 columns wide, two blank lines on each
  side:

  ```python
  # ========================== #
  #          Reading           #
  # ========================== #
  ```

- Docstrings, comments, and messages use no em dash and no ` -- `.
- In docstrings and comments, single backticks mark identifiers,
  values, and expressions alike (`path`, `"merge"`, `(H, W)`); double
  backticks only when the content holds a backtick.
- A standalone runnable script carries PEP 723 inline metadata. Manage
  it with `uv add --script`; edit it by hand only when asked.

### Source code

Modules and classes:

- A module takes no docstring unless the user asks for one.
- A module-level constant is `UPPER_SNAKE` and annotated `Final`.
- A class body opens with its docstring, then `__slots__` and class
  attributes, then `__init__` (or `__post_init__`) and `__repr__`;
  `__enter__` and `__exit__` close it. Order the methods between for
  readability and consistency: related methods together, sibling
  classes in the same order.
- Mark every override with `@override`, an implemented
  `abstractmethod` included; a self-evident dunder (`__len__`) needs
  none.
- An `@abstractmethod` takes a docstring and a bare
  `raise NotImplementedError`; a `Protocol` member keeps `...`.
- A value type is `@dataclass(frozen=True, slots=True)`; a plain
  `@dataclass` is for mutable configuration.
- A closed set of options is a `Literal` alias, not an `Enum`.
- Keep code fully typed (`ty` runs with `error-on-warning`), with
  standard typing only: `ty` has no plugins, so use PEP 681
  `dataclass_transform` or `.pyi` stubs.

Errors and messages:

- Raise built-in exceptions. Add a custom one only when callers need to
  catch it apart; name it `*Error` and subclass one built-in.
- Write the `msg` on one line. When it would pass 88 columns, shorten
  the prose, hoist a value to a local, or use `{value=}`; never split
  the string.
- A message starts lower-case and ends without a period, unless it
  begins with an identifier. Show a value with `!r`, not hand-written
  quotes, and put a path at the end.
- Name the valid set or the fix, not just the failure ("unsupported
  node type 'X': expected File, Directory, ...").

Docstrings and comments:

- Docstrings are optional. Write one where it clarifies *intent and
  contracts, not mechanism*: never restate the code, and never explain
  a base class through its subclasses (a *closed* hierarchy's base may
  name them as a family map). A public method callers consume still
  gets one.
  - The summary is one line ending in a period: a noun phrase for a
    class ("An ordered, read-only view over ..."), a property ("The
    reporting unit ..."), and a boolean method ("Whether `path`
    exists."); an imperative verb phrase for every other function and
    method ("Yield successive windows from `items`.").
  - A consumed public method is self-explainable from its own
    docstring and signature, never an inherited one. An abstract
    method documents the generic contract and names no subclass.
  - Say what the signature cannot: invariants, edge cases, what
    subclasses must override, trade-offs. Document an edge case a
    family shares once, on the class.
  - Use [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
    sections (`Args:`, `Returns:`, `Yields:`, `Raises:`,
    `Type Parameters:`), without types in `Args:`. Custom sections
    (`Example:`) are welcome when they clarify a real pitfall. Add a
    section only for what the summary and signature do not convey;
    often the summary *is* the whole docstring.
  - Document constructor arguments in the class docstring's `Args:`
    and leave `__init__` bare. An `@overload` stub takes no docstring.
- Comments explain why, not what: a constraint, a reason, a rejected
  alternative. Keep a comment to one line, three at most; longer
  belongs in a docstring or a commit message. An inline comment is for
  a short qualifier, such as a unit.
- Fill docstring and comment prose toward 88 columns: a line was
  wrapped early if the next line's first word would still have fit.
  Nothing checks this, so rewrap and read the result. Never split a
  backticked span or an `*emphasis*` across lines.

## Documentation

Whoever changes the code keeps the documents current, in the same
commit as the change. A docs-only fix (wording, a stale example) is
its own `📝` commit.

| When a change ...                                         | Update                                   |
| --------------------------------------------------------- | ---------------------------------------- |
| alters user-visible behavior, requirements, or dependencies | `CHANGELOG.md` → `[Unreleased]`        |
| changes how the project is set up                         | `README.md` → 📦 Setup                   |
| changes how the project is run                            | `README.md` → 🚀 Usage                   |
| adds, moves, or removes a top-level directory             | `README.md` → 🗂️ Layout, if present      |
| changes code that a README example uses                   | that README → the example                |
| moves, renames, or deletes a file a README links to       | that README → the link                   |
| adds, removes, renames, or reorders a sub-README section  | that README → `## Contents`, if present  |
| defers work, or uncovers a problem it does not fix        | `TODO.md` → add an item                  |
| resolves a `TODO.md` item                                 | `TODO.md` → remove the item              |
| settles a design choice later work should not reopen      | `docs/decisions/` → add a record         |
| settles a convention later sessions must follow           | `AGENTS.md` → below the marker           |

Each document has one audience and one tense:

- `README.md` describes the project **as it is now**: what it does and
  how to set it up and run it. No history, no "new in vX.Y".
- `CHANGELOG.md` records what **changed for a user** of the
  application: external behavior only, never internal refactoring.
- `TODO.md` lists work that is **not done yet**.
- `docs/decisions/` records **why** the code is shaped as it is: one
  decision per file, written once.
- `AGENTS.md` and its guides hold rules for whoever works on the code
  next.

Every document wraps prose at 72 columns; tables, code blocks,
headings, and a line holding a long URL or command are exempt. Write
a new document in English; one already written in another language
keeps that language. No document uses an em dash or ` -- ` in its
prose: recast the sentence with a colon, a comma, parentheses, or two
sentences.

### `AGENTS.md`

- When a project-specific convention, command, or pitfall is settled
  (the user states a rule, or a workflow is agreed on), record it
  below the `<!-- Add project-specific guidance below. -->` marker at
  the end of this file.
- Leave everything above the marker as it is, and the guides in
  `.agents/` and `tests/AGENTS.md` too: `copier update` refreshes them
  from the template, so local edits turn into merge conflicts. If a
  template rule does not fit, add an overriding note below the marker
  and tell the user.

## Template

Generated from a copier template. `.copier-answers.yml` records the
answers; run `copier update --UNSAFE` to pull later template changes.

---

<!-- Add project-specific guidance below. -->

## Project notes

Design decisions and their reasons are in `docs/decisions/`; the notes
below are the rules that follow from them.

### Package layout

- One package per front end, named for its kind: `gui/` is the
  PySide6 application, and a later CLI or web front end goes beside it
  as `cli/` or `web/`. Sub-apps live in `features/<name>/` and shared
  code in `common/`, both split into `core/` (no Qt) and `gui/` (later
  `cli/`). See `docs/decisions/0001-*.md` for the dependency rules
  between them: no Qt in `core/`, imports run from a front end to
  `features/` to `common/`, and sub-apps never import each other.
- `main.py` in the project root is the one entry point, for a run from
  the checkout (`uv run python main.py`) and for the build. It only
  starts the process; `gui/bootstrap.py` assembles and runs the
  application in `main()`, and `gui/launcher.py` is the launcher window
  and nothing more. `gui/__init__.py` exports `main` alone.
- The package has no `__main__.py`, and no module in it gets an
  `if __name__ == "__main__":` block, which would run the module twice
  (`docs/decisions/0002-*.md`). A later front end that needs its own
  command gets one in its package, such as `cli/__main__.py`.
- The GUI opens a launcher, and each sub-app opens in its own window.
  The launcher, the settings window, the About window (which shows the
  licenses), and each sub-app's window exist at most once per process;
  asking for an open one brings it to the front. The GUI front end
  opens and tracks them (`docs/decisions/0006-*.md`). Values pass
  between sub-apps only through the GUI front end, typed by
  `common/core/` (planned; `docs/decisions/0004-*.md`).

### Assets and scripts

- A data file the application reads goes in an `assets/` folder beside
  the package that reads it: `gui/assets/`,
  `features/<name>/gui/assets/`, or `common/gui/assets/`. An `assets/`
  folder holds no code and no `__init__.py`. Code finds it with
  `importlib.resources.files(__package__) / "assets"` (and
  `importlib.resources.as_file` where an API wants a path); the build
  carries it through `--include-package-data=iivs_cardio_app`
  (`docs/decisions/0003-*.md`).
- `scripts/` holds development scripts that generate or check data
  files. They run in the project environment,
  `uv run python scripts/<name>.py`, and import nothing from
  `iivs_cardio_app`. Overriding the template rule above, they carry no
  PEP 723 metadata: what they import is a project dependency (user
  decision, 2026-10-16). `tests/scripts/` tests them, loading each from
  its file through a fixture in its `conftest.py`.
- `scripts/create_icon.py` builds `iivs_cardio_app/gui/assets/icon.ico`
  from stacked qtawesome glyphs (`docs/decisions/0005-*.md`). Change
  the icon there, rerun the script, and commit the ICO; never edit the
  ICO by hand. Generate it on Windows: the fit depends on how glyphs
  snap to pixels, which differs on Linux, so its pixel-fit tests run on
  Windows only (`windows_glyph_rendering` in `tests/marks.py`).

### Build

- `uv run pyside6-deploy --no-install` builds the application from
  `[tool.pyside6.deploy]` in `pyproject.toml`; pyside6-deploy reads
  that table only from the `pyproject.toml` beside its entry file,
  which is why `main.py` stays in the project root.
- On Windows, build from a Visual Studio developer shell, as the
  README's 🏗️ Build shows. pyside6-deploy finds `dumpbin` only on
  `PATH`; without it the build merely warns and caches an incomplete Qt
  module list in `pysidedeploy.spec`.
- Do not add a `[tool.pyside6-project]` table to silence the build's
  "Unable to resolve a valid project file" warning: its `files` takes
  no directories or globs, so it would have to list every source file,
  and pyside6-deploy would scan only those for Qt modules (user
  decision, 2026-10-15).
- The build leaves out Qt Network and Qt PDF (`extra_args` in
  `[tool.pyside6.deploy]`). Code that starts using either must drop the
  matching `--noinclude-qt-plugins`, `--nofollow-import-to`, and
  `--noinclude-dlls` arguments in the same commit, or the built
  application fails to import it.
- The built application must not read installed distribution metadata
  (licenses, versions): reading it through Nuitka's
  `--include-distribution-metadata` crashed the build (2026-10-15).
  Ship such facts as a data file generated before the build.
- Build a test program with `--windows-console-mode=attach`, as the
  application does: with Nuitka's default (`force`), standalone builds
  here crash at startup, even a hello world.

### Qt tests

- GUI tests use `pytest-qt` (`qtbot`). `tests/conftest.py` defaults
  `QT_QPA_PLATFORM` to `offscreen`, so they run without a display.
- CI installs the Qt system libraries on Linux in `ci.yml`; keep that
  step when `copier update` touches the workflow.

### Reference implementation

- The old application, `../cardiomyocytes-app-old`, is a reference for
  requirements and domain logic only (what users must be able to do,
  the beat-detection algorithm, validation, quantification, and their
  defaults), never for structure, state handling, markers, or file
  formats. Its latest code is on the remote branch `origin/remake`,
  which has no local branch: read it with
  `git -C ../cardiomyocytes-app-old show origin/remake:<path>`, and do
  not change that repository.
