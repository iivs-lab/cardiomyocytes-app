from __future__ import annotations

import pytest
from PySide6.QtCore import Qt

from iivs_cardio_app.shell.appearance import (
    apply_color_scheme,
    load_color_scheme,
    save_color_scheme,
)


class _RecordingStyleHints:
    def __init__(self):
        self.schemes = []

    def setColorScheme(self, scheme):  # noqa: N802  # mirrors the QStyleHints method
        self.schemes.append(scheme)


def test_saved_color_scheme_loads_back(settings):
    save_color_scheme(settings, "dark")

    assert load_color_scheme(settings) == "dark"


@pytest.mark.parametrize(
    "stored",
    (
        pytest.param(None, id="missing"),
        pytest.param("sepia", id="unknown"),
    ),
)
def test_missing_or_unknown_color_scheme_loads_as_system(settings, stored):
    if stored is not None:
        settings.setValue("appearance/color_scheme", stored)

    assert load_color_scheme(settings) == "system"


@pytest.mark.parametrize(
    ("scheme", "expected"),
    (
        ("system", Qt.ColorScheme.Unknown),
        ("light", Qt.ColorScheme.Light),
        ("dark", Qt.ColorScheme.Dark),
    ),
)
def test_apply_color_scheme_requests_the_matching_qt_scheme(scheme, expected):
    hints = _RecordingStyleHints()

    apply_color_scheme(hints, scheme)

    assert hints.schemes == [expected]
