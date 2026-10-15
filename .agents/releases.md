# Releasing `cardiomyocytes-app`

`cardiomyocytes-app` is an application and is not published; a version
marks a notable state of the project. Procedure for `X.Y.Z`:

1. Promote `CHANGELOG.md`'s `[Unreleased]` section to `[X.Y.Z]` (see
   `.agents/changelog.md`).
2. Bump `version` in `pyproject.toml`; `uv sync --group dev` to refresh
   `uv.lock`.
3. Commit `🔖 Release version X.Y.Z` (body references the `[X.Y.Z]`
   entry).
4. Tag and push:
   `git tag -a vX.Y.Z -m "🔖 Release version X.Y.Z" && git push origin vX.Y.Z`.
