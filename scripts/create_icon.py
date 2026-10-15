from __future__ import annotations

import math
import struct
import sys
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Final

import qtawesome as qta
from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QRect
from PySide6.QtGui import QGuiApplication, QImage, QImageWriter, QPainter

ROOT: Final[Path] = Path(__file__).resolve().parent.parent
ICO_PATH: Final[Path] = ROOT / "iivs_cardio_app" / "gui" / "assets" / "icon.ico"

# Windows asks for the 16 px and 32 px icons times the display scale (100 % to 300 %),
# plus 128 px and 256 px for Explorer; a size it finds here is drawn without scaling.
ICO_SIZES: Final[tuple[int, ...]] = (
    16,
    20,
    24,
    28,
    32,
    40,
    48,
    56,
    64,
    80,
    96,
    128,
    256,
)

MARGIN: Final[int] = 1  # transparent pixels kept at every edge
# The heart carries its weight in the top lobes, so centering its top and bottom
# edges makes it look high. The row put at the canvas center lies this fraction of
# the way from the middle of those edges to the center of mass.
OPTICAL_WEIGHT: Final[float] = 0.5
FIT_PASSES: Final[int] = 6

BORDER_COLOR: Final[str] = "#000000"
BORDER_WIDTH: Final[float] = 1.0  # pixels, at every size
BORDER_DIRECTIONS: Final[int] = 8


@dataclass(frozen=True, slots=True)
class Glyph:
    """One qtawesome glyph in the icon stack.

    Args:
        name: The qtawesome icon name, such as `"fa5s.heartbeat"`.
        color: The fill color.
        scale: The glyph size as a fraction of the icon size.
        offset: The shift from the center as fractions of the icon size.
    """

    name: str
    color: str
    scale: float = 1.0
    offset: tuple[float, float] = (0.0, 0.0)


# The old application's icon, bottom to top: a heart with a beat line under a
# microscope.
GLYPHS: Final[tuple[Glyph, ...]] = (
    Glyph("fa5s.heartbeat", "#e74c3c"),
    Glyph("fa5s.microscope", "#ffffff", scale=0.7, offset=(0.0, -0.05)),
)


@dataclass(frozen=True, slots=True)
class _Placement:
    zoom: float = 1.0
    dx: float = 0.0  # fractions of the icon size, rightward
    dy: float = 0.0  # fractions of the icon size, downward


@dataclass(frozen=True, slots=True)
class _Extent:
    left: int
    top: int
    right: int
    bottom: int
    mass_y: float

    @property
    def center_x(self) -> float:
        return (self.left + self.right + 1) / 2

    @property
    def anchor_y(self) -> float:
        middle = (self.top + self.bottom + 1) / 2
        return middle + OPTICAL_WEIGHT * (self.mass_y - middle)


def _paint(size: int, placement: _Placement) -> QImage:
    # Each glyph's border is the glyph itself in `BORDER_COLOR`, laid down one step
    # away in every direction before the glyph goes on top. qtawesome offsets are
    # fractions of the icon size, so a fixed pixel width needs a step per size.
    step = BORDER_WIDTH / size
    angles = [2 * math.pi * k / BORDER_DIRECTIONS for k in range(BORDER_DIRECTIONS)]
    names: list[str] = []
    options: list[dict[str, object]] = []
    for glyph in GLYPHS:
        scale = glyph.scale * placement.zoom
        x = glyph.offset[0] * placement.zoom + placement.dx
        y = glyph.offset[1] * placement.zoom + placement.dy
        layers = [(x + step * math.cos(a), y + step * math.sin(a)) for a in angles]
        colors = [BORDER_COLOR] * len(layers) + [glyph.color]
        for offset, color in zip([*layers, (x, y)], colors, strict=True):
            names.append(glyph.name)
            options.append({"color": color, "scale_factor": scale, "offset": offset})

    # Painting into an image of the target size, rather than asking the icon for a
    # pixmap, keeps the screen's device pixel ratio out of the result.
    image = QImage(size, size, QImage.Format.Format_ARGB32)
    image.fill(0)
    painter = QPainter(image)
    qta.icon(*names, options=options).paint(painter, QRect(0, 0, size, size))
    painter.end()
    return image


