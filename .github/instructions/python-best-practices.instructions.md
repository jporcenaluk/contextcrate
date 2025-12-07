---
applyTo: "**/*.py"
---
# Python Best Practices (2025)

You are an expert Python developer in 2025. Follow these guidelines when writing or refactoring Python code.

## 1. Modern Tooling & Configuration
- **Linter/Formatter**: Assume `ruff` is used for both linting and formatting. Adhere to its default rules unless specified otherwise.
- **Package Management**: Prefer `uv` or `poetry` over raw pip/requirements.txt. Look for `pyproject.toml` for configuration.
- **Type Checking**: Use strict type hints compatible with `mypy` or `pyright`.

## 2. Coding Standards
- **Type Hints**: All function arguments and return values must be typed. Use built-in generics (`list[str]`, `dict[str, int]`) instead of `typing.List`.
  - Use `typing.Self` for methods returning the instance.
  - Use `|` for unions (e.g., `str | None` instead of `Optional[str]`).
- **Data Classes**: Prefer `pydantic.BaseModel` for data validation and settings. Use standard `@dataclass` only for simple internal structures.
- **Async**: Prefer `asyncio` for I/O-bound operations. Use `anyio` if cross-compatibility is needed.
- **Path Handling**: Always use `pathlib.Path`, never `os.path`.

## 3. Testing
- **Framework**: Use `pytest`.
- **Fixtures**: Use `conftest.py` for shared fixtures.
- **Async Tests**: Use `pytest-asyncio` for async test functions.

## 4. Documentation
- Use Google-style docstrings.
- Include type information in function signatures, not in docstrings.
