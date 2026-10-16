# Changelog

All notable changes to this project will be documented in this file.

The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `PySide6>=6.12.0` as a runtime requirement, for the Qt GUI.
- `qtawesome>=1.4.2` as a runtime requirement, for icon fonts.
- `python main.py` in the project root, which opens the application's
  launcher window.
- The application icon, a heart with a microscope, on the application's
  windows and on the built executable.
- A menu bar with **File**, **Window**, and **Help** menus on the
  launcher; their items show disabled until their features exist.
- **File > Quit** (Ctrl+Q) closes every window and quits the
  application; closing the launcher does the same.
- **Help > About Cardiomyocytes App**, a window with the application's
  version and license, and the licenses of the components the
  application ships, with their full texts.

[Unreleased]: https://github.com/iivs-lab/cardiomyocytes-app/commits/main
