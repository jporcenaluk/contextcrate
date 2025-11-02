---
title: "Prompt Generator"
summary: "Meta-prompt for architecting high-fidelity GitHub Copilot agent-mode prompts"
mode: agent
model: claude-haiku-4.5
tools:
  - view
  - create
  - edit
  - bash
  - github-mcp-server
agent: true
---

# Objective
Architect a GitHub Copilot agent-mode prompt stored at `.github/prompts/{name}.prompt.md` that orchestrates software-engineering tasks with surgical precision, harnessing Microsoft prompt-engineering tenets.

# Key Principles
- **Lexical precision:** Harness the full breadth of English vocabulary (177,000+ words) to articulate intent with surgical clarity. Supplant verbose approximations with the singular, most exacting term. Prioritize specificity over generality—each word must bear semantic weight.
- **Domain specialization:** Calibrate every prompt for software engineering, DevOps, security, data science, machine learning, or cognate technical disciplines. Eschew generic problem-solving patterns in favor of domain-specific protocols.
- **Agent orchestration:** Ensure the generated prompt unambiguously delineates agent responsibilities, requisite context, decision heuristics, and mandated outputs. Leave no ambiguity in scope boundaries or success criteria.
- **Microsoft prompt-engineering tenets:**
  - Establish scenario, objectives, and constraints antecedent to procedural directives.
  - Decompose intricate workflows into sequenced, numbered actions; enumerate prerequisite artifacts with explicit traceability.
  - Furnish exemplars, input templates, and authoritative references where they disambiguate expectations.
  - Mandate transparent reasoning, source attribution, and comprehensive outcome synthesis.
- **Response customization:** Leverage frontmatter fields (`mode`, `model`, `tools`, `style`, `tone`, `audience`, `format`) or embedded directives that calibrate Copilot responses for distinct stakeholder cohorts and communication modalities.
- **Markdown rigor:** Produce syntactically valid Markdown eschewing superfluous code fences; deploy headings, tables, enumerations, and callouts to amplify cognitive accessibility.

# Required Sections in Generated Prompts
1. **Frontmatter** encompassing `title`, `summary`, `mode: agent`, `model: claude-haiku-4.5`, `tools`, and `agent: true`. Enumerate applicable tools (e.g., `view`, `edit`, `bash`, `github-mcp-server`, `playwright-browser`). Augment with response customization keys (`style`, `tone`, `audience`, `format`) where they enhance stakeholder alignment.
2. **Context** delineating the operational scenario, stakeholder taxonomy, environmental constraints, and tacit assumptions. Illuminate dependencies, access boundaries, and regulatory obligations.
3. **Objectives** articulating the terminal state with quantifiable success metrics, acceptance criteria, and exit conditions. Each objective must be measurable and verifiable.
4. **Directives** furnishing sequenced, numbered imperatives employing decisive action verbs. Mandate prerequisite validations, artifact provenance, and escalation protocols. Each directive must be atomic and actionable.
5. **Guardrails** enumerating constraints, compliance mandates, security postures, and quality gates. Codify non-negotiable boundaries and escalation thresholds.
6. **Deliverables** specifying output artifacts with exacting formats, validation schemas, and evaluative criteria. Distinguish primary artifacts from ancillary documentation.
7. **Verification** detailing validation protocols, test matrices, and review checklists the agent must execute prior to completion. Include command invocations, expected outcomes, and failure remediation paths.
8. **Communication** explicating progress cadences, escalation channels, and reporting formats. Define information granularity for distinct stakeholder tiers.
9. **Reference Material** (optional) linking authoritative documentation, architectural decision records, style guides, or canonical exemplars that expedite execution.

# Style Requirements
- Deploy typographic emphasis (bold, italic) judiciously to spotlight non-negotiable directives or pivotal concepts.
- Privilege enumerations, tables, and callouts for information-dense technical content, optimizing cognitive load distribution.
- Eschew hedging constructs; mandate assertive, imperative phrasing that brooks no ambiguity.
- Maintain instruction concision while ensuring exhaustive coverage—each directive must be self-contained yet interconnected.
- Explicitly reference personas, tooling ecosystems, or collaboration protocols when they materially influence tonal calibration or content architecture.
- Enumerate follow-up interrogatives the agent must pose when requirements exhibit ambiguity, ensuring bidirectional clarity.

# Validation Checklist
Antecedent to prompt finalization, corroborate that it:
- Targets a discrete software-engineering scenario with unambiguous boundaries.
- Employs domain lexicon with terminological precision and semantic consistency.
- Articulates success metrics, acceptance criteria, and prescribed response architectures without equivocation.
- Maintains self-sufficiency, eschewing external prompt template dependencies absent explicit contextual provisioning.
- Preserves Markdown syntactic integrity, avoiding document-spanning code fence encapsulation.
- Exploits response customization fields (`mode`, `model`, `tools`, `style`, `tone`, `audience`, `format`) to fortify stakeholder alignment.
- Enumerates appropriate tools comprehensively—prefer surfeit to scarcity; provision more rather than fewer when uncertain.

# Output Format
Emit **exclusively** the completed Markdown prompt content. Suppress extraneous commentary, preambles, or document-enclosing code fences. The artifact must be deployment-ready without post-processing.
