from __future__ import annotations

import tomllib
from importlib.resources import files

import pytest
from PySide6.QtCore import QEvent, QObject
from PySide6.QtWidgets import QApplication

from iivs_cardio_app.gui.about import AboutWindow
from iivs_cardio_app.gui.app_manager import AppInfo, AppManager
from iivs_cardio_app.gui.launcher import LauncherWindow


class RefuseClose(QObject):
    """An event filter that refuses every close, as a window with unsaved work may."""

    def eventFilter(self, _watched, event):  # noqa: N802  # Qt's method name
        if event.type() == QEvent.Type.Close:
            event.ignore()
            return True
        return False


@pytest.fixture()
def quits(monkeypatch):
    """Record each `QApplication.quit()` call instead of quitting the test run."""
    calls = []
    monkeypatch.setattr(QApplication, "quit", lambda: calls.append("quit"))
    return calls


@pytest.fixture()
def windows(qtbot, manager):
    """Open the launcher, then the About window, and return them in that order."""
    opened = (manager.show_launcher(), manager.show_about())
    for window in opened:
        qtbot.addWidget(window)
    return opened


def test_info_holds_the_facts_of_app_toml(manager):
    path = files("iivs_cardio_app.gui") / "assets" / "app.toml"
    facts = tomllib.loads(path.read_text(encoding="utf-8"))

    assert manager.assets.info == AppInfo(**facts)


def test_icon_holds_every_size_of_its_ico(manager):
    sizes = [size.width() for size in manager.assets.icon.availableSizes()]

    assert sorted(sizes) == [16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96, 128, 256]


@pytest.mark.parametrize(
    ("show", "kind"),
    (
        (AppManager.show_launcher, LauncherWindow),
        (AppManager.show_about, AboutWindow),
    ),
    ids=("launcher", "about"),
)
def test_show_reuses_one_window_and_restores_it(qtbot, manager, show, kind):
    first = show(manager)
    qtbot.addWidget(first)
    first.showMinimized()

    second = show(manager)

    assert isinstance(first, kind)
    assert second is first
    assert second.isVisible()
    assert not second.isMinimized()


def test_show_brings_a_closed_window_back(qtbot, manager):
    first = manager.show_about()
    qtbot.addWidget(first)
    first.close()

    assert manager.show_about() is first
    assert first.isVisible()


def test_window_kinds_are_kept_apart(manager, windows):
    launcher, about = windows

    assert manager.show_launcher() is launcher
    assert manager.show_about() is about


def test_about_window_shows_the_managers_facts(manager, windows):
    _launcher, about = windows

    assert about.windowTitle() == f"About {manager.assets.info.name}"


def test_each_manager_keeps_windows_of_its_own(qtbot, qapp):
    windows = [AppManager().show_about() for _ in range(2)]
    for window in windows:
        qtbot.addWidget(window)

    assert windows[0] is not windows[1]


def test_quit_closes_every_window_then_quits(manager, windows, quits):
    assert manager.quit()
    assert [window.isVisible() for window in windows] == [False, False]
    assert quits == ["quit"]


def test_a_window_that_refuses_to_close_stops_the_quit(manager, windows, quits):
    launcher, about = windows
    refuse = RefuseClose()
    about.installEventFilter(refuse)

    assert not manager.quit()
    assert launcher.isVisible()
    assert about.isVisible()
    assert quits == []


def test_close_windows_spares_the_window_to_keep(manager, windows):
    launcher, about = windows

    assert manager.close_windows(keep=launcher)
    assert launcher.isVisible()
    assert not about.isVisible()


def test_closing_the_launcher_closes_the_other_windows_first(windows):
    launcher, about = windows

    assert launcher.close()
    assert not about.isVisible()


def test_the_launcher_stays_open_while_a_window_refuses(windows):
    launcher, about = windows
    refuse = RefuseClose()
    about.installEventFilter(refuse)

    assert not launcher.close()
    assert launcher.isVisible()
    about.removeEventFilter(refuse)
