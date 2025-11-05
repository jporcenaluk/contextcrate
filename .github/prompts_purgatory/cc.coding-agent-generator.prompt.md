---
title: "Coding Agent Prompt Generator"
summary: "Meta-prompt for crafting GitHub Copilot coding agents with robust workflows and safeguards"
agent: true
---

# Objective
Author a GitHub Copilot coding-agent prompt stored at `.github/prompts/{name}.prompt.md` that orchestrates autonomous implementation work while adhering to GitHub's coding-agent lifecycle guidance.

# Context
The agent will:
- Consume repository context (code, tests, docs) supplied by the developer.
- Plan and execute multi-step coding tasks, handing off results via pull requests or patches.
- Collaborate with maintainers by narrating reasoning, surfacing risks, and requesting clarifications when requirements are ambiguous.

# Objectives
- Deliver production-ready code that satisfies functional, performance, and security expectations.
- Maintain traceability between requirements, implementation steps, and verification evidence.
- Optimize for developer productivity by minimizing back-and-forth while preserving reviewability.

# Directives
1. Enumerate the scenario, stakeholders, and environmental assumptions before describing actions.
2. Define the agent's responsibilities across the full coding lifecycle: requirement digestion, solution design, implementation, validation, documentation, and handoff.
3. Break the workflow into numbered stages with clear entry/exit criteria and required artifacts per stage.
4. Specify how the agent gathers context (files, commands, telemetry) and when it must pause for human input.
5. Detail quality gates covering unit/integration tests, static analysis, security checks, and documentation updates.
6. Instruct the agent to produce transparent reasoning, cite sources, and summarize decisions in every response.
7. Include contingency guidance for blockers, missing dependencies, or conflicting requirements.

# Guardrails
- Enforce compliance with repository coding standards, security practices, and change-management policies.
- Prohibit speculative feature work; keep scope aligned with explicit user requests.
- Require confirmation before destructive operations (e.g., force pushes, mass refactors).
- Mandate adherence to the Microsoft prompt-engineering principles for structure and clarity.

# Deliverables
- A single Markdown prompt containing validated frontmatter and the sections above, free of extraneous commentary.
- Clearly labeled subsections for context, objectives, directives, guardrails, deliverables, verification, communication, and reference material (if used).

# Verification
- Confirm that success metrics and acceptance criteria are measurable and testable.
- Ensure each workflow stage lists the validation steps or commands the agent must execute.
- Validate Markdown formatting and absence of code fences around the entire document.

# Communication
- Define how the coding agent reports progress, escalates issues, and formats final summaries for maintainers.
- Provide expectations for citing file paths, command outputs, and test results within responses.

# Reference Material (optional)
Link to relevant engineering playbooks, style guides, security checklists, or architectural decision records when they sharpen execution.

# Follow-up Prompts
List clarifying questions the agent should ask when requirements, dependencies, or acceptance criteria are unclear.
