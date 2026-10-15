from __future__ import annotations

import os

# Windows stay off screen, so the tests run on CI runners with no display and do
# not flash on a desktop; set `QT_QPA_PLATFORM` to watch them instead.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
