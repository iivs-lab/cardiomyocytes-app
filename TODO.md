# TODO

Open work that is not done yet: deferred, blocked on a decision, or a
known limitation. Delete an item in the commit that resolves it.

## Open

- `iivs_cardio_app/`: add `common/` and `features/` with the first
  sub-app, the launcher's sub-app buttons, a window per sub-app, and
  the messaging between them through the GUI front end
  (`docs/decisions/0001-*.md`, `0004-*.md`); add tests that check the
  import rules of decision 0001 by reading the imports.
- `gui/menu_bar.py`: give the disabled items their features: File >
  Preferences… (the settings window, `docs/decisions/0006-*.md`), File >
  Close Window, Window > Launcher (`AppManager.show_launcher()`), and
  Help > Report an Issue (the project's issue tracker).
- `gui/`: show a splash image from `gui/assets/` while the application
  starts.
- Add the color scheme choice (system, light, dark) to the
  application's global settings.
- Once result files and settings are saved: notice before saving a
  result that another process changed the file since it was read, and
  write settings atomically, since several application processes may
  run at once (`docs/decisions/0004-*.md`).
- `gui/about/about_tab.py`: take the icon from `AppAssets` instead of
  `QApplication.windowIcon()`, as every other shared asset is passed
  in (`docs/decisions/0008-*.md`).
- Repeat the application's name in one place only: the About item's
  text in `gui/menu_bar.py` and `title` and `--output-filename` in
  `[tool.pyside6.deploy]` spell it out beside `app.toml`.
- `scripts/`: check a build's `dist/` folder against `licenses.toml`,
  since the shipped DLLs are now compared by hand, and macOS and Linux
  builds will ship other libraries (`docs/decisions/0007-*.md`).

### Settle how sub-apps plug into the GUI front end

Three questions block the first sub-app; settle them in one
`docs/decisions/` record before writing it:

- **Contract.** A sub-app in `features/` must not import `gui/`
  (decision 0001), yet each window shows the shared `MenuBar`, which
  lives in `gui/` and acts on `AppManager`. Either the front end adds
  the menu bar to a sub-app window it creates, or `common/gui/` holds
  a protocol the front end implements. The sub-app also needs a
  description the launcher reads (name, window factory) to register
  itself.
- **Closing a window.** Closing only hides a window today, so its data
  stays in memory, and `AppManager.close_windows()` skips hidden
  windows: unsaved work in a sub-app window the user closed is lost at
  quit without a question. Either closing asks about unsaved work and
  discards the window, or quitting also asks the hidden ones.
- **`AppManager`'s scope.** A `show_*` method per window kind grows
  with every sub-app; one `show(kind)` over the registered sub-apps
  scales. Settings and the messaging between sub-apps should not all
  land in the same class.

Revisit when the profile-analysis sub-app starts.

### Give each operating system its own icon format

Each system takes the application icon differently, and only the
Windows one exists:

- Windows embeds `gui/assets/icon.ico` in the executable.
- macOS puts an `.icns` file (sizes up to 1024 px) in the app bundle;
  Nuitka converts another image only when `imageio` is installed.
- Linux keeps no icon in the executable: Nuitka's `--linux-icon` only
  names one in the desktop file, which shows once a PNG or SVG is
  installed into the system icon folders.

Supporting macOS and Linux touches four places:
`scripts/create_icon.py` writes each format (up to 1024 px for
macOS); `gui/assets/` holds them; `AppAssets.load()` in
`gui/app_manager.py` picks one per system or keeps reading `icon.ico`,
which Qt opens everywhere; and the build sets `icon` per system, since
`[tool.pyside6.deploy]` holds a single path.

Revisit when the application is first built on macOS or Linux.
