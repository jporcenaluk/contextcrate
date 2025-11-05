---
title: "Dependency Upgrade Delivery"
summary: "Operational prompt for agents executing scoped dependency upgrade initiatives"
agent: true
tone: "Decisive, technically rigorous"
audience: "Senior software engineers, release managers"
format: "Markdown report with enumerated sections"
---

## Context
The platform maintains multiple services, libraries, and deployment artifacts whose reliability depends on curated third-party dependencies. Security advisories, vendor support windows, and performance regressions necessitate disciplined upgrade cadences. The requesting stakeholder is the Release Engineering lead, who requires a deterministic upgrade proposal and execution plan that accounts for cross-service compatibility, observability alignment, and rollback readiness. The delivery environment spans Git-managed repositories, automated CI/CD pipelines, IaC-managed infrastructure, and observability stacks (logging, tracing, metrics). Historical incidents show that unvetted version jumps disrupt downstream consumers, so every decision must be evidence-backed and version-pinned before execution.

## Objectives
- Produce a dependency upgrade plan covering scope, version targets, migration considerations, validation strategy, and fallback contingencies.
- Justify version selections using changelog analysis, semantic versioning expectations, vendor lifecycle data, and known security bulletins.
- Deliver actionable implementation steps that minimize service downtime, including configuration updates, code refactors, and schema migrations where relevant.
- Ensure the final output equips the Release Engineering lead to schedule the upgrade confidently and communicate risk posture to stakeholders.

## Directives
1. **Inventory Scope**: Enumerate the repositories, services, and packages under review. Clarify runtime environments (language versions, build tools, package managers) and call out transitive dependencies that may be implicitly affected.
2. **Assess Drivers**: Gather motivations such as CVEs, EOL timelines, feature adoption, or performance tuning. Cite official advisories, vendor documentation, or internal incident reports and attach permalinks where available.
3. **Evaluate Candidate Versions**: For each dependency, compare the current version with stable releases. Highlight semantic deltas (patch/minor/major), compatibility notes, deprecated APIs, and required platform prerequisites. Include a decision matrix that recommends the target version and justifies alternative rejections.
4. **Design Migration Steps**: Draft sequential implementation tasks encompassing code modifications, configuration updates, infrastructure changes, and data migration needs. Map each task to owning teams, prerequisite approvals, and estimated effort. Emphasize automation opportunities (scripts, linters, codemods) that reduce manual toil.
5. **Testing Strategy**: Define mandatory validation layers—unit, integration, contract, performance, security scans, and chaos experiments where pertinent. Specify test data requirements, staging environment parity expectations, and success/failure gates. Document how to monitor metrics, logs, and alerts before, during, and after deployment.
6. **Deployment and Rollback Plan**: Outline rollout sequencing (canary, blue/green, feature flags), communication checkpoints, and runbooks for immediate rollback. Detail artifact version pinning, database backup procedures, and configuration toggles needed to revert safely.
7. **Risk Register**: Compile risks with probability, impact, detection method, mitigation strategy, and contingency actions. Include cross-team dependencies, regulatory considerations, and change-freeze calendars that could block execution.
8. **Follow-up Questions**: List any ambiguities requiring stakeholder clarification (e.g., environment availability, maintenance windows, contractual SLAs) and recommend default assumptions if answers remain pending.

## Guardrails
- Adhere to organization security policies, coding standards, and change-management protocols (CAB approvals, incident response SLAs).
- Maintain reproducibility: document commands with exact flags, hashes, and environment variables.
- Avoid speculative tooling. Reference only vetted package sources, signed artifacts, and documented configuration paths.
- Prohibit direct modification of production environments; all changes flow through pipeline automation with peer review.
- Present all timelines in ISO 8601 format and align with the current release calendar.
- Flag any dependencies that require legal or licensing review before adoption.

## Deliverables
- **Upgrade Overview Table** summarizing each dependency, current version, proposed version, rationale, migration complexity, and owners.
- **Implementation Playbook** enumerating tasks, responsible parties (RACI), expected duration, and acceptance criteria.
- **Testing Checklist** referencing CI jobs, manual test cases, and monitoring dashboards with links or identifiers.
- **Rollback Runbook** describing triggers, reversal steps, validation post-rollback, and communication recipients.
- **Risk and Mitigation Register** highlighting blockers, mitigations, and contingency status.
- **Open Questions Log** capturing outstanding information needs and target resolution dates.

## Verification
- Confirm that every dependency in scope has an explicit version recommendation backed by at least one authoritative source (release notes, advisory, or vendor matrix).
- Validate that migration tasks cover both application code and infrastructure touchpoints, including IaC templates and deployment manifests.
- Ensure the testing strategy spans pre-commit, pre-deploy, and post-deploy validations with clear exit criteria.
- Dry-run critical scripts or commands in a sandbox environment and record outcomes, including logs or screenshots as evidence.
- Cross-check rollback steps against documented disaster recovery procedures and verify that backups or snapshots exist and are current.
- Peer-review the entire prompt output with a senior engineer or architect for technical completeness before final submission.

## Communication
- Provide an executive summary for the Release Engineering lead, highlighting scope, expected timelines, and confidence levels.
- Schedule sync points with service owners before implementation, during rollout, and post-deployment to confirm readiness and capture lessons learned.
- Broadcast status via the agreed channel (e.g., Slack #release-upgrades) using standardized message templates that include risk posture and next actions.
- Escalate blockers immediately to the on-call release manager and document escalation paths, including after-hours contact information.
- Archive final artifacts, logs, and approvals in the designated knowledge base with traceable links for audit purposes.

## Reference Material
- Vendor release notes, migration guides, and security advisories for the target dependencies.
- Internal engineering playbooks covering change management, observability dashboards, and rollback procedures.
- CI/CD pipeline documentation detailing promotion workflows, artifact repositories, and feature flag management.
- Architecture decision records (ADRs) or design docs that constrain dependency selections or platform compatibility.
