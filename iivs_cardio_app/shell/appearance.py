from __future__ import annotations

__all__ = (
    "COLOR_SCHEMES",
    "ColorScheme",
    "apply_color_scheme",
    "load_color_scheme",
    "save_color_scheme",
)

from typing import TYPE_CHECKING, Final, Literal

from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from PySide6.QtCore import QSettings
    from PySide6.QtGui import QStyleHints

type ColorScheme = Literal["system", "light", "dark"]

COLOR_SCHEMES: Final[tuple[ColorScheme, ...]] = ("system", "light", "dark")
COLOR_SCHEME_KEY: Final[str] = "appearance/color_scheme"

_QT_COLOR_SCHEMES: Final[dict[ColorScheme, Qt.ColorScheme]] = {
    "system": Qt.ColorScheme.Unknown,
    "light": Qt.ColorScheme.Light,
    "dark": Qt.ColorScheme.Dark,
}


def load_color_scheme(settings: QSettings) -> ColorScheme:
    """Read the saved color scheme; a missing or unknown value reads as `"system"`."""
    value = settings.value(COLOR_SCHEME_KEY)
    for scheme in COLOR_SCHEMES:
        if value == scheme:
            return scheme
    return "system"


def save_color_scheme(settings: QSettings, scheme: ColorScheme) -> None:
    """Save `scheme` as the color scheme the next launch starts with."""
    settings.setValue(COLOR_SCHEME_KEY, scheme)


def apply_color_scheme(hints: QStyleHints, scheme: ColorScheme) -> None:
    """Draw the application in `scheme`, where `"system"` follows the OS setting.

    A platform that cannot override the OS setting, such as `offscreen`, ignores the
    request.
    """
    hints.setColorScheme(_QT_COLOR_SCHEMES[scheme])
