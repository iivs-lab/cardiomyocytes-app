from __future__ import annotations

__all__ = (
    "LICENSE_DATA_PATH",
    "PackageLicense",
    "collect_package_licenses",
    "dump_package_licenses",
    "load_package_licenses",
    "python_license",
)

import json
import platform
import re
from dataclasses import asdict, dataclass
from importlib.metadata import PackageNotFoundError, distribution
from pathlib import Path
from typing import TYPE_CHECKING, Final

from iivs_cardio_app.metadata import RUNTIME_DISTRIBUTIONS

if TYPE_CHECKING:
    from collections.abc import Iterable
    from importlib.metadata import Distribution

# The About dialog reads this file rather than the installed metadata, which a compiled
# build cannot read reliably; `python -m iivs_cardio_app.licenses` rewrites it.
LICENSE_DATA_PATH: Final[Path] = Path(__file__).with_name("license_data.json")

_REQUIREMENT_NAME: Final = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")
_EXTRA_MARKER: Final = re.compile(r"\bextra\s*==")
_LICENSE_FILE_NAME: Final = re.compile(r"licen[cs]e|copying|notice", re.IGNORECASE)
# The Qt wheels ship only the terms of a commercial Qt license, which the application
# does not use; showing them would suggest it does.
_UNUSED_LICENSE_FILE_NAME: Final = re.compile(r"commercial", re.IGNORECASE)


@dataclass(frozen=True, slots=True)
class PackageLicense:
    """The license of one component the application ships with.

    Args:
        name: The distribution name, as its metadata spells it.
        version: The installed version.
        license: An SPDX expression or a license name; `"Unknown"` when the metadata
            names none.
        texts: The license documents the distribution ships, in path order, except
            commercial terms the application does not use; empty when there are
            none.
    """

    name: str
    version: str
    license: str
    texts: tuple[str, ...] = ()


def _normalize(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _license_name(dist: Distribution) -> str:
    metadata = dist.metadata
    for field in ("License-Expression", "License"):
        value = (metadata.get(field) or "").strip()
        # Older metadata may put the whole license text into `License`.
        if value and "\n" not in value:
            return value

    names = [
        classifier.rsplit(" :: ", 1)[-1]
        for classifier in metadata.get_all("Classifier") or ()
        if classifier.startswith("License :: ")
    ]
    return ", ".join(names) or "Unknown"


def _license_texts(dist: Distribution) -> tuple[str, ...]:
    texts: list[str] = []
    for path in sorted(dist.files or (), key=str):
        if not _LICENSE_FILE_NAME.search(path.name):
            continue
        if _UNUSED_LICENSE_FILE_NAME.search(path.name):
            continue
        try:
            texts.append(path.read_text(encoding="utf-8"))
        except OSError, UnicodeDecodeError:
            continue
    return tuple(texts)


def _required_names(dist: Distribution) -> list[str]:
    names: list[str] = []
    for requirement in dist.requires or ():
        if _EXTRA_MARKER.search(requirement):
            continue
        if match := _REQUIREMENT_NAME.match(requirement):
            names.append(match.group())
    return names


def collect_package_licenses(roots: Iterable[str]) -> list[PackageLicense]:
    """Collect the licenses of `roots` and of every installed distribution they need.

    Requirements behind an extra are skipped, and so is any distribution that is not
    installed, such as one an environment marker leaves out. The result is sorted by
    name.
    """
    seen: set[str] = set()
    licenses: list[PackageLicense] = []
    pending = list(roots)
    while pending:
        name = pending.pop()
        if (key := _normalize(name)) in seen:
            continue
        seen.add(key)

        try:
            dist = distribution(name)
        except PackageNotFoundError:
            continue
        licenses.append(
            PackageLicense(
                name=dist.name,
                version=dist.version,
                license=_license_name(dist),
                texts=_license_texts(dist),
            ),
        )
        pending.extend(_required_names(dist))

    return sorted(licenses, key=lambda item: _normalize(item.name))


def python_license() -> PackageLicense:
    """Describe the Python runtime the application runs on."""
    return PackageLicense(
        name="Python",
        version=platform.python_version(),
        license="PSF-2.0",
    )


def dump_package_licenses(licenses: Iterable[PackageLicense]) -> str:
    """Render `licenses` as the JSON text that `load_package_licenses` reads back."""
    records = [asdict(package) for package in licenses]
    return json.dumps(records, ensure_ascii=False, indent=2) + "\n"


def load_package_licenses(path: Path = LICENSE_DATA_PATH) -> list[PackageLicense]:
    """Read the package licenses that `dump_package_licenses` wrote to `path`."""
    records = json.loads(path.read_text(encoding="utf-8"))
    return [
        PackageLicense(
            name=record["name"],
            version=record["version"],
            license=record["license"],
            texts=tuple(record["texts"]),
        )
        for record in records
    ]


if __name__ == "__main__":
    licenses = collect_package_licenses(RUNTIME_DISTRIBUTIONS)
    LICENSE_DATA_PATH.write_text(
        dump_package_licenses(licenses),
        encoding="utf-8",
        newline="\n",
    )
