from __future__ import annotations

import platform
from pathlib import Path

import pytest
import qtawesome
from PySide6.QtCore import qVersion

from iivs_cardio_app.gui.about.licenses import Component


def _walk(components):
    for component in components:
        yield component
        yield from _walk(component.bundled)


def _components():
    return {component.name: component for component in _walk(Component.load_all())}


def test_components_are_listed_in_order():
    names = [component.name for component in Component.load_all()]

    assert names == ["Python", "Qt", "Font Awesome Free"]


def test_python_brings_libffi_along():
    bundled = {
        component.name: [child.name for child in component.bundled]
        for component in Component.load_all()
    }

    assert bundled == {
        "Python": ["libffi"],
        "Qt": [],
        "Font Awesome Free": [],
    }


def test_runtime_components_report_the_running_versions():
    components = _components()

    assert components["Python"].version == platform.python_version()
    assert components["Qt"].version == qVersion()


def test_only_libffi_lacks_a_version():
    missing = [
        component.name for component in _components().values() if not component.version
    ]

    assert missing == ["libffi"]


def test_font_awesome_version_matches_the_glyphs_the_icon_is_drawn_from():
    fonts = Path(qtawesome.__file__).parent / "fonts"
    (font,) = fonts.glob("fontawesome5-solid-webfont-*.ttf")

    assert _components()["Font Awesome Free"].version == font.stem.rsplit("-", 1)[1]


@pytest.mark.parametrize(
    ("name", "heading"),
    (
        ("Python", "PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2"),
        ("Qt", "GNU LESSER GENERAL PUBLIC LICENSE"),
        ("Qt", "GNU GENERAL PUBLIC LICENSE"),
        ("libffi", "Permission is hereby granted"),
        ("Font Awesome Free", "Font Awesome Free License"),
    ),
)
def test_each_license_text_holds_its_license(name, heading):
    assert heading in _components()[name].read_license_text()


def test_qt_note_names_qt_for_python():
    assert "Qt for Python (PySide6 and Shiboken6)" in _components()["Qt"].note
