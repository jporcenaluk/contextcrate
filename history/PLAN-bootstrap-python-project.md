# Plan: Bootstrap 'plan-test-project' Python Project

## Goal
Initialize a new Python project named `plan-test-project` within the `contextcrate` repository, adhering to modern best practices.

## Scope
- **Directory Structure**: Standard `src/` layout.
- **Dependency Management**: Use `uv` or standard `pip` + `pyproject.toml`. (Will use standard `pyproject.toml` for broad compatibility).
- **Testing**: `pytest`.
- **Linting/Formatting**: `ruff` (fast, comprehensive).
- **Type Checking**: `mypy`.

## Tasks Breakdown

1.  **Project Skeleton & Configuration**
    - Create folder `plan-test-project/`.
    - Create `pyproject.toml` with build system (hatchling or setuptools) and tool config.
    - Create `src/plan_test_project/__init__.py`.
    - Create `tests/__init__.py`.

2.  **Tooling Setup**
    - Configure `ruff` in `pyproject.toml`.
    - Configure `pytest` in `pyproject.toml`.
    - Configure `mypy` in `pyproject.toml`.

3.  **Implementation & Verification**
    - Add a simple function in `src/plan_test_project/main.py`.
    - Add a test in `tests/test_main.py`.
    - Verify `pytest` passes.
    - Verify `ruff` and `mypy` pass.

## Dependencies
- python >= 3.10
- pytest
- ruff
- mypy
