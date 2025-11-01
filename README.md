# Context Crate

Context Crate is a curated library of prompts, agents, meta-prompts, and operating instructions designed to supercharge GitHub Copilot users. By assembling reusable patterns for planning, coding, reviewing, and coordinating work, the crate enables teams to consistently deliver high-quality software faster.

## Why it exists
- **Double developer throughput:** Each artifact is engineered to help Copilot act as a force multiplier, aiming to boost individual productivity by roughly 2× through sharper task decomposition and decision support.
- **Ready-to-use building blocks:** Mix and match prompts to spin up specialized agents without starting from scratch.
- **Operational consistency:** Shared guidance keeps cross-functional collaborators aligned on communication norms, quality gates, and verification steps.

## Repository structure
- `README.md`: Overview of the Context Crate mission and structure.
- `.github/prompts/`: Meta-prompts that instruct Copilot to generate downstream prompts or agent behaviors.

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
