from __future__ import annotations

import pytest

from iivs_cardio_app.gui.app_manager import AppManager


@pytest.fixture()
def manager(qapp):
    return AppManager()
