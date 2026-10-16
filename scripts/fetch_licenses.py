from __future__ import annotations

import sys
import sysconfig
import urllib.request
from pathlib import Path
from typing import Final

import qtawesome
from PySide6.QtCore import qVersion

ROOT: Final[Path] = Path(__file__).resolve().parent.parent
ASSETS_DIR: Final[Path] = ROOT / "iivs_cardio_app" / "gui" / "about" / "assets"

# Qt ships the license texts it is offered under; gnu.org, the other source of the
# same texts, refused connections when this was written.
QT_LICENSE_URL: Final[str] = (
    "https://raw.githubusercontent.com/qt/qtbase/v{version}/LICENSES/{spdx}.txt"
)
# CPython's Windows build pins libffi 3.4.4, and its DLL records no version.
LIBFFI_URL: Final[str] = (
    "https://raw.githubusercontent.com/libffi/libffi/v3.4.4/LICENSE"
)
FONT_AWESOME_URL: Final[str] = (
    "https://raw.githubusercontent.com/FortAwesome/Font-Awesome/{version}/LICENSE.txt"
)

QT_HEADER: Final[str] = """\
Qt and Qt for Python (PySide6 and Shiboken6)
Copyright (C) The Qt Company Ltd. and other contributors.

Both are used under the GNU Lesser General Public License version 3, which follows,
together with the GNU General Public License version 3 that it supplements.
"""
SECTION_RULE: Final[str] = "\n" + "=" * 79 + "\n\n"


def _download(url: str) -> str:
    with urllib.request.urlopen(url, timeout=30) as response:  # noqa: S310  # fixed https URLs
        return response.read().decode("utf-8")


def _normalized(text: str) -> str:
    lines = text.replace("\r\n", "\n").rstrip("\n").split("\n")
    return "\n".join(line.rstrip() for line in lines) + "\n"


def font_awesome_version() -> str:
    """Return the Font Awesome 5 version qtawesome bundles, which drew the icon."""
    fonts = Path(qtawesome.__file__).parent / "fonts"
    (font,) = fonts.glob("fontawesome5-solid-webfont-*.ttf")
    return font.stem.removeprefix("fontawesome5-solid-webfont-")


def python_license_path() -> Path:
    """Return the license file of the running Python, with its build's own notices.

    Windows keeps it at the top of the installation, other systems in the standard
    library folder. Run this on Windows: the application is built there, and only
    that file holds the Windows build's notices.
    """
    candidates = (
        Path(sys.base_prefix) / "LICENSE.txt",
        Path(sysconfig.get_path("stdlib")) / "LICENSE.txt",
    )
    for path in candidates:
        if path.is_file():
            return path
    msg = f"no LICENSE.txt in the Python installation: {sys.base_prefix}"
    raise FileNotFoundError(msg)


def build_texts() -> dict[str, str]:
    """Return the text of each license file, keyed by its name in `ASSETS_DIR`."""
    lgpl, gpl = (
        _download(QT_LICENSE_URL.format(version=qVersion(), spdx=spdx))
        for spdx in ("LGPL-3.0-only", "GPL-3.0-only")
    )
    texts = {
        "python.txt": python_license_path().read_text(encoding="utf-8"),
        "qt.txt": QT_HEADER + SECTION_RULE + lgpl + SECTION_RULE + gpl,
        "libffi.txt": _download(LIBFFI_URL),
        "font-awesome-free.txt": _download(
            FONT_AWESOME_URL.format(version=font_awesome_version()),
        ),
    }
    return {name: _normalized(text) for name, text in texts.items()}


def main() -> None:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in build_texts().items():
        path = ASSETS_DIR / name
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
