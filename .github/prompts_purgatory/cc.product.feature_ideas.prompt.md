---
title: "Product Feature Opportunity Mapper"
summary: "Prompt for product-minded Copilot agents to surface feature opportunities, address gaps, and structure ideation funnels."
agent: true
tone: "Directive, optimistic, customer-obsessed"
audience: "Product strategists and cross-functional engineering leads"
style: "Analytical narrative with prioritized bulleting"
---

# Context
Product strategists at ContextCrate seek a structured examination of the product surface area to inform the next two quarterly roadmaps. The agent operates with access to recent customer interviews, product analytics dashboards, support tickets, sales feedback, and competitive intelligence briefs. Stakeholders include product management, engineering leadership, customer success, and revenue operations, each requiring crisp insights that translate into build-measure-learn loops. The delivery must anticipate dependencies on design systems, data infrastructure, compliance policies, and GTM enablement assets.

# Objectives
- Surface high-leverage feature opportunities that align with customer pains, revenue goals, and platform differentiation.
- Expose gaps in current capabilities, workflows, or integrations that inhibit user activation, retention, or expansion.
- Construct at least two ideation funnels that channel raw ideas into validated concepts with measurable checkpoints.
- Prioritize recommendations using impact, confidence, and effort scoring, and tie them to quarterly planning horizons.
- Articulate how each proposal harmonizes with existing product architecture and operational constraints.

# Directives
1. Aggregate and summarize the most recent qualitative and quantitative signals, citing source artifacts where available, and flag signal strength or reliability.
2. Map customer journeys across acquisition, onboarding, core usage, and renewal; annotate frictions, drop-offs, or unmet jobs-to-be-done using precise product vocabulary.
3. Perform gap analysis against competitor capabilities, adjacent tools, and regulatory or standards requirements; highlight table-stakes vs. differentiators.
4. Generate a backlog of feature opportunities categorized by strategic theme (e.g., collaboration, analytics, automation) with crisp user stories and acceptance criteria.
5. Score each opportunity on impact, confidence, and effort (ICE or RICE variant) and rationalize the scoring assumptions referencing data or stakeholder input.
6. Design at least two ideation funnels, each with entry criteria, triage checkpoints, experimentation tactics, success metrics, and ownership expectations.
7. Identify technical, design, or go-to-market dependencies for each top-tier opportunity, proposing mitigation strategies or sequencing adjustments.
8. Recommend instrumentation updates, analytics dashboards, or research cadences required to validate hypotheses post-launch.
9. Summarize risks, unknowns, and follow-up questions, explicitly noting where additional discovery or stakeholder alignment is mandatory.

# Guardrails
- Keep scope within capabilities that can be prototyped or shipped within the next two quarters unless explicitly justified.
- Avoid speculative technology bets lacking supporting evidence or strategic fit.
- Preserve confidentiality markers when referencing customer accounts or proprietary metrics.
- Align terminology with existing product taxonomy, design language system, and API naming conventions.
- Ensure all frameworks or scoring models are transparent and reproducible by partner teams.

# Deliverables
- **Insight Summary:** Bullet-point synopsis of key findings from data synthesis, with signal strength tags (e.g., High, Medium, Low).
- **Opportunity Matrix:** Table listing opportunity name, user segment, pain addressed, ICE/RICE scores, estimated timeframe, and required stakeholders.
- **Ideation Funnels:** Two structured funnels presented as stepwise lists or tables, each clarifying stage purpose, responsible roles, decision gates, and exit criteria.
- **Risk Register:** Enumerated risks with probability, impact, mitigation owner, and contingency approach.
- **Action Plan:** Sequenced next steps for the upcoming roadmap workshop, including preparatory analyses, stakeholder check-ins, and decision milestones.

# Verification
- Cross-check that every opportunity references at least one customer or data signal and that scoring assumptions are documented.
- Validate that ideation funnels cover divergent thinking, convergent prioritization, experiment execution, and retrospective learning.
- Confirm numerical scoring adds up logically, with consistent scales and definitions across entries.
- Proofread for clarity, professional tone, and alignment with ContextCrate brand voice.
- Ensure the final document stays within 500-1000 words and adheres to Markdown standards without code fences.

# Communication
- Provide an executive overview followed by drill-down sections to support both leadership briefings and working sessions.
- Highlight blockers or unanswered questions in a dedicated callout, tagging responsible roles (e.g., "Eng Platform", "CX Insights").
- Suggest follow-up meeting cadence and documentation channels (e.g., product brief, PRD, shared workspace) for sustaining momentum.
- Offer tailored talking points for cross-functional partners when socializing the recommendations.

# Reference Material
- Latest customer NPS and churn analysis dashboards.
- Design language system guidelines and component inventory.
- Prior roadmap retrospectives and launch postmortems from the last 12 months.
- Competitive intelligence briefs covering top five market rivals and emerging entrants.

