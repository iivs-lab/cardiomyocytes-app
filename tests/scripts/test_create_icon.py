from __future__ import annotations

import struct

import pytest
from PySide6.QtCore import QBuffer, QByteArray, QIODevice
from PySide6.QtGui import QImageReader


@pytest.mark.parametrize("size", (16, 48, 256))
def test_icon_is_exactly_the_size_with_transparent_corners(qtbot, create_icon, size):
    image = create_icon.render_icon(size)

    assert (image.width(), image.height()) == (size, size)
    corners = [(0, 0), (size - 1, 0), (0, size - 1), (size - 1, size - 1)]
    assert [image.pixelColor(x, y).alpha() for x, y in corners] == [0, 0, 0, 0]
    assert image.pixelColor(size // 2, size // 2).alpha() == 255


def _opaque_span(image, *, horizontal):
    size = image.width()
    filled = []
    for index in range(size):
        for other in range(size):
            x, y = (index, other) if horizontal else (other, index)
            if image.pixelColor(x, y).alpha():
                filled.append(index)
                break
    return filled[0], filled[-1]


@pytest.mark.parametrize("size", (16, 20, 32, 64, 256))
def test_icon_fills_the_canvas_but_its_margin(qtbot, create_icon, size):
    image = create_icon.render_icon(size)
    margin = create_icon.MARGIN

    left, right = _opaque_span(image, horizontal=True)
    top, bottom = _opaque_span(image, horizontal=False)

    assert min(left, top) >= margin
    assert max(right, bottom) <= size - 1 - margin
    assert right - left + 1 >= size - 2 * margin - 1


@pytest.mark.parametrize("size", (16, 24, 40, 64, 256))
def test_icon_sits_halfway_between_edge_and_mass_centering(qtbot, create_icon, size):
    image = create_icon.render_icon(size)
    top, bottom = _opaque_span(image, horizontal=False)
    total = moment = 0
    for y in range(size):
        for x in range(size):
            alpha = image.pixelColor(x, y).alpha()
            total += alpha
            moment += alpha * (y + 0.5)
    middle = (top + bottom + 1) / 2
    anchor = middle + create_icon.OPTICAL_WEIGHT * (moment / total - middle)

    assert abs(anchor - size / 2) <= 0.5
    assert moment / total < middle


def test_ico_holds_every_size_in_order(qtbot, create_icon):
    images = [create_icon.render_icon(size) for size in create_icon.ICO_SIZES]
    data = create_icon._ico_bytes(images)  # noqa: SLF001  # the ICO layout is the contract

    reserved, kind, count = struct.unpack_from("<HHH", data)
    buffer = QBuffer()
    buffer.setData(QByteArray(data))
    buffer.open(QIODevice.OpenModeFlag.ReadOnly)
    reader = QImageReader(buffer, QByteArray(b"ico"))
    sizes = []
    while not (image := reader.read()).isNull():
        sizes.append(image.width())
        if not reader.jumpToNextImage():
            break

    assert (reserved, kind, count) == (0, 1, len(create_icon.ICO_SIZES))
    assert sizes == list(create_icon.ICO_SIZES)