def _measure(image: QImage) -> _Extent:
    alpha = image.convertToFormat(QImage.Format.Format_Alpha8)
    width, stride = alpha.width(), alpha.bytesPerLine()
    data = bytes(alpha.constBits())

    left, right = width, -1
    rows: list[int] = []
    total = moment = 0.0
    for y in range(alpha.height()):
        row = data[y * stride : y * stride + width]
        if not any(row):
            continue
        rows.append(y)
        left = min(left, width - len(row.lstrip(b"\0")))
        right = max(right, len(row.rstrip(b"\0")) - 1)
        total += sum(row)
        moment += sum(row) * (y + 0.5)
    return _Extent(left, rows[0], right, rows[-1], moment / total)


def _grow(placement: _Placement, extent: _Extent, size: int) -> _Placement:
    # The vertical extent counts from the anchor, which will sit at the center.
    height = 2 * max(extent.anchor_y - extent.top, extent.bottom + 1 - extent.anchor_y)
    factor = (size - 2 * MARGIN) / max(extent.right + 1 - extent.left, height)
    return replace(placement, zoom=placement.zoom * factor)


def _center(placement: _Placement, extent: _Extent, size: int) -> _Placement:
    return replace(
        placement,
        dx=placement.dx + (size / 2 - extent.center_x) / size,
        dy=placement.dy + (size / 2 - extent.anchor_y) / size,
    )


def _fits(extent: _Extent, size: int) -> bool:
    low, high = MARGIN, size - 1 - MARGIN
    return (
        min(extent.left, extent.top) >= low and max(extent.right, extent.bottom) <= high
    )


def render_icon(size: int) -> QImage:
    """Render the icon on a transparent square of exactly `size` pixels.

    Each size is fitted on its own, since glyphs snap to the pixel grid differently
    at each one: the icon is centered across and at `OPTICAL_WEIGHT` down, grown
    until it reaches `MARGIN`, and never drawn inside the margin.
    """
    # Growing and centering each take a fresh measurement: pixel snapping makes the
    # result of one step hard to predict from the other's.
    placement = _Placement()
    for _ in range(FIT_PASSES):
        placement = _grow(placement, _measure(_paint(size, placement)), size)
        placement = _center(placement, _measure(_paint(size, placement)), size)

    # Pixel snapping can leave the result a pixel too large; shrink until it fits.
    image = _paint(size, placement)
    while not _fits(_measure(image), size):
        placement = replace(placement, zoom=placement.zoom * 0.998)
        image = _paint(size, placement)
    return image


def _png_bytes(image: QImage) -> bytes:
    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    # `QImage.save` takes the format as `str` at run time but `bytes` in its stubs;
    # `QImageWriter` takes a `QByteArray` in both.
    QImageWriter(buffer, QByteArray(b"PNG")).write(image)
    return bytes(buffer.data().data())


def _ico_bytes(images: list[QImage]) -> bytes:
    # Qt's ICO writer stores one image per file, so the entries are packed by hand,
    # each holding a PNG as Windows Vista and later accept.
    pngs = [_png_bytes(image) for image in images]
    header = struct.pack("<HHH", 0, 1, len(pngs))
    entries = b""
    offset = len(header) + 16 * len(pngs)
    for image, png in zip(images, pngs, strict=True):
        side = image.width() if image.width() < 256 else 0  # 0 stands for 256
        entries += struct.pack("<BBBBHHII", side, side, 0, 0, 1, 32, len(png), offset)
        offset += len(png)
    return header + entries + b"".join(pngs)


def main() -> None:
    app = QGuiApplication(sys.argv)  # qtawesome loads its fonts through the app
    ICO_PATH.write_bytes(_ico_bytes([render_icon(size) for size in ICO_SIZES]))
    print(f"wrote {ICO_PATH}")
    app.quit()


if __name__ == "__main__":
    main()
