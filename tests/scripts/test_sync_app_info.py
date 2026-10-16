from __future__ import annotations

import tomllib

import pytest

PYPROJECT = """\
[project]
name = "sample-app"
version = "1.2.3"
description = "A sample."
license = "MIT"

[project.urls]
GitHub = "https://example.com/sample-app"

[tool.cardiomyocytes-app]
name = "Sample App"
"""
LICENSE = """\
MIT License

Copyright (c) 2026 Sample Author

Permission is hereby granted, free of charge, ...
"""


def test_app_toml_is_in_step_with_the_project(sync_app_info):
    current = sync_app_info.APP_TOML_PATH.read_text(encoding="utf-8")

    assert current == sync_app_info.build_app_toml()


def test_facts_come_from_pyproject_and_the_license(sync_app_info):
    facts = sync_app_info.app_facts(PYPROJECT, LICENSE)

    assert facts == {
        "name": "Sample App",
        "version": "1.2.3",
        "description": "A sample.",
        "copyright": "Copyright (c) 2026 Sample Author",
        "license": "MIT",
        "homepage": "https://example.com/sample-app",
    }


def test_rendered_text_reads_back_as_the_facts(sync_app_info):
    facts = {"name": r'A "quoted" \ name', "description": "Ünïcode\tand tabs"}

    text = sync_app_info.render(facts)

    assert text.startswith(sync_app_info.HEADER)
    assert tomllib.loads(text) == facts


def test_a_license_without_a_copyright_line_is_refused(sync_app_info):
    with pytest.raises(ValueError, match="no line starting with 'Copyright'"):
        sync_app_info.app_facts(PYPROJECT, "MIT License\n")
