from __future__ import annotations

import sys

import pytest

# The application icon is generated on Windows, and its pixel fit depends on how the
# platform rasterizes glyphs: Linux snaps a 16 px glyph to whole pixels differently.
windows_glyph_rendering = pytest.mark.skipif(
    sys.platform != "win32",
    reason="needs Windows glyph rendering, which the icon is fitted under",
)
