# Start the application from `main.py` only

- Status: accepted
- Date: 2026-10-16

## Context and problem statement

pyside6-deploy reads `[tool.pyside6.deploy]` only from the
`pyproject.toml` beside its entry file, so the build needs `main.py` in
the project root. The template also created
`iivs_cardio_app/__main__.py` for `python -m iivs_cardio_app`. The two
files held the same two lines. Starting the GUI on its own was also
proposed as an `if __name__ == "__main__":` block in the module that
assembles it.

## Considered options

- Keep both `main.py` and `__main__.py`.
- Keep `main.py` alone.
- Keep `main.py` alone and add a `__main__` block to
  `gui/bootstrap.py`.

## Decision outcome

`main.py` alone. A run from the checkout (`uv run python main.py`) and
the build start from the same file. Starting the GUI takes three
modules, one step each: `main.py` starts the process and exits with
its code, `gui/bootstrap.py` assembles and runs the application in
`main()`, and `gui/launcher.py` is the launcher window.
`gui/__init__.py` exports `main` alone.

No module inside the package gets a `__main__` block:
`python -m iivs_cardio_app.gui.bootstrap` imports the package first,
whose `__init__.py` imports `bootstrap`, so the module runs twice.
Python warns about it (`RuntimeWarning: 'iivs_cardio_app.gui.bootstrap'
found in sys.modules after import of package 'iivs_cardio_app.gui'`),
and module state such as a registry of open windows would exist twice.

## Consequences

- `python -m iivs_cardio_app` no longer starts the application.
- A later front end that needs a command of its own gets a package
  `__main__.py`, such as `iivs_cardio_app/cli/__main__.py`, which runs
  once.
