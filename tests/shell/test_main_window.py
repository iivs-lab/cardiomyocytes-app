from __future__ import annotations

from iivs_cardio_app.shell import MainWindow
from iivs_cardio_app.shell.appearance import load_color_scheme, save_color_scheme


def _menu(window, title):
    return next(
        action.menu() for action in window.menuBar().actions() if action.text() == title
    )


def _theme_actions(window):
    view_menu = _menu(window, "&View")
    theme_menu = next(
        action.menu() for action in view_menu.actions() if action.text() == "&Theme"
    )
    return {action.text(): action for action in theme_menu.actions()}


def test_main_window_opens_with_the_application_title(qtbot, settings):
    window = MainWindow(settings)
    qtbot.addWidget(window)

    window.show()
    qtbot.waitExposed(window)

    assert window.isVisible()
    assert window.windowTitle() == "Cardiomyocytes App"


def test_theme_menu_checks_only_the_saved_color_scheme(qtbot, settings):
    save_color_scheme(settings, "light")

    window = MainWindow(settings)
    qtbot.addWidget(window)

    checked = [
        text for text, action in _theme_actions(window).items() if action.isChecked()
    ]
    assert checked == ["&Light"]


def test_choosing_a_theme_applies_and_saves_it(qtbot, settings, monkeypatch):
    applied = []
    monkeypatch.setattr(
        "iivs_cardio_app.shell.main_window.apply_color_scheme",
        lambda _hints, scheme: applied.append(scheme),
    )
    window = MainWindow(settings)
    qtbot.addWidget(window)

    _theme_actions(window)["&Dark"].trigger()

    assert applied == ["dark"]
    assert load_color_scheme(settings) == "dark"
    assert _theme_actions(window)["&Dark"].isChecked()
