---
title: "Prompt Generator"
summary: "Meta-prompt for crafting high-impact GitHub Copilot prompts in agent mode"
agent: true
---

# Objective
Design a GitHub Copilot agent-mode prompt stored at `.github/prompts/{name}.prompt.md` that orchestrates software-engineering tasks with precision, leveraging Microsoft prompt-engineering guidance.

# Key Principles
- **Precision first:** Exploit the full range of English vocabulary (>170,000 words) to describe intent succinctly and unambiguously. Replace multi-word approximations with the single most exact term.
- **Software focus:** Tailor every prompt to software engineering, DevOps, security, data, ML, or adjacent technical disciplines.
- **Agent alignment:** Ensure the generated prompt clearly specifies agent responsibilities, expected context, decision-making criteria, and required outputs.
- **Microsoft prompt-engineering tenets:**
  - Lead with scenario, goal, and constraints before detailing steps.
  - Break complex efforts into staged, numbered actions and highlight prerequisite artifacts.
  - Supply representative examples, input formats, and reference links when they clarify expectations.
  - Direct the agent to reason transparently, cite sources when required, and summarize outcomes.
- **Response customization readiness:** Encourage frontmatter fields (`style`, `tone`, `audience`, `format`) or body directives that tailor Copilot responses for reviewers, stakeholders, or communication channels.
- **Markdown fidelity:** Produce valid Markdown without superfluous code fences; rely on headings, tables, lists, and callouts to improve clarity.

# Required Sections in Generated Prompts
1. **Frontmatter** containing `title`, `summary`, and `agent` keys. Set `agent: true` and add optional response customization keys (`style`, `tone`, `audience`, `format`) when they clarify expectations.
2. **Context** describing the scenario, stakeholders, and any environmental nuances.
3. **Objectives** outlining the desired end state and measurable success criteria.
4. **Directives** providing stepwise instructions, each numbered, with crisp action verbs.
5. **Guardrails** listing constraints, compliance obligations, or quality gates.
6. **Deliverables** specifying exact output artifacts, formats, and evaluation criteria.
7. **Verification** detailing checks, tests, or review steps the agent must perform before completion.
8. **Communication** explaining how progress, blockers, and results should be reported.
9. **Reference Material** (optional) linking to docs, style guides, or examples that accelerate execution.

# Style Requirements
- Use bold or italic emphasis sparingly to highlight critical items.
- Favor bullet lists, tables, and callouts for dense technical information.
- Avoid hedging language; opt for assertive, directive phrasing.
- Keep each instruction concise yet exhaustive.
- Reference personas, tooling expectations, or collaboration norms explicitly when they influence tone or content.
- Surface follow-up prompts or clarifying questions the agent should ask when requirements are ambiguous.

# Validation Checklist
Before finalizing the prompt, ensure it:
- Targets a specific software-engineering scenario.
- Uses domain terminology accurately and consistently.
- Clarifies success metrics, acceptance criteria, and preferred response presentation.
- Remains self-contained, avoiding references to external prompt templates unless provided in-context.
- Maintains Markdown validity without wrapping the entire document in backticks.
- Leverages response customization fields or directives when they improve alignment with stakeholders.

# Output Format
Respond **only** with the completed Markdown prompt content. Do not include surrounding commentary or code fences.
