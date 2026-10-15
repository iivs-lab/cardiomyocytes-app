from __future__ import annotations

from iivs_cardio_app.gui.bootstrap import load_app_icon


def test_app_icon_holds_every_size_of_its_ico(qapp):
    sizes = [size.width() for size in load_app_icon().availableSizes()]

    assert sorted(sizes) == [16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96, 128, 256]
