from __future__ import annotations

__all__ = ("RUNTIME_VERSIONS", "Component")

import platform
import tomllib
from dataclasses import dataclass
from importlib.resources import files
from typing import TYPE_CHECKING, Final, NotRequired, TypedDict

from PySide6.QtCore import qVersion

if TYPE_CHECKING:
    from collections.abc import Callable
    from importlib.resources.abc import Traversable


# These versions come from the running libraries, never from package metadata,
# which the built application cannot read (`AGENTS.md`).
RUNTIME_VERSIONS: Final[dict[str, Callable[[], str]]] = {
    "Python": platform.python_version,
    "Qt": qVersion,
}


class _Entry(TypedDict):
    name: str
    version: NotRequired[str]
    license: str
    homepage: str
    file: str
    note: NotRequired[str]
    bundled: NotRequired[list[_Entry]]


@dataclass(frozen=True, slots=True)
class Component:
    """A third-party component the built application ships.

    Args:
        name: The component's name, such as `"Qt"`.
        version: The shipped version; empty when nothing records it.
        license: The SPDX expression of the license it is used under.
        homepage: The component's web site.
        file: The name of its license text in the `assets/` folder.
        note: Anything else a reader should know, or an empty string.
        bundled: The components it ships inside it, such as the libraries the
            Python runtime brings along.
    """

    name: str
    version: str
    license: str
    homepage: str
    file: str
    note: str = ""
    bundled: tuple[Component, ...] = ()

    @staticmethod
    def _folder() -> Traversable:
        return files(__package__) / "assets"

    @classmethod
    def _from_entry(cls, entry: _Entry) -> Component:
        version = entry.get("version") or RUNTIME_VERSIONS.get(entry["name"], str)()
        return cls(
            name=entry["name"],
            version=version,
            license=entry["license"],
            homepage=entry["homepage"],
            file=entry["file"],
            note=entry.get("note", ""),
            bundled=tuple(cls._from_entry(child) for child in entry.get("bundled", [])),
        )

    @classmethod
    def load_all(cls) -> tuple[Component, ...]:
        """Read the top-level components listed in `licenses.toml`, in its order.

        An entry without a `version` takes it from `RUNTIME_VERSIONS`, or leaves it
        empty when the component has no entry there either.
        """
        text = (cls._folder() / "licenses.toml").read_text(encoding="utf-8")
        entries: list[_Entry] = tomllib.loads(text)["component"]
        return tuple(cls._from_entry(entry) for entry in entries)

    def read_license_text(self) -> str:
        """Return the full license text that the component is shipped under."""
        return (self._folder() / self.file).read_text(encoding="utf-8")
