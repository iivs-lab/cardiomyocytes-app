from __future__ import annotations

import re
import shlex
import tomllib
from pathlib import Path

from iivs_cardio_app.metadata import (
    APPLICATION_NAME,
    COPYRIGHT,
    DESCRIPTION,
    DISPLAY_NAME,
    HOMEPAGE,
    LICENSE,
    RUNTIME_DISTRIBUTIONS,
    VERSION,
)

ROOT = Path(__file__).resolve().parents[1]
PYPROJECT = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def _normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def test_project_fields_match_pyproject():
    project = PYPROJECT["project"]

    assert project["name"] == APPLICATION_NAME
    assert project["version"] == VERSION
    assert project["description"] == DESCRIPTION
    assert project["license"] == LICENSE
    assert project["urls"]["GitHub"] == HOMEPAGE


def test_runtime_distributions_match_pyproject_dependencies():
    dependencies = PYPROJECT["project"]["dependencies"]
    declared = {_normalize(re.match(r"[\w.-]+", item).group()) for item in dependencies}
    listed = {_normalize(name) for name in RUNTIME_DISTRIBUTIONS}

    assert listed == declared


def test_display_name_names_the_built_executable():
    extra_args = shlex.split(PYPROJECT["tool"]["pyside6"]["deploy"]["extra_args"])

    assert f"--output-filename={DISPLAY_NAME}" in extra_args


def test_copyright_matches_the_license_file():
    assert COPYRIGHT in (ROOT / "LICENSE").read_text(encoding="utf-8")
