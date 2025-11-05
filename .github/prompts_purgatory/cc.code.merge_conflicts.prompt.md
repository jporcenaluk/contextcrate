---
title: "Merge Conflict Mitigation Playbook"
summary: "Directive prompt for Copilot agents to analyze, prevent, and resolve Git merge conflicts with disciplined collaboration"
agent: true
style: "decisive"
tone: "assertive"
audience: "software engineers, release managers, DevOps leads"
format: "markdown"
---

# Context
Software teams are integrating feature branches into a shared mainline while operating under continuous-delivery expectations. Releases must remain stable despite parallel development, hotfixes, and automated merges triggered by CI pipelines. Stakeholders include feature engineers, code reviewers, release managers, and SREs accountable for uptime. Tooling spans Git (CLI), hosted providers (GitHub, Azure DevOps), and automation bots that may initiate merges outside working hours. Unmitigated merge conflicts delay releases, erode confidence, and can inject regressions when resolved hastily.

# Objectives
- Establish a repeatable protocol that detects conflict risk early, documents root causes, and resolves divergences without jeopardizing mainline stability.
- Ensure every merge or rebase operation concludes with validated builds, synchronized metadata, and clearly communicated status updates.
- Capture remediation insights and preventive actions in shared knowledge bases to reduce recurrence.

# Directives
1. **Inventory Context:** Enumerate branches, owners, last synchronization points, and pending pull requests. Pull the latest mainline changes locally and record the exact commit SHAs before proceeding.
2. **Diagnose Divergence:** Compare commit graphs (`git log --graph --oneline --decorate`) and inspect overlapping touch-points using `git diff --name-only`. Tag files and subsystems with high churn or criticality.
3. **Assess Impact:** Classify conflicts by severity (blocking release, blocking PR, or cosmetic) and note downstream dependencies (CI pipelines, packaging jobs, deployment windows).
4. **Select Mitigation Strategy:** Decide between merge, rebase, or cherry-pick based on branch freshness, CI requirements, and policy. Justify the choice explicitly in the work log.
5. **Execute Resolution:** Apply the chosen strategy. For manual edits, annotate conflicting regions with rationale, reconcile semantic differences, and run targeted unit/integration tests. Maintain atomic commits with descriptive messages referencing tracked issues.
6. **Validate Outcomes:** Run linting, tests, and static analysis specified in project checklists. Re-run CI workflows if preconfigured. Confirm the working tree is clean and the branch history aligns with organizational standards (e.g., linear history mandates).
7. **Document and Communicate:** Update PR descriptions, release notes, and incident trackers with conflict causes, resolution steps, and preventive recommendations. Signal completion to stakeholders via agreed channels.
8. **Propose Prevention:** Identify automation or process adjustments (e.g., shorter-lived branches, feature toggles, code ownership adjustments) and log them in retrospectives or governance boards.

# Guardrails
- Never force-push to shared branches without explicit approval from branch owners and release management.
- Preserve code review integrity: do not suppress required reviewer re-approvals after significant conflict resolutions.
- Maintain audit trails by avoiding local history rewriting unless policy allows and documentation is updated.
- Respect branch protection rules, CI gating, and security scans before finalizing merges.
- Keep communication artifacts free from sensitive data, credentials, or security findings beyond approved disclosure channels.

# Deliverables
- Updated branch with conflicts resolved, rebased or merged per policy, and all tests passing.
- Consolidated conflict report summarizing root cause, files impacted, decisions taken, and outstanding risks.
- Logged action items for future prevention, including owner, due date, and success metric.
- Confirmation message to stakeholders referencing the relevant PR, commits, and verification evidence.

# Verification
- Confirm `git status` reports a clean working tree and no unresolved paths.
- Ensure CI workflows associated with the branch have succeeded or have documented waivers.
- Validate that regression, smoke, or targeted tests executed post-resolution meet exit criteria.
- Cross-check that documentation and work logs align with actual commit history and timestamps.
- Perform peer review of the conflict resolution diff or pair-programming inspection when mandated by policy.

# Communication
- Broadcast progress in the primary collaboration channel (e.g., Slack, Teams) with timestamps, blockers, and next steps.
- Escalate unresolved conflicts or policy exceptions immediately to release management and the incident commander if a freeze is active.
- Provide succinct end-of-task summaries in PR threads, including verification evidence and prevention proposals.
- Schedule follow-up knowledge-sharing sessions or addenda to architecture reviews when structural changes were required to resolve the conflict.

# Reference Material
- Git documentation on merge strategies and rerere: https://git-scm.com/doc
- Organization-specific branching policy and CI requirements (link or repository path to be provided by the team).
- Post-incident retrospective template stored in the shared operations knowledge base.
