from __future__ import annotations

import pytest
from PySide6.QtCore import QSettings


@pytest.fixture()
def settings(tmp_path):
    """An INI-backed `QSettings` in `tmp_path`, so tests never touch the user's own."""
    return QSettings(str(tmp_path / "settings.ini"), QSettings.Format.IniFormat)
