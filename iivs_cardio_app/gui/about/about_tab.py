from __future__ import annotations

__all__ = ("AboutTab",)

from typing import TYPE_CHECKING, Final

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from iivs_cardio_app.gui.app_manager import AppInfo

ICON_SIZE: Final[int] = 64


class AboutTab(QWidget):
    """The tab that tells about the application.

    Args:
        info: The facts it shows about the application.
        parent: The parent widget, if any.
    """

    def __init__(self, info: AppInfo, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._info = info
        self._setup_ui()

    def _setup_ui(self) -> None:
        info = self._info

        icon = QLabel(parent=self)
        icon.setPixmap(QApplication.windowIcon().pixmap(ICON_SIZE, ICON_SIZE))
        text = QLabel(
            f"<h2>{info.name}</h2>"
            f"<p>Version {info.version}</p>"
            f"<p>{info.description}</p>"
            f"<p>{info.copyright}<br>Licensed under the {info.license} License.</p>"
            f'<p><a href="{info.homepage}">{info.homepage}</a></p>',
            parent=self,
        )
        text.setOpenExternalLinks(True)
        text.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)

        header = QHBoxLayout()
        header.addWidget(icon, alignment=Qt.AlignmentFlag.AlignTop)
        header.addWidget(text, stretch=1)

        layout = QVBoxLayout(self)
        layout.addLayout(header)
        layout.addStretch()
