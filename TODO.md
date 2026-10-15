# TODO

Open work that is not done yet: deferred, blocked on a decision, or a
known limitation. Delete an item in the commit that resolves it.

## Open

- Show the licenses of the dependencies the application uses,
  Font Awesome Free (CC BY 4.0) included, since the icon is built from
  its glyphs.
- Add the color scheme choice (system, light, dark) to the
  application's global settings.

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
macOS); `gui/assets/` holds them; `load_app_icon()` in
`gui/bootstrap.py` picks one per system or keeps reading `icon.ico`,
which Qt opens everywhere; and the build sets `icon` per system, since
`[tool.pyside6.deploy]` holds a single path.

Revisit when the application is first built on macOS or Linux.
