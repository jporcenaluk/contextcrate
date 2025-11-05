# Context Crate

Context Crate is a curated library of prompts, agents, meta-prompts, and operating instructions designed to supercharge GitHub Copilot users. By assembling reusable patterns for planning, coding, reviewing, and coordinating work, the crate enables teams to consistently deliver high-quality software faster.

## Why it exists
- **2x Throughput:** Each artifact is engineered to help Copilot act as a force multiplier, aiming to boost individual productivity by roughly 2× through sharper task decomposition and decision support.
- **Composable Structure:** Chatmodes x prompts x customization x context x steering are intended to be combined to create strong guardrails and allow your creativity to come to the fore.
- **Operational Consistency:** Shared guidance keeps cross-functional collaborators aligned on communication norms, quality gates, and verification steps.

## Repository Structure
- `README.md`: Overview of the Context Crate mission and structure.
- `.github/agents/`: Agents that instruct Copilot how to operate completely autonomously.
- `.github/prompts/`: Prompts that instruct Copilot to operate with one hand on the wheel.

## The Feature Workflow

Every meaningful change you want to make with the code is considered a `Feature`. While you can use all prompts individually and out of the context of a feature, the intent is to (generally) follow the `Feature Worfklow`.

The `Feature Workflow` is intended to scale with the work - work that takes as little as half an hour and work that can take a day or two all can fit within the `Feature Workflow`.

The `Feature Workflow` consists of following chatmodes that handoff

## Getting started
1. Browse the prompts under `.github/prompts/` to find a starting point for your Copilot agent scenario.
2. Customize frontmatter and directives so they reflect your project constraints and quality expectations.
3. Store the tailored prompt in the same directory so it is easy to discover and evolve alongside the rest of the crate.

## Contributing
- Keep new prompts agent-ready by following the structure described inside each meta-prompt.
- Document assumptions, verification steps, and deliverables so other developers can reuse the prompt confidently.
- Prefer descriptive filenames that communicate the agent’s purpose, such as `incident-responder.prompt.md`.

## License
Specify the license that governs contributions and usage when formalizing distribution.
