# Pass one app manager down from the bootstrap

- Status: accepted
- Date: 2026-10-16

## Context and problem statement

Decision 0006 lets each window kind exist at most once per process,
and the front end has to track the open windows to keep that promise.
The windows also show facts about the application (its name, version,
and license) read from `gui/assets/app.toml`. The first About window
kept itself in a module global, and every widget read the facts
through a cached module function, so any module could reach both from
anywhere, and tests had to reset the global between them.

## Considered options

- A module global per window and a cached reader for the facts.
- One process-wide object reached through a global accessor, such as a
  `QApplication` subclass or a singleton class.
- One object that the bootstrap creates and passes down to the widgets
  that need it.

## Decision outcome

The bootstrap creates one `AppManager` (`gui/app_manager.py`) per
process and passes it down. It loads what the whole application
shares, the facts and the icon, once into `AppAssets` when it is
created, and owns every window decision 0006 covers, keyed by window
class: `show_launcher()`, `show_about()`, and later the settings
window and each sub-app's window. It also ends them: `quit()` closes
every window, the newest first, and stops when one refuses, such as a
window with unsaved work. A widget gets only what it uses: a window
whose menus open others takes the manager, and the About window takes
the facts alone. No module keeps a window, the facts, or the icon in a
global or behind a module-level loader.

## Consequences

- Constructors name what a widget depends on, and a test builds its
  own manager or a stand-in, with no module state to reset.
- Modules the manager imports, such as the windows and their menu bar,
  name it for type checking only, since a runtime import would be
  circular; a menu item reaches it through a small function.
- A second manager in one process would open a second set of windows,
  so only the bootstrap creates one.
