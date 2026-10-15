# cardiomyocytes-app

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg?logo=opensourceinitiative&logoColor=white)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.14%20%7C%203.15-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-%E2%89%A56.12.0-41cd52.svg?logo=qt&logoColor=white)](https://doc.qt.io/qtforpython-6/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ty/main/assets/badge/v0.json)](https://github.com/astral-sh/ty)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-orange.json)](https://github.com/copier-org/copier)

_A GUI application for cardiomyocyte analysis_

## 📦 Setup

Requires Python 3.14+.

```bash
git clone https://github.com/iivs-lab/cardiomyocytes-app.git
cd cardiomyocytes-app
uv sync --group dev
```

## 🚀 Usage

Launch the application from the project root:

```bash
uv run python -m iivs_cardio_app
```

To build a standalone application instead, see 🏗️ Build below.

## 🏗️ Build

pyside6-deploy compiles the application with Nuitka into a folder that
runs without Python. It builds for the platform it runs on only, so
build on each operating system you ship to. Builds are tested on
Windows; the Linux and macOS steps below follow the tools' requirements
but have not been run yet.

### Requirements

| Platform | Operating system                          | C compiler                                       | Other tools                                                    |
| -------- | ----------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------- |
| Windows  | x64 or ARM64                              | MSVC 14.3 (VS 2022) or later, or Zig via Nuitka  | none                                                           |
| Linux    | glibc 2.34+ (x86_64), 2.39+ (aarch64)     | gcc 5 or later                                   | `patchelf` (not 0.18.0), `readelf` (binutils), Qt libraries    |
| macOS    | macOS 14 or later                         | clang (Xcode Command Line Tools)                 | `dyld_info` (Xcode 15 or later)                                |

The operating system floors come from the PySide6 wheels, so they hold
for every machine that runs the built application too. The compiler
floors are Nuitka's for Python 3.14. Python and Nuitka themselves come
from `uv sync --group dev`.

- **Windows:** install Visual Studio Build Tools with the "Desktop
  development with C++" workload; Nuitka uses MSVC whenever it finds it,
  and its `dumpbin` lets pyside6-deploy detect which Qt plugins the
  application needs. Without MSVC, the first build downloads the Zig
  compiler (about 100 MB) and Dependency Walker into
  `%LOCALAPPDATA%\Nuitka` and reuses them afterwards. Zig is enough for
  development builds; release builds use MSVC.
- **Linux (Debian or Ubuntu):** glibc 2.34 means Ubuntu 22.04 or later
  on x86_64, and glibc 2.39 means Ubuntu 24.04 or later on aarch64.
  Nuitka refuses patchelf 0.18.0, a buggy release, unless it comes from
  a Debian, Ubuntu, Fedora, or SUSE package. Install the compiler, the
  tools, and the Qt system libraries, which the build imports and the
  built application needs at run time:

  ```bash
  sudo apt-get install build-essential patchelf libegl1 libgl1 libopengl0 libxkbcommon0 libfontconfig1 libdbus-1-3
  ```

- **macOS:** install the Xcode Command Line Tools:

  ```bash
  xcode-select --install
  ```

### Building

Run from the project root:

```bash
uv run pyside6-deploy --no-install
```

| Platform | Output                                                |
| -------- | ----------------------------------------------------- |
| Windows  | `dist/CardiomyocytesApp.dist/Cardiomyocytes App.exe`  |
| Linux    | `dist/CardiomyocytesApp.dist/Cardiomyocytes App`      |
| macOS    | `dist/CardiomyocytesApp.app`                          |

The build settings live in `[tool.pyside6.deploy]` in `pyproject.toml`,
and `main.py` in the project root is the build entry point.
`--no-install` keeps pyside6-deploy from calling `pip`, which a uv
environment lacks; Nuitka comes from the `dev` group instead. The first
run writes `pysidedeploy.spec`, which caches the detected Qt modules:
delete it after the application starts using a new Qt module.

The build warns `Unable to resolve a valid project file`. It is
harmless: without a `[tool.pyside6-project]` table, pyside6-deploy
scans every Python file in the project for the Qt modules it needs.

## 📋 TODO

See [TODO.md](./TODO.md) for tracked open items.

## 📜 Changelog

See [CHANGELOG.md](./CHANGELOG.md) for the version history.

## ⚖️ License

This project is distributed under the terms of the
[MIT](./LICENSE) license.
