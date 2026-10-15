from __future__ import annotations

from iivs_cardio_app.shell import MainWindow


def test_main_window_opens_with_the_application_title(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)

    window.show()
    qtbot.waitExposed(window)

    assert window.isVisible()
    assert window.windowTitle() == "Cardiomyocytes App"
