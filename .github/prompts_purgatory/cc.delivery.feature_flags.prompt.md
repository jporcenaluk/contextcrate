---
title: "Feature Flag Delivery Orchestrator"
summary: "Prompt for GitHub Copilot agents to implement feature toggles with progressive rollout and safety guardrails"
agent: true
audience: "Platform reliability engineers and product delivery teams"
tone: "Directive, risk-aware"
---

# Context
Feature delivery is occurring within a mature service ecosystem that serves paying customers across multiple regions. Stakeholders include product managers demanding fast iteration, reliability engineers enforcing service-level objectives, security teams requiring compliance adherence, and customer support teams needing clear rollback narratives. The deployment environment spans microservices, mobile applications, and data pipelines, each with their own telemetry and alerting stacks. Existing tooling includes a centralized feature flag service, CI/CD pipelines with automated testing, and observability platforms capturing logs, metrics, and distributed traces. Multiple release trains operate concurrently, so coordination across squads and environments (development, staging, canary, production) is essential. The agent must orchestrate work such that new capabilities can be toggled safely, audited comprehensively, and communicated crisply to both technical and non-technical stakeholders.

# Objectives
- Introduce or extend feature toggles enabling controlled exposure of functionality, with code-level hooks, configuration schemas, and lifecycle documentation.
- Engineer guardrails that enforce blast-radius limits, including fallbacks, kill switches, and monitoring thresholds tied to service-level indicators (SLIs).
- Plan and execute gradual rollout strategies (e.g., user cohorts, percentage rollouts, geo targeting) with measurable success metrics and automated rollback triggers.
- Ensure every change is testable, observable, and reversible without manual intervention beyond flipping designated toggles.
- Deliver traceable artifacts—design notes, implementation diffs, test evidence, and rollout playbooks—that allow stakeholders to audit decision making.

# Directives
1. Characterize the feature, its risk profile, dependencies, and intended user cohorts before any implementation guidance.
2. Inventory existing toggles, configuration stores, and experimentation frameworks; map how the new toggle will integrate or whether refactors are required.
3. Define a toggling taxonomy (e.g., release, ops, experiment flags) and articulate lifecycle expectations: creation, default state, ownership, deprecation plan.
4. Outline implementation steps for code instrumentation, including guard branches, configuration fetches, and safe defaults when the flag is absent or misconfigured.
5. Specify validation layers: unit tests covering both flag states, integration tests for dependency interactions, and contract tests ensuring clients degrade gracefully.
6. Detail progressive rollout sequencing across environments and cohorts, citing rollout percentages, duration, and success thresholds for promotion or rollback.
7. Mandate observability hooks: log markers, metrics dimensions, alert rules, and dashboards linked to the flag state.
8. Prescribe automated rollback playbooks, including toggling procedures, cache invalidation, message queue draining, and communication steps.
9. Instruct the agent to surface compliance or privacy considerations (e.g., data residency) when targeting user segments or geographies.
10. Require explicit human checkpoints where risk is elevated—security review, performance benchmarking, legal approvals—and define exit criteria for each.
11. Direct the agent to record reasoning, cite evidence (tests, telemetry), and flag uncertainties or data gaps requiring stakeholder input.

# Guardrails
- Never bypass existing change-management approvals; integrate with ticketing systems and release calendars.
- Disallow long-lived toggles without sunset plans; mandate documentation of cleanup tasks and deadlines.
- Prohibit hard-coded rollout logic that cannot be reversed rapidly; all toggles must be remotely configurable.
- Enforce principle of least privilege when accessing flag management APIs or secrets.
- Require accessibility and localization considerations when the toggle impacts user interfaces.
- Demand alignment with incident response policies: on-call rotation awareness, escalation matrices, and post-incident analysis requirements.

# Deliverables
- A comprehensive plan describing feature flag integration, rollout stages, and rollback contingencies, formatted as Markdown with clearly labeled subsections.
- Annotated code or pseudocode snippets illustrating toggle usage patterns, default paths, and error handling.
- Testing matrix detailing scenarios, flag states, test types, responsible owners, and pass/fail criteria.
- Observability checklist listing metrics, dashboards, alerts, and runbooks updated or created for the flag.
- Rollout timeline specifying environments, cohort definitions, percentage increments, monitoring windows, and success/failure gates.
- Communication packet summarizing launch readiness, including audience-specific messaging templates and support playbooks.

# Verification
- Confirm that every planned change has corresponding tests for both enabled and disabled flag states, including negative cases and resilience drills.
- Validate that monitoring artifacts exist and are linked to the flag identifier, with thresholds matching SLO error budgets.
- Ensure rollback pathways are documented, automated where possible, and tested in lower environments before production rollout.
- Cross-check that toggle metadata (owner, expiry date, rationale) is stored in the feature flag system and referenced in repository docs or ADRs.
- Review Markdown for structural fidelity to this template: all headings present, numbering consistent, tables or lists rendered correctly.
- Perform word-count verification (500-1000 words) and readability audit to guarantee clarity and absence of ambiguous phrasing.

# Communication
- Provide status updates at each rollout milestone, including metrics snapshots, anomalies, and decisions regarding progression or rollback.
- Notify stakeholders (product, support, reliability, security) before toggling states that impact their domains, using predefined channels (Slack, email, incident tooling).
- Escalate blockers immediately with succinct summaries of impact, attempted mitigations, and requested assistance.
- Deliver final report summarizing outcomes, telemetry, lessons learned, and flag cleanup schedule; archive in the team knowledge base.

# Reference Material
- Link to organizational feature flag guidelines, experimentation frameworks, and incident management playbooks when available.
- Cite architectural decision records, runbooks, or compliance documents that constrain rollout strategies.
- Include representative examples of successful feature flag rollouts to anchor expectations.

# Follow-up Prompts
- Request clarification on regulatory constraints (GDPR, HIPAA) affecting user cohort selection.
- Ask for historical incident data related to similar features to refine risk assessments.
- Inquire about existing experiment or analytics requirements that influence flag instrumentation.
- Confirm expectations for decommissioning the toggle once the feature stabilizes.
