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

Build a standalone folder with pyside6-deploy (Nuitka). It writes
`dist/CardiomyocytesApp.dist/`, which holds `Cardiomyocytes App.exe` on
Windows:

```bash
uv run pyside6-deploy --no-install
```

Nuitka compiles with MSVC when it is installed. Without it, the first
build downloads the Zig compiler (about 100 MB) and Dependency Walker
into Nuitka's user cache (`%LOCALAPPDATA%\Nuitka` on Windows) and reuses
them afterwards.

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
