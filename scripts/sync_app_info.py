from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Final

ROOT: Final[Path] = Path(__file__).resolve().parent.parent
PYPROJECT_PATH: Final[Path] = ROOT / "pyproject.toml"
LICENSE_PATH: Final[Path] = ROOT / "LICENSE"
APP_TOML_PATH: Final[Path] = ROOT / "iivs_cardio_app" / "gui" / "assets" / "app.toml"

HEADER: Final[str] = """\
# Facts about the application that its windows show, copied from `pyproject.toml`
# and `LICENSE` by `scripts/sync_app_info.py`. Edit those and rerun the script;
# `tests/scripts/test_sync_app_info.py` fails while this file is out of date.
"""


def _copyright_line(license_text: str) -> str:
    for line in license_text.splitlines():
        if line.startswith("Copyright"):
            return line.strip()
    msg = "LICENSE has no line starting with 'Copyright': add the copyright notice"
    raise ValueError(msg)


def _toml_string(value: str) -> str:
    # The standard library writes no TOML, and a JSON string is a TOML basic string.
    return json.dumps(value, ensure_ascii=False)


def app_facts(pyproject_text: str, license_text: str) -> dict[str, str]:
    """Return the application facts, in the order `app.toml` lists them.

    The name comes from `[tool.cardiomyocytes-app]`, the copyright from the first
    line of `license_text` that starts with `Copyright`, and the rest from
    `[project]`.

    Raises:
        ValueError: If `license_text` holds no copyright line.
    """
    pyproject = tomllib.loads(pyproject_text)
    project = pyproject["project"]
    return {
        "name": pyproject["tool"]["cardiomyocytes-app"]["name"],
        "version": project["version"],
        "description": project["description"],
        "copyright": _copyright_line(license_text),
        "license": project["license"],
        "homepage": project["urls"]["GitHub"],
    }


def render(facts: dict[str, str]) -> str:
    """Return the text of an `app.toml` that holds `facts`."""
    lines = [f"{key} = {_toml_string(value)}" for key, value in facts.items()]
    return HEADER + "\n".join(lines) + "\n"


def build_app_toml() -> str:
    """Return the text `app.toml` should hold for the current project files."""
    facts = app_facts(
        PYPROJECT_PATH.read_text(encoding="utf-8"),
        LICENSE_PATH.read_text(encoding="utf-8"),
    )
    return render(facts)


def main() -> None:
    APP_TOML_PATH.write_text(build_app_toml(), encoding="utf-8", newline="\n")
    print(f"wrote {APP_TOML_PATH}")


if __name__ == "__main__":
    main()
