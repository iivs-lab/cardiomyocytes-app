from __future__ import annotations

import pytest
from PySide6.QtCore import qVersion


@pytest.fixture()
def downloads(fetch_licenses, monkeypatch):
    """Answer each download with a marker naming its URL, and record the URLs."""
    urls = []

    def fake_download(url):
        urls.append(url)
        return f"text of {url}\r\n"

    monkeypatch.setattr(fetch_licenses, "_download", fake_download)
    return urls


def test_texts_cover_every_license_file(fetch_licenses, downloads):
    texts = fetch_licenses.build_texts()

    assert sorted(texts) == [
        "font-awesome-free.txt",
        "libffi.txt",
        "python.txt",
        "qt.txt",
    ]


def test_qt_text_puts_the_lgpl_before_the_gpl_after_its_header(
    fetch_licenses,
    downloads,
):
    qt = fetch_licenses.build_texts()["qt.txt"]
    base = f"https://raw.githubusercontent.com/qt/qtbase/v{qVersion()}/LICENSES"

    assert qt.startswith("Qt and Qt for Python (PySide6 and Shiboken6)\n")
    assert qt.index(f"{base}/LGPL-3.0-only.txt") < qt.index(f"{base}/GPL-3.0-only.txt")


def test_font_awesome_source_follows_the_installed_glyphs(fetch_licenses, downloads):
    fetch_licenses.build_texts()
    font_awesome = fetch_licenses.font_awesome_version()

    assert f"Font-Awesome/{font_awesome}/LICENSE.txt" in " ".join(downloads)


def test_python_text_is_the_running_pythons_license(fetch_licenses, downloads):
    expected = fetch_licenses.python_license_path().read_text(encoding="utf-8")

    python = fetch_licenses.build_texts()["python.txt"]

    assert python.split() == expected.split()


def test_texts_end_lines_in_lf_without_trailing_spaces(fetch_licenses, downloads):
    for text in fetch_licenses.build_texts().values():
        assert "\r" not in text
        assert text.endswith("\n")
        assert not text.endswith("\n\n")
        assert all(line == line.rstrip() for line in text.split("\n"))
