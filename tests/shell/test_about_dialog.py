from __future__ import annotations

import platform

import pytest
from PySide6.QtCore import qVersion
from PySide6.QtWidgets import QLabel, QPlainTextEdit, QPushButton, QTreeWidget

from iivs_cardio_app.licenses import PackageLicense
from iivs_cardio_app.metadata import DISPLAY_NAME, VERSION
from iivs_cardio_app.shell.about_dialog import AboutDialog


@pytest.fixture()
def dialog(qtbot, monkeypatch):
    monkeypatch.setattr(
        "iivs_cardio_app.shell.about_dialog.load_package_licenses",
        lambda: [
            PackageLicense("alpha", "1.0", "MIT", ("alpha license text",)),
            PackageLicense("beta", "2.0", "Apache-2.0"),
        ],
    )
    dialog = AboutDialog()
    qtbot.addWidget(dialog)
    return dialog


def _label_text(dialog):
    return "\n".join(label.text() for label in dialog.findChildren(QLabel))


def test_shows_the_application_before_qt(dialog):
    text = _label_text(dialog)

    assert dialog.windowTitle() == f"About {DISPLAY_NAME}"
    assert f"Version {VERSION}" in text
    assert text.index(DISPLAY_NAME) < text.index(f"Qt {qVersion()}")


def test_qt_details_open_the_about_qt_box(dialog, monkeypatch):
    shown = []

    class FakeMessageBox:
        @staticmethod
        def aboutQt(parent):  # noqa: N802  # mirrors the QMessageBox method
            shown.append(parent)

    monkeypatch.setattr(
        "iivs_cardio_app.shell.about_dialog.QMessageBox",
        FakeMessageBox,
    )

    details = next(
        button
        for button in dialog.findChildren(QPushButton)
        if button.text() == "Details…"
    )
    details.click()

    assert shown == [dialog]


def test_license_list_starts_with_python_then_the_packages(dialog):
    packages = dialog.findChild(QTreeWidget)
    rows = [
        [packages.topLevelItem(row).text(column) for column in range(3)]
        for row in range(packages.topLevelItemCount())
    ]

    assert rows == [
        ["Python", platform.python_version(), "PSF-2.0"],
        ["alpha", "1.0", "MIT"],
        ["beta", "2.0", "Apache-2.0"],
    ]


def test_selecting_a_package_shows_its_license(dialog):
    packages = dialog.findChild(QTreeWidget)
    text = dialog.findChild(QPlainTextEdit)

    packages.setCurrentItem(packages.topLevelItem(1))
    shipped = text.toPlainText()
    packages.setCurrentItem(packages.topLevelItem(2))
    missing = text.toPlainText()

    assert shipped == "alpha license text"
    assert missing.startswith("beta 2.0 is licensed under Apache-2.0.")
