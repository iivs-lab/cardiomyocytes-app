from __future__ import annotations

import pytest
from PySide6.QtWidgets import QLabel

from iivs_cardio_app.gui.about.about_tab import AboutTab
from iivs_cardio_app.gui.app_manager import AppInfo

INFO = AppInfo(
    name="Test App",
    version="9.8.7",
    description="An application under test.",
    copyright="Copyright (c) 2026 Tester",
    license="MIT",
    homepage="https://example.com/test-app",
)


@pytest.fixture()
def tab(qtbot):
    tab = AboutTab(INFO)
    qtbot.addWidget(tab)
    return tab


def test_shows_the_facts_it_was_given(tab):
    text = "\n".join(label.text() for label in tab.findChildren(QLabel))

    assert "<h2>Test App</h2>" in text
    assert "Version 9.8.7" in text
    assert "An application under test." in text
    assert "Copyright (c) 2026 Tester" in text
    assert "Licensed under the MIT License." in text
    assert 'href="https://example.com/test-app"' in text
