# Keep data files beside the package that reads them

- Status: accepted
- Date: 2026-10-16

## Context and problem statement

The application reads files that are not code: the window icon now,
a splash image soon, and images for single sub-apps later. The build
also needs the executable's icon. Code and data should stay apart, a
checkout and the Nuitka build must find the files the same way, and
nothing should depend on a build argument that is easy to forget.

## Considered options

- One `assets/` folder at the top of the repository. The build copies
  it with `--include-data-dir=assets=assets`, and code finds it
  through the package's parent folder.
- An `assets/` folder inside the package that reads the files, found
  with `importlib.resources` and carried as package data.
- The Qt resource system: a `.qrc` file compiled by `pyside6-rcc` into
  a Python module.

## Decision outcome

An `assets/` folder beside the package that reads the files:
`gui/assets/` for the GUI front end, `features/<name>/gui/assets/` for
one sub-app, `common/gui/assets/` for shared widgets. An `assets/`
folder holds no code and no `__init__.py`. Code finds its files with
`importlib.resources.files(__package__) / "assets"`, using
`importlib.resources.as_file` where an API wants a path, and the build
carries every such folder through
`--include-package-data=iivs_cardio_app`. Code that only generates or
checks those files lives in `scripts/`.

The top-level folder was tried first and dropped: a missing build
argument goes unnoticed until a build runs, and the lookup depends on
where the package sits. The Qt resource system stores images inside a
generated module, which brings a build step and large diffs.

## Consequences

- One build argument covers every `assets/` folder, and the lookup
  works however the package is installed. A build on 2026-10-16 had
  `gui/assets/icon.ico` in its package data, and the window icon read
  through `importlib.resources` showed in the built application.
- A sub-app's images move with the sub-app.
- The application package holds data folders, kept apart from the code
  folders.
