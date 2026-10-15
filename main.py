from __future__ import annotations

import sys

from iivs_cardio_app.shell import main

# The build entry point: pyside6-deploy reads `[tool.pyside6.deploy]` only from the
# `pyproject.toml` beside its input file, so this file stays in the project root.
if __name__ == "__main__":
    sys.exit(main())
