# Organize the package by front end, sub-app, and layer

- Status: accepted
- Date: 2026-10-16

## Context and problem statement

The application is one program that hosts several cardiomyocyte
analysis tools (sub-apps), starting with profile analysis and a
comparison of quantified results. It has a PySide6 GUI now, and a CLI
or a web front end may follow. The planning handoff proposed
`shell/` (the frame that knows the sub-apps), `common/` (shared code),
and `features/<name>/`, each split into `core/` (no Qt) and `gui/`.
The name `shell` did not say what the package is, and it would not
leave room for a second front end.

## Considered options

- `shell/`, as the handoff proposed.
- One package per front end, named for its kind: `gui/` now, later
  `cli/` or `web/`.
- `desktop/` for the GUI, with `cli/` beside it later.
- `frontends/gui/` and later `frontends/cli/`.

## Decision outcome

One package per front end, named for its kind. The frame the handoff
called `shell` is the GUI front end and lives in
`iivs_cardio_app/gui/`.

```
iivs_cardio_app/
├── gui/                    the PySide6 application
├── cli/, web/              later front ends
├── common/{core,gui}/      code two or more sub-apps share
└── features/<name>/        one sub-app
    ├── core/               no Qt
    └── gui/                (later cli/, web/)
```

The handoff's dependency rules carry over:

1. No `core/` imports Qt (PySide6, pyqtgraph, superqt, qtawesome) or
   any `gui/`.
2. Imports run from a front end to `features/` to `common/`, and
   within one unit from `gui/` to `core/`. `common/` knows neither
   `features/` nor a front end.
3. Sub-apps never import each other. Something two of them need moves
   to `common/` when the second one needs it, not before.
4. Only a front-end package knows the list of sub-apps, and it imports
   a sub-app the first time it is opened.
5. A heavy dependency (such as a later `torch`) is imported lazily,
   inside the one sub-app that needs it.

## Consequences

- A front-end package assembles the matching layer of every sub-app:
  `gui/` uses each `features/<name>/gui/`, a later `cli/` each
  `features/<name>/cli/`. A CLI layer imports no Qt, so it runs on a
  machine without a display.
- The name `gui` appears at three levels (the front end,
  `common/gui/`, `features/<name>/gui/`) with one meaning: the PySide6
  layer.
- `common/` and `features/` do not exist yet. Tests that check the
  rules above by reading the imports are planned with them.
