from __future__ import annotations

__all__ = (
    "APPLICATION_NAME",
    "COPYRIGHT",
    "DESCRIPTION",
    "DISPLAY_NAME",
    "HOMEPAGE",
    "LICENSE",
    "ORGANIZATION_NAME",
    "RUNTIME_DISTRIBUTIONS",
    "VERSION",
)

from typing import Final

# The application runs uninstalled, so it cannot read `pyproject.toml` through
# `importlib.metadata`; `tests/test_metadata.py` keeps these values in step with it.
APPLICATION_NAME: Final[str] = "cardiomyocytes-app"
ORGANIZATION_NAME: Final[str] = "iivs-lab"
DISPLAY_NAME: Final[str] = "Cardiomyocytes App"
VERSION: Final[str] = "0.1.0"
DESCRIPTION: Final[str] = "A GUI application for cardiomyocyte analysis"
COPYRIGHT: Final[str] = "Copyright (c) 2026 Jaewoo Park"
LICENSE: Final[str] = "MIT"
HOMEPAGE: Final[str] = "https://www.github.com/iivs-lab/cardiomyocytes-app"
RUNTIME_DISTRIBUTIONS: Final[tuple[str, ...]] = ("pyside6",)
