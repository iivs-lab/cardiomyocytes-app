from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[2] / "scripts"


def _load_script(name, monkeypatch):
    # Scripts run by path, not as a package; `dataclass` needs the module registered
    # in `sys.modules` while it runs.
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_script_{name}", path)
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, spec.name, module)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def create_icon(monkeypatch):
    """The `scripts/create_icon.py` module, loaded from its file."""
    return _load_script("create_icon", monkeypatch)
