from __future__ import annotations

__all__ = ("AboutDialog",)

from typing import TYPE_CHECKING, Final

from PySide6 import __version__ as pyside6_version
from PySide6.QtCore import qVersion
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from iivs_cardio_app.licenses import load_package_licenses, python_license
from iivs_cardio_app.metadata import (
    COPYRIGHT,
    DESCRIPTION,
    DISPLAY_NAME,
    HOMEPAGE,
    LICENSE,
    VERSION,
)

if TYPE_CHECKING:
    from iivs_cardio_app.licenses import PackageLicense

DEFAULT_SIZE: Final[tuple[int, int]] = (640, 640)


def _describe(package: PackageLicense) -> str:
    if package.texts:
        return "\n\n".join(package.texts)
    return (
        f"{package.name} {package.version} is licensed under {package.license}.\n\n"
        "The package ships no license document of its own."
    )


class AboutDialog(QDialog):
    """A window that shows the application, then Qt, then the open source licenses.

    Args:
        parent: The parent widget, if any.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._licenses = [
            python_license(),
            *load_package_licenses(),
        ]
        self.setWindowTitle(f"About {DISPLAY_NAME}")
        self.resize(*DEFAULT_SIZE)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close, parent=self)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(self._create_application_section())
        layout.addWidget(self._create_qt_section())
        layout.addWidget(self._create_license_section(), stretch=1)
        layout.addWidget(buttons)

    def _create_application_section(self) -> QLabel:
        label = QLabel(
            f"<h2>{DISPLAY_NAME}</h2>"
            f"<p>Version {VERSION}</p>"
            f"<p>{DESCRIPTION}</p>"
            f"<p>{COPYRIGHT}<br>Licensed under the {LICENSE} License.</p>"
            f'<p><a href="{HOMEPAGE}">{HOMEPAGE}</a></p>',
            parent=self,
        )
        label.setOpenExternalLinks(True)
        return label

    def _create_qt_section(self) -> QGroupBox:
        group = QGroupBox("Qt", parent=self)
        summary = QLabel(
            f"Qt {qVersion()} with PySide6 {pyside6_version}, "
            "used under the GNU LGPL version 3.",
            parent=group,
        )
        details = QPushButton("Details…", parent=group)
        details.clicked.connect(lambda _checked=False: QMessageBox.aboutQt(self))

        layout = QHBoxLayout(group)
        layout.addWidget(summary, stretch=1)
        layout.addWidget(details)
        return group

    def _create_license_section(self) -> QGroupBox:
        group = QGroupBox("Open Source Licenses", parent=self)
        packages = QTreeWidget(parent=group)
        packages.setHeaderLabels(["Package", "Version", "License"])
        packages.setRootIsDecorated(False)
        text = QPlainTextEdit(parent=group)
        text.setReadOnly(True)

        # Each item takes the tree as its parent, so Qt owns it from the start.
        for package in self._licenses:
            QTreeWidgetItem(packages, [package.name, package.version, package.license])
        self._packages = packages
        self._license_text = text
        packages.currentItemChanged.connect(self._show_license)
        if (first := packages.topLevelItem(0)) is not None:
            packages.setCurrentItem(first)
        for column in range(packages.columnCount()):
            packages.resizeColumnToContents(column)

        layout = QVBoxLayout(group)
        layout.addWidget(packages)
        layout.addWidget(text)
        return group

    # Takes both arguments of `currentItemChanged`, so PySide never has to drop one.
    def _show_license(
        self,
        current: QTreeWidgetItem | None,
        _previous: QTreeWidgetItem | None,
    ) -> None:
        index = self._packages.indexOfTopLevelItem(current) if current else -1
        text = _describe(self._licenses[index]) if index >= 0 else ""
        self._license_text.setPlainText(text)
