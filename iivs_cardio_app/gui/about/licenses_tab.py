from __future__ import annotations

__all__ = ("LicensesTab",)

from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import (
    QPlainTextEdit,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from iivs_cardio_app.gui.about.licenses import Component


class LicensesTab(QWidget):
    """The tab that lists the shipped components and shows the license of one.

    A component shipped inside another, such as a library the Python runtime brings
    along, sits under it in the tree. Selecting a component shows its note, if any,
    followed by its full license text. The first component is selected from the
    start.

    Args:
        parent: The parent widget, if any.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()

        # Selected once connected, so the first license shows through the slot.
        if (first := self._tree.topLevelItem(0)) is not None:
            self._tree.setCurrentItem(first)

    def _setup_ui(self) -> None:
        self._tree = self._create_tree()
        self._text = QPlainTextEdit(parent=self)
        self._text.setReadOnly(True)

        layout = QVBoxLayout(self)
        layout.addWidget(self._tree, stretch=1)
        layout.addWidget(self._text, stretch=2)

    def _create_tree(self) -> QTreeWidget:
        tree = QTreeWidget(parent=self)
        tree.setHeaderLabels(["Component", "Version", "License"])
        self._add_items(tree.invisibleRootItem(), Component.load_all())
        tree.expandAll()

        for column in range(tree.columnCount()):
            tree.resizeColumnToContents(column)

        return tree

    @staticmethod
    def _add_items(parent: QTreeWidgetItem, components: tuple[Component, ...]) -> None:
        # Each item takes its parent at once, so Qt owns it from the start.
        for component in components:
            data = [component.name, component.version, component.license]
            item = QTreeWidgetItem(parent, data)
            item.setData(0, Qt.ItemDataRole.UserRole, component)
            LicensesTab._add_items(item, component.bundled)

    def _connect_signals(self) -> None:
        self._tree.currentItemChanged.connect(self._on_component_changed)

    @Slot(QTreeWidgetItem, QTreeWidgetItem)
    def _on_component_changed(
        self,
        current: QTreeWidgetItem | None,
        _previous: QTreeWidgetItem | None,
    ) -> None:
        if current is None:
            self._text.clear()
            return
        component: Component = current.data(0, Qt.ItemDataRole.UserRole)
        text = component.read_license_text()
        if component.note:
            text = f"{component.note}\n\n{text}"
        self._text.setPlainText(text)
