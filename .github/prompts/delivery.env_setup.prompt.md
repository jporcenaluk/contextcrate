---
title: "Environment Provisioning Delivery"
summary: "Directive for engineering agents to produce reproducible environment setup scripts, container definitions, and onboarding documentation"
mode: agent
model: claude-haiku-4.5
tools:
  - view
  - create
  - edit
  - bash
  - github-mcp-server-list_workflow_runs
  - github-mcp-server-list_workflow_jobs
  - github-mcp-server-get_workflow_run
  - github-mcp-server-get_job_logs
  - report_progress
agent: true
audience: "DevOps engineers and platform maintainers"
tone: "assertive, authoritative"
style: "structured, reference-ready"
format: "Markdown with sectioned deliverables"
---

# Context
The target product team is onboarding new developers and external contributors to a polyglot service platform that spans web, data processing, and background job workloads. The infrastructure is currently fragmented across ad-hoc local scripts, inconsistent container images, and undocumented cloud prerequisites. You must consolidate environment setup into a cohesive delivery package that functions on macOS, Windows (WSL2), and mainstream Linux distributions while remaining CI-compatible.

Stakeholders include:
- **Platform maintainers** who require hardened, auditable provisioning processes.
- **Application developers** needing fast, deterministic onboarding with minimal manual effort.
- **Security reviewers** verifying that dependencies and credentials adhere to organizational controls.
- **Release engineering** teams integrating environment initialization into automated pipelines.

# Objectives
- Deliver a **turnkey environment setup suite** that standardizes local, CI, and containerized workflows.
- Capture every prerequisite, dependency, and configuration artifact so that a new contributor becomes productive within one work session.
- Ensure scripts are idempotent, cross-platform, and emit actionable diagnostics when assumptions are unmet.
- Provide documentation that enumerates architecture decisions, validation steps, and troubleshooting playbooks.

# Directives
1. **Inventory prerequisites**: enumerate operating system requirements, package managers, system dependencies, required environment variables, and external service accounts. Document alternative paths (e.g., Homebrew vs. apt) and version pins.
2. **Author provisioning scripts**: create shell or PowerShell scripts (prefer POSIX shell plus Windows-compatible variants) that install dependencies, configure secrets management, and set up local databases. Scripts must support non-interactive execution with flags for dry-run and verbose logging.
3. **Define container strategy**: produce Dockerfiles for development and CI that reuse a base image where feasible. Specify build arguments, multi-stage builds, health checks, and entrypoints aligned with project workflows.
4. **Create orchestration templates**: where multi-service coordination is necessary, provide docker-compose or equivalent manifests with service definitions, volumes, networks, and resource constraints.
5. **Integrate with CI/CD**: prescribe how setup scripts and Dockerfiles plug into existing pipelines (GitHub Actions, Azure Pipelines, or similar). Include matrix considerations, cache strategies, and secrets handling.
6. **Draft onboarding documentation**: assemble a Markdown guide describing installation steps, verification commands, rollback procedures, and FAQ-style troubleshooting. Reference scripts and containers created earlier.
7. **Capture configuration reference**: compile `.env.example` templates or configuration manifests with placeholder values, explanations, and security posture notes.
8. **Embed validation hooks**: integrate linting, security scanning (e.g., trivy, bandit), and dependency auditing within scripts or pipeline instructions. Ensure failure modes are explicit and machine-parseable.
9. **Plan knowledge transfer**: recommend how updates to the environment toolkit are versioned, reviewed, and communicated. Include changelog expectations and review gates.

# Guardrails
- Prefer declarative approaches (infrastructure-as-code, container orchestrations) over manual instructions whenever feasible.
- Scripts must avoid destructive operations unless explicitly flagged and confirmed. Provide rollback or cleanup commands.
- Assume contributors lack elevated privileges; document when admin rights are unavoidable and provide alternatives.
- Enforce reproducibility by pinning tool versions, capturing checksums, and referencing immutable artifact sources.
- Maintain compatibility with air-gapped or proxied networks; note fallback mechanisms for artifact downloads.
- Do not embed secrets. Instead, describe secure retrieval patterns (vault integrations, SSM parameters) and redaction practices for logs.

# Deliverables
- **Provisioning scripts**: `scripts/setup-local.sh`, `scripts/setup-ci.sh`, and if required `scripts/setup-windows.ps1`, each annotated with usage instructions and exit codes.
- **Container definitions**: `Dockerfile.dev`, `Dockerfile.ci`, and optional language-specific variants. Include `.dockerignore` updates and build instructions.
- **Orchestration manifest**: `docker-compose.dev.yml` or equivalent, accompanied by service diagrams or tables summarizing dependencies.
- **Configuration templates**: `.env.example`, `config/README.md`, and secrets handling notes.
- **Documentation bundle**: `docs/onboarding.md` covering quickstart, deep-dive setup, validation checklist, troubleshooting, architecture overview, and glossary. Supplement with `docs/setup-FAQ.md` if complex edge cases exist.
- **Verification scripts or pipeline snippets**: automated checks ensuring environment integrity (e.g., smoke tests, schema migrations, lint suites) with instructions for local execution and CI integration.

# Verification
- Enumerate automated commands to confirm successful provisioning (e.g., `scripts/setup-local.sh --verify`, `docker compose ps`, test suites). Provide expected outputs and remediation guidance for common failures.
- Include a self-review checklist covering dependency freshness, container scan results, script idempotence, and documentation accuracy.
- Recommend peer review criteria: reproducibility, security posture, alignment with infrastructure standards, and developer experience metrics.
- Specify how to capture evidence (logs, screenshots, CI artifacts) that the environment setup works across supported platforms.

# Communication
- Outline progress reporting cadence, including daily status summaries and blockers communicated via designated collaboration tools.
- Define escalation paths for security or compliance concerns uncovered during setup work.
- Provide templates for onboarding announcements and update notes when environment tooling changes.
- Encourage proactive solicitation of feedback from new joiners and integration of their findings into continuous improvements.

# Reference Material
- Link to existing organizational infrastructure guidelines, security baselines, or SRE runbooks if available.
- Cite authoritative docs for tooling used (Docker, package managers, cloud CLIs) to ensure maintainers can verify instructions.
- Include sample repositories or canonical implementations that exemplify high-quality environment setup practices.

# Clarifying Questions
Direct the agent to ask for missing inputs such as cloud provider specifics, required services, access policies, or unique hardware constraints before implementation.

# Completion Criteria
The prompt is fulfilled when scripts, container assets, and documentation are delivered, reviewed, and validated against the verification checklist, and onboarding stakeholders confirm readiness for new contributors.
