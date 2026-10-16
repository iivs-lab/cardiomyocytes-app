# List the shipped components' licenses in the About window

- Status: accepted
- Date: 2026-10-16

## Context and problem statement

The application ships third-party code under licenses that ask for
notices: Qt and Qt for Python under the LGPL v3, the Python runtime,
the OpenSSL and libffi libraries that come with it, and the Font
Awesome glyphs the icon is drawn from. A first attempt listed every
installed package from its metadata, which the built application
cannot read without crashing (`AGENTS.md`), listed packages the build
leaves out, and showed no license texts, since the PySide6 wheels
carry none for the LGPL.

## Considered options

- Where: a Licenses window of its own, or a Licenses tab in the About
  window.
- What: every installed runtime package, or what the build ships.
- How much: license names and links, or the full texts.
- Versions: written in the data file, or read from the running
  libraries where they can tell.

## Decision outcome

- The About window (Help > About Cardiomyocytes App) has two tabs:
  About, for the application, and Licenses. One window keeps one menu
  item, and the tab gives the texts room as the list grows. Qt's own
  About box is left out: the Licenses tab already shows Qt's version
  and license texts.
- The Licenses tab lists the components the built application ships,
  named as a reader knows them: Qt covers Qt for Python, and libffi
  sits under Python in the tree, since the runtime brings it along. A
  build on 2026-10-16 showed that the application ships libffi
  whatever its own code imports, as PySide6 loads `ctypes`, and that
  Python's own license file, which carries the bzip2 and Zstandard
  notices, lacks it. A component selected shows its note, then its
  full license text.
- The build leaves out OpenSSL, which it shipped only because standard
  library modules Nuitka includes, such as `urllib.request`, import
  `ssl`; the application uses no network, and `hashlib` falls back to
  its built-in algorithms. One component fewer to list, and a smaller
  build.
- `gui/about/assets/licenses.toml` lists the components, each with
  its license, homepage, text file, an optional note, and the
  components bundled inside it. Each text is its own file beside it,
  written by `scripts/fetch_licenses.py` from its source: the running
  Python's license file, Qt's repository for the LGPL and GPL
  (gnu.org refused connections on 2026-10-16), and the tags of libffi
  and Font Awesome matching the versions shipped.
- Python and Qt report their versions at run time
  (`platform.python_version()`, `qVersion()`), so their entries hold
  none and never go stale. Font Awesome's is written in the file and
  tested against the font qtawesome ships; libffi's DLL records none,
  so it shows no version.

## Consequences

- Shipping a new component, or upgrading Python or Qt, means editing
  `licenses.toml` where needed and rerunning the script on Windows,
  whose Python license file carries the Windows build's notices.
- Qt itself contains third-party code (FreeType, HarfBuzz, libpng, and
  others) whose notices Qt documents; this list does not repeat them.
- Every license text is in the build, so the built application meets
  the LGPL's demand to come with the license texts.
- Code that comes to need TLS must let the build ship OpenSSL again
  and list it under Python (`AGENTS.md`).
