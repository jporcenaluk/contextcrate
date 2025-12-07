# Plan: Interactive "Hey!/What?" Web UI Feature

## Overview
Add a simple web UI to plan-test-project that displays "hey!" when opened, and toggles to "what?" when clicked. The solution uses test-driven development (TDD) and provides a single command to launch the UI locally.

## Goals
- Add a minimal web server using Flask (lightweight, well-tested, simple)
- Create an interactive web page with click-to-toggle behavior
- Implement tests FIRST following TDD principles
- Provide one-command startup via `uv run serve` or similar

## Technology Choices
- **Flask**: Minimal Python web framework, fits project's Python-only stack
- **pytest + Flask test client**: For backend route testing
- **playwright/selenium OR simple fetch-based tests**: For UI interaction testing
- **Vanilla JavaScript**: No framework needed for simple toggle

## Work Breakdown

### Epic: Test Infrastructure (suggested id: hey-tests)
Set up the testing infrastructure before implementing features (TDD approach).

#### Tasks:
1. **Add web dependencies to pyproject.toml** (suggested id: hey-tests-1)
   - Dependencies: None
   - Description: Add Flask and pytest-playwright (or similar) to project dependencies. Flask goes in main deps, testing tools go in dev deps.
   - Acceptance:
     - Flask added to `[project.dependencies]`
     - pytest-playwright or equivalent added to `[project.optional-dependencies.dev]`
     - `uv sync` completes successfully
   - Files: `plan-test-project/pyproject.toml`
   - Estimate: 5 minutes

2. **Write failing test for /hey route** (suggested id: hey-tests-2)
   - Dependencies: hey-tests-1
   - Description: Create a test file `tests/test_web.py` that tests the `/` route returns HTML containing "hey!". Use Flask's test client. This test should FAIL initially (TDD red phase).
   - Acceptance:
     - Test file exists at `tests/test_web.py`
     - Test imports app from `plan_test_project.web`
     - Test checks GET `/` returns 200 status
     - Test checks response contains "hey!"
     - Test FAILS when run (no implementation yet)
   - Files: `plan-test-project/tests/test_web.py`
   - Estimate: 10 minutes

3. **Write failing test for toggle behavior** (suggested id: hey-tests-3)
   - Dependencies: hey-tests-1
   - Description: Add a test that verifies clicking the text toggles between "hey!" and "what?". This can be a playwright browser test or a simpler test checking the JavaScript is present and correct in the HTML response.
   - Acceptance:
     - Test verifies toggle JavaScript/behavior exists
     - Test checks both states are achievable
     - Test FAILS initially
   - Files: `plan-test-project/tests/test_web.py`
   - Estimate: 15 minutes

### Epic: Web Implementation (suggested id: hey-impl)
Implement the Flask app and HTML/JS to make tests pass.

#### Tasks:
1. **Create Flask app with / route** (suggested id: hey-impl-1)
   - Dependencies: hey-tests-2
   - Description: Create `src/plan_test_project/web.py` with a Flask app. Add a `/` route that returns HTML with "hey!" displayed. This makes the first test pass (TDD green phase).
   - Acceptance:
     - `web.py` exists with Flask app
     - GET `/` returns HTML with "hey!" visible
     - Test `hey-tests-2` passes
   - Files: `plan-test-project/src/plan_test_project/web.py`
   - Estimate: 10 minutes

2. **Add toggle JavaScript** (suggested id: hey-impl-2)
   - Dependencies: hey-impl-1, hey-tests-3
   - Description: Add inline JavaScript to the HTML template that toggles the displayed text between "hey!" and "what?" on click. Use a simple click event listener.
   - Acceptance:
     - Clicking "hey!" changes it to "what?"
     - Clicking "what?" changes it back to "hey!"
     - All tests pass
   - Files: `plan-test-project/src/plan_test_project/web.py`
   - Estimate: 10 minutes

3. **Add serve command/entry point** (suggested id: hey-impl-3)
   - Dependencies: hey-impl-2
   - Description: Add a CLI entry point or script so users can run `uv run serve` (or `uv run python -m plan_test_project.web`) to start the dev server. Update pyproject.toml with scripts section if needed.
   - Acceptance:
     - Single command starts the web server
     - Server runs on localhost:5000 (or similar)
     - Browser can access and interact with the page
   - Files: 
     - `plan-test-project/pyproject.toml`
     - `plan-test-project/src/plan_test_project/web.py`
   - Estimate: 5 minutes

4. **Update README with usage instructions** (suggested id: hey-impl-4)
   - Dependencies: hey-impl-3
   - Description: Document how to install dependencies, run tests, and start the UI server.
   - Acceptance:
     - README includes install command
     - README includes test command
     - README includes serve command
     - README describes the UI behavior
   - Files: `plan-test-project/README.md`
   - Estimate: 5 minutes

## Dependency Graph

```
hey-tests-1 (Add deps)
    │
    ├──────────────────┐
    ▼                  ▼
hey-tests-2         hey-tests-3
(Route test)        (Toggle test)
    │                  │
    ▼                  │
hey-impl-1 ◄───────────┘
(Flask app)
    │
    ▼
hey-impl-2
(Toggle JS)
    │
    ▼
hey-impl-3
(Serve cmd)
    │
    ▼
hey-impl-4
(README)
```

## Execution Waves

| Wave | Tasks | Can Parallelize |
|------|-------|-----------------|
| 1 | hey-tests-1 | No (single task) |
| 2 | hey-tests-2, hey-tests-3 | Yes |
| 3 | hey-impl-1 | No (needs tests) |
| 4 | hey-impl-2 | No (sequential) |
| 5 | hey-impl-3 | No (sequential) |
| 6 | hey-impl-4 | No (sequential) |

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Playwright setup complexity | Medium | Medium | Fall back to simpler HTML/response testing |
| Flask conflicts with existing code | Low | Low | web.py is isolated module |
| TDD flow disruption | Low | Medium | Clear task ordering enforces red-green-refactor |

## Notes

- Using Flask over FastAPI for simplicity (no async complexity needed)
- Inline HTML/JS avoids template folder complexity for this simple feature
- Playwright can be optional; basic tests work with Flask test client alone
