---
title: "Codebase Lint and Format Enforcement"
summary: "Guidance for Copilot agents to eliminate stylistic inconsistency by orchestrating automated linting and formatting workflows."
agent: true
tone: "assertive"
audience: "software maintainers and release engineers"
format: "markdown report"
---

## Context
The repository shows diverging code styles across languages, unresolved lint warnings, and sporadic formatter usage. Release engineers have flagged review delays and regression risk caused by inconsistent whitespace, import ordering, and static-analysis violations. You operate within a CI-enabled Git project where language-specific tooling is available (e.g., ESLint + Prettier for JavaScript/TypeScript, Ruff/Black/isort for Python, gofmt/golangci-lint for Go, Clang-Format/Clang-Tidy for C/C++, rustfmt/clippy for Rust). Stakeholders include maintainers seeking deterministic diffs, QA teams requiring reproducible builds, and project managers demanding auditable change logs.

## Objectives
- Establish a coherent lint-and-format regimen tailored to the languages present, resolving all actionable findings.
- Produce commits that contain only stylistic or lint-correction changes, free from functional alterations unless strictly required to satisfy lint rules.
- Document the exact tooling versions, commands, and configuration sources employed so downstream reviewers can reproduce the results.
- Integrate verification artifacts (logs, summaries, or checklists) demonstrating that no lint or formatting errors remain.

## Directives
1. **Assess Tooling Landscape:** Inventory languages, frameworks, and existing configuration files (`package.json`, `.eslintrc.*`, `pyproject.toml`, `.prettierrc.*`, `.editorconfig`, etc.). Note gaps, overrides, or conflicting settings. Capture findings in a brief analysis section of your final report.
2. **Confirm Dependencies:** Validate tool availability through `--version` checks. If tooling is missing, document installation steps or package-manager commands. Prefer project-local configuration over ad hoc flags.
3. **Plan Remediation:** Draft a lint/format execution plan before modifying files. Sequence commands logically (formatters before linters when they auto-fix issues). Highlight any commands that must run in watch or fix mode.
4. **Automate Formatting:** Execute language-appropriate formatters (e.g., `prettier --write`, `black`, `gofmt`, `rustfmt`). Ensure commands operate on the intended scope (whole repo vs targeted directories). When formatters cannot process specific files, record the exceptions and rationale.
5. **Resolve Lint Failures:** Run lint tools with auto-fix capabilities (`eslint --fix`, `ruff --fix`, `golangci-lint run --fix`, etc.). For remaining violations requiring manual edits, update code minimally while respecting project style guides. Capture before/after reasoning for any non-trivial change.
6. **Re-run Checks:** After applying fixes, rerun all relevant linters and formatters in verification mode (e.g., `--check`, `--format-check`, `--no-fix`) to confirm a clean state. Include raw or summarized output in the deliverables.
7. **Safeguard Functional Integrity:** Execute smoke tests, unit tests, or build commands if lint rules alter code structure (imports, generated files). Note skipped tests with justification when execution is impractical.
8. **Curate Commit Scope:** Stage only stylistic diffs. Avoid bundling unrelated changes. If lint tooling surfaces defects requiring larger refactors, document blockers and stop pending product-owner approval.
9. **Prepare Reporting Artifacts:** Assemble a final Markdown report enumerating tooling used, command invocations, notable adjustments, verification outputs, outstanding issues, and recommended follow-up automation (e.g., CI job additions).
10. **Solicit Clarifications:** When encountering ambiguous or conflicting configurations, draft targeted questions for maintainers and capture them in the Communication section.

## Guardrails
- Do not modify configuration files without explicit rationale tied to lint/format success.
- Maintain existing copyright notices and license headers.
- Preserve file encodings and line endings unless configuration dictates otherwise.
- Ensure formatter application respects `.gitignore`, `.eslintignore`, and analogous ignore lists.
- Avoid suppressing lint rules globally; prefer localized overrides with justification.
- Keep generated artifacts out of version control unless the repository already tracks them.

## Deliverables
- A structured Markdown summary suitable for inclusion in a pull request, containing:
  - Tooling inventory with versions and configuration paths.
  - Executed commands with intent (e.g., "Formatted Python modules with `black .`).
  - Description of manual edits and their rationale.
  - Verification results, including clean lint/format check outputs.
  - Outstanding issues or dependencies awaiting follow-up.
- Updated source files reflecting lint and formatting corrections only.
- Optional automation proposal (CI integration, pre-commit hooks) when gaps are identified.

## Verification
- Confirm that `git status` shows only the intended stylistic changes before committing.
- Run formatter commands in `--check` or equivalent mode to ensure idempotence.
- Capture and review lint outputs, ensuring zero errors and enumerating residual warnings.
- Document test results, including command, environment notes, and pass/fail outcomes.
- Double-check that documentation and code comments remain semantically accurate post-formatting.

## Communication
- Provide interim updates after tooling assessment and post-fix verification, noting any blockers or anomalies.
- Escalate missing dependencies, permission restrictions, or configuration conflicts immediately with proposed remedies.
- When hand-offs are required, supply a concise status recap: completed commands, pending actions, and risk areas.
- Encourage maintainers to adopt automated CI checks by outlining benefits and integration steps.

## Reference Material
- ESLint Configuration Guide: https://eslint.org/docs/latest/use/configure/
- Prettier Options: https://prettier.io/docs/en/options.html
- Ruff User Guide: https://docs.astral.sh/ruff/
- Black Documentation: https://black.readthedocs.io/en/stable/
- Go Formatting Tools: https://go.dev/doc/effective_go#formatting
- Rustfmt Guide: https://rust-lang.github.io/rustfmt/
- Clang-Format Style Options: https://clang.llvm.org/docs/ClangFormatStyleOptions.html
- GitHub Actions Lint Workflow Samples: https://docs.github.com/actions/examples/using-workflows#linting-workflows
