---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. **Setup**: Run `.specify/scripts/bash/setup-plan.sh --json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load Context & Determine Sizing** (NEW):
   - Read FEATURE_SPEC and `.specify/memory/constitution.md`
   - Extract the Feature Sizing & Adaptive Workflows section from constitution
   - **Sizing Detection**: Estimate feature size (S/M/L) based on:
     * Scope of spec (single story vs. multi-story)
     * Number of new entities (1–2 vs. 3+)
     * API endpoints needed (1–2 vs. 3+)
     * External dependencies (none vs. many)
     * Technical risk/uncertainty
   - Load IMPL_PLAN template (already copied)

3. **Execute Adaptive Plan Workflow** (NEW - phases depend on size):
   
   **For Small (S)**:
   - Phase 0: Load spec + constitution
   - Phase 1: Constitution Check (brief validation)
   - Phase 2: Generate minimal plan.md (~150 words):
     * Tech stack reference (one-liner or link to existing choice)
     * File structure (2–3 files touched)
     * Success criteria (from spec)
   - Phase 3: Skip to `/tasks` (do NOT generate research.md, data-model.md, contracts/)
   - **Total artifact output**: spec.md, plan.md only
   
   **For Medium (M)**:
   - Phase 0: Load spec + constitution
   - Phase 1: Constitution Check
   - Phase 2: Conditional Research
     * If [NEEDS CLARIFICATION] markers in spec: run brief research (~5 min)
     * Otherwise: skip
   - Phase 3: Generate design artifacts (conditional):
     * data-model.md: Only if new entities detected
     * contracts/: Only if 3+ new endpoints
     * research.md: Only if Phase 2 research ran
   - Phase 4: Generate plan.md (~400–600 words)
   - Phase 5: Update agent context
   - Phase 6: Proceed to `/tasks`
   - **Total artifact output**: spec.md, plan.md, ±research.md, ±data-model.md, ±contracts/
   
   **For Large (L)**:
   - Phase 0: Load spec + constitution
   - Phase 1: Constitution Check (comprehensive)
   - Phase 2: Research Phase (required)
     * Resolve all [NEEDS CLARIFICATION] markers
     * Generate research.md
   - Phase 3: Design Phase
     * Generate data-model.md
     * Generate contracts/
     * Generate quickstart.md
   - Phase 4: Generate plan.md (~600–1000 words)
   - Phase 5: Update agent context
   - Phase 6: Proceed to `/tasks`
   - **Total artifact output**: spec.md, research.md, data-model.md, contracts/, quickstart.md, plan.md

4. **Multi-Feature Problem Handling** (NEW):
   - If FEATURE_SPEC is a problem-level spec (from multi-feature detection in `/specify`):
     * This is `[problem-spec]`; User can now request `/plan f001` for Feature F001
     * Current `/plan` run outputs a generic planning guide for the problem
     * Subsequent `/plan f001` calls generate feature-level artifacts
   - If FEATURE_SPEC is a feature-level spec:
     * Generate full artifacts per size above
     * Feature-level artifacts land in `specs/f001/`, `specs/f002/`, etc.

5. **Stop and report**: Command ends after planning phase. Report branch, IMPL_PLAN path, generated artifacts, sizing decision, and readiness for `/tasks`.

## Phases (Adaptive by Sizing)

### Phase 0: Outline & Research (Large Only)

1. **Extract unknowns from Technical Context** (if size is L):
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:
   ```
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved (Large only; skipped for S/M)

### Phase 1: Design & Contracts (Medium+ Only)

**Prerequisites:** `research.md` complete (if Large)

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/bash/update-agent-context.sh copilot`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file (Medium+ only; skipped for S)

### Phase 2: Sizing Validation Checkpoint (All)

Before proceeding to `/tasks`, validate:
- Estimated task count aligns with size category:
  * Small (S): 1–3 tasks expected
  * Medium (M): 4–7 tasks expected
  * Large (L): 8–15 tasks per feature expected
- If task estimate exceeds ceiling:
  * S exceeding 3 → suggest size reclassification to M or task split
  * M exceeding 7 → suggest size reclassification to L or task split
  * L exceeding 15 per feature → suggest feature split into F+1 features
- Output sizing validation result to report

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
- DO CREATE a spec that is LESS than 1 page (~500 words)