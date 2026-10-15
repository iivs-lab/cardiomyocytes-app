from __future__ import annotations

import platform
from email.message import Message
from importlib.metadata import PackageNotFoundError, version

import pytest

from iivs_cardio_app.licenses import (
    PackageLicense,
    collect_package_licenses,
    dump_package_licenses,
    load_package_licenses,
    python_license,
)
from iivs_cardio_app.metadata import RUNTIME_DISTRIBUTIONS


class _FakePath:
    def __init__(self, path, text=None):
        self._path = path
        self.name = path.rsplit("/", 1)[-1]
        self._text = text

    def __str__(self):
        return self._path

    def read_text(self, encoding):
        if self._text is None:
            raise FileNotFoundError(self._path)
        return self._text


class _FakeDistribution:
    def __init__(self, name, *, headers=(), requires=None, files=None):
        self.name = name
        self.version = "1.0"
        self.metadata = Message()
        for key, value in headers:
            self.metadata[key] = value
        self.requires = requires
        self.files = files


@pytest.fixture()
def installed(monkeypatch):
    """Replace the installed distributions with the fakes a test puts in the dict."""
    distributions = {}

    def fake_distribution(name):
        try:
            return distributions[name.lower().replace("_", "-")]
        except KeyError:
            raise PackageNotFoundError(name) from None

    monkeypatch.setattr(
        "iivs_cardio_app.licenses.distribution",
        fake_distribution,
    )
    return distributions


def test_collects_the_roots_and_their_installed_requirements(installed):
    installed["root"] = _FakeDistribution(
        "Root",
        requires=[
            "dep-b>=1",
            "dep_a",
            'missing; python_version < "3.11"',
            'optional; extra == "full"',
        ],
    )
    installed["dep-a"] = _FakeDistribution("dep_a", requires=["Root"])
    installed["dep-b"] = _FakeDistribution("dep-b")
    installed["optional"] = _FakeDistribution("optional")

    names = [package.name for package in collect_package_licenses(["root"])]

    assert names == ["dep_a", "dep-b", "Root"]


@pytest.mark.parametrize(
    ("headers", "expected"),
    (
        pytest.param(
            [("License-Expression", "MIT"), ("License", "BSD")],
            "MIT",
            id="expression-first",
        ),
        pytest.param([("License", "BSD-3-Clause")], "BSD-3-Clause", id="license"),
        pytest.param(
            [
                ("License", "Copyright (c) someone\nPermission is granted ..."),
                ("Classifier", "License :: OSI Approved :: MIT License"),
                ("Classifier", "Programming Language :: Python"),
            ],
            "MIT License",
            id="full-text-falls-back-to-classifier",
        ),
        pytest.param([], "Unknown", id="none"),
    ),
)
def test_license_name_prefers_the_most_specific_field(installed, headers, expected):
    installed["pkg"] = _FakeDistribution("pkg", headers=headers)

    (package,) = collect_package_licenses(["pkg"])

    assert package.license == expected


def test_license_texts_skip_commercial_terms_and_unreadable_files(installed):
    installed["pkg"] = _FakeDistribution(
        "pkg",
        files=[
            _FakePath("pkg/__init__.py", "code"),
            _FakePath("pkg-1.0.dist-info/licenses/NOTICE", "notice text"),
            _FakePath("pkg-1.0.dist-info/licenses/LICENSE", "license text"),
            _FakePath("pkg-1.0.dist-info/licenses/LicenseRef-Commercial.txt", "paid"),
            _FakePath("pkg-1.0.dist-info/licenses/COPYING"),
        ],
    )

    (package,) = collect_package_licenses(["pkg"])

    assert package.texts == ("license text", "notice text")


def test_installed_pyside6_is_collected_with_its_version():
    packages = {
        package.name: package for package in collect_package_licenses(["pyside6"])
    }

    assert packages["PySide6"].version == version("pyside6")
    assert packages["shiboken6"].version == version("shiboken6")


def test_python_license_describes_the_running_interpreter():
    assert python_license() == PackageLicense(
        name="Python",
        version=platform.python_version(),
        license="PSF-2.0",
    )


def test_dumped_licenses_load_back(tmp_path):
    licenses = [
        PackageLicense("alpha", "1.0", "MIT", ("Copyright Ä\nline two",)),
        PackageLicense("beta", "2.0", "Apache-2.0"),
    ]
    path = tmp_path / "license_data.json"
    path.write_text(dump_package_licenses(licenses), encoding="utf-8")

    assert load_package_licenses(path) == licenses


def test_license_data_matches_the_installed_packages():
    installed = collect_package_licenses(RUNTIME_DISTRIBUTIONS)

    assert load_package_licenses() == installed, (
        "license_data.json is stale; run `uv run python -m iivs_cardio_app.licenses`"
    )
