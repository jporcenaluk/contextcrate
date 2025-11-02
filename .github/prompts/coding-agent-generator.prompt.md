---
title: "Coding Agent Prompt Generator"
summary: "Meta-prompt for architecting GitHub Copilot coding agents with fortified workflows and comprehensive safeguards"
mode: agent
model: claude-haiku-4.5
tools:
  - view
  - create
  - edit
  - bash
  - github-mcp-server
  - report_progress
  - code_review
  - codeql_checker
agent: true
---

# Objective
Author a GitHub Copilot coding-agent prompt stored at `.github/prompts/{name}.prompt.md` that orchestrates autonomous implementation endeavors while manifesting GitHub's coding-agent lifecycle tenets.

# Context
The agent shall:
- Assimilate repository context (codebase, test suites, documentation) furnished by the developer with comprehensive provenance tracking.
- Architect and execute multi-phase coding endeavors, delivering artifacts via pull requests or patch sets with exhaustive audit trails.
- Collaborate with maintainers through transparent reasoning narratives, proactive risk disclosure, and targeted clarification requests when requirements exhibit ambiguity.

# Objectives
- Deliver production-grade code artifacts satisfying functional correctness, performance baselines, and security postures with verifiable attestation.
- Maintain bidirectional traceability spanning requirements, implementation sequences, and validation evidence with immutable audit chains.
- Optimize developer throughput by curtailing iterative refinement cycles while preserving comprehensive reviewability and change transparency.

# Directives
1. Enumerate the operational scenario, stakeholder taxonomy, and environmental axioms antecedent to action delineation, establishing context with maximal specificity.
2. Define the agent's mandates across the comprehensive coding lifecycle: requirement assimilation, solution architecture, implementation execution, validation protocols, documentation synchronization, and stakeholder handoff with traceability preservation.
3. Decompose the workflow into sequenced, numbered phases with unambiguous entry/exit criteria and mandated artifacts per stage, ensuring atomic progression checkpoints.
4. Specify context acquisition modalities (file inspection, command execution, telemetry ingestion) and codify pause conditions necessitating human intervention with explicit escalation thresholds.
5. Articulate quality gates encompassing unit/integration test coverage, static analysis compliance, security vulnerability scanning, and documentation currency with concrete validation commands.
6. Mandate transparent reasoning exposition, authoritative source citation, and comprehensive decision synthesis in every agent response, ensuring auditability.
7. Provision contingency protocols for blockers, dependency deficits, or requirement conflicts with graduated escalation pathways and fallback strategies.

# Guardrails
- Mandate unwavering compliance with repository coding standards, security protocols, and change-management governance frameworks.
- Proscribe speculative feature elaboration; confine scope to explicit user requisitions with documented rationale for any variance.
- Necessitate explicit authorization antecedent to destructive operations (e.g., force pushes, wholesale refactorings, irreversible schema alterations).
- Codify adherence to Microsoft prompt-engineering principles governing structural coherence, lexical clarity, and stakeholder communication protocols.
- Enumerate comprehensive tool provisioning (prefer surfeit to deficit)—coding agents typically require: `view`, `create`, `edit`, `bash`, `github-mcp-server`, `report_progress`, `code_review`, `codeql_checker`.

# Deliverables
- A singular Markdown prompt artifact containing validated frontmatter (`title`, `summary`, `mode: agent`, `model: claude-haiku-4.5`, `tools`, `agent: true`) and requisite sections, devoid of extraneous commentary or meta-narrative.
- Explicitly demarcated subsections for context, objectives, directives, guardrails, deliverables, verification, communication, and reference material (when applicable), each maintaining structural and tonal consistency.

# Verification
- Corroborate that success metrics and acceptance criteria exhibit measurability and testability with concrete validation protocols.
- Ensure each workflow phase enumerates validation sequences or command invocations the agent must execute with expected outcomes documented.
- Validate Markdown syntactic integrity and absence of document-spanning code fence encapsulation.
- Confirm tool enumeration comprehensiveness—coding agents typically mandate: `view`, `create`, `edit`, `bash`, `github-mcp-server`, `report_progress`, `code_review`, `codeql_checker`, and domain-specific tools as warranted.

# Communication
- Codify progress reporting protocols, issue escalation channels, and final summary architectures for maintainer consumption with prescribed cadences and granularity.
- Enumerate citation expectations for file paths (absolute, not relative), command outputs (with exit codes), and test results (with coverage metrics) within agent responses, ensuring reproducibility.

# Reference Material (optional)
Link authoritative engineering playbooks, style guides, security checklists, or architectural decision records when they materially enhance execution precision or accelerate context assimilation.

# Follow-up Prompts
Enumerate targeted interrogatives the agent must pose when requirements, dependencies, or acceptance criteria manifest ambiguity, ensuring bidirectional clarity establishment antecedent to implementation commencement.
