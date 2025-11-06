# Feature Loop: Structured Iterative Development

## Overview

The **Feature Loop** is a structured, iterative development methodology designed to deliver software features of varying complexity—from small enhancements to large architectural initiatives—while maintaining consistent quality standards and comprehensive traceability.

## Core Concepts

### 1. Size-Based Workflow Calibration

Features are classified by size to calibrate validation intensity and process rigor:

| Size | Scope | Duration | Lines Changed | Testing Requirement |
|------|-------|----------|---------------|---------------------|
| **Small** | Single module | ≤4 hours | ≤200 | Unit tests, basic integration |
| **Medium** | Multiple modules | 1-5 days | 200-1000 | Comprehensive unit/integration, performance validation |
| **Large** | Cross-service | 1-4 weeks | >1000 | Full test pyramid, load testing, security audits |

### 2. Modular Addins

**Addins** are specialized, composable modules that inject domain-specific capabilities into the Feature Loop without disrupting core workflow integrity.

**Standard Addins**:
- **Performance Optimization**: Profiling, benchmarking, hotspot analysis
- **Security Hardening**: Threat modeling, vulnerability scanning, audit logging
- **Accessibility Compliance**: WCAG validation, keyboard navigation, screen reader support
- **Observability Instrumentation**: Structured logging, metric emission, distributed tracing
- **Localization Support**: String externalization, locale formatting, translation workflows

**Addin Characteristics**:
- **Trigger Conditions**: Explicit criteria for when to invoke
- **Integration Points**: Specific loop phases accepting invocation
- **Input Contracts**: Required context and configuration
- **Output Artifacts**: Generated code, reports, or validation evidence

### 3. Steering Prompts vs. Generic Instructions

The Feature Loop distinguishes between universal guidance and domain-specific knowledge:

#### Generic Instructions (`instructions.md`)
Universal development principles applicable across all contexts:
- Coding standards (DRY, SOLID principles)
- Testing requirements (coverage thresholds, test types)
- Security baselines (authentication, authorization, secret management)
- Documentation standards (code comments, README, changelogs)
- Collaboration practices (code reviews, commit messages)

#### Steering Prompts (`{domain}_steering.instructions.md`)
Domain-specific guidance layered atop generic instructions:
- **Language Steering**: Python, TypeScript, Go, Rust, Java conventions
- **Framework Steering**: React, Django, Spring, Express patterns
- **Architectural Steering**: Microservices, event-driven, serverless approaches

**Steering Extension Pattern**:
```markdown
---
title: "Python Development Steering Instructions"
extends: "instructions.md"
domain: "language"
---

# Python Steering Instructions
*Extends generic `instructions.md` with Python-specific context*

## Language Conventions
[Python-specific syntax, idioms, standard library usage]

## Validation Protocol
[Python tooling: mypy, ruff, black, pytest]

## Integration with Generic Instructions
[How Python steering complements universal guidelines]
```

## Loop Phases

### Phase 1: Intake & Planning
**Purpose**: Understand requirements, classify feature size, select addins/steering

**Activities**:
1. Parse requirements and acceptance criteria
2. Apply size classification rubric
3. Identify applicable steering prompts (by language, framework, architecture)
4. Select required addins based on feature characteristics
5. Draft implementation strategy with risk assessment

**Exit Criteria**: Plan approved, size confirmed, addins/steering identified

### Phase 2: Implementation
**Purpose**: Execute development with domain guidance and addin integration

**Activities**:
1. Load applicable steering prompts for context
2. Implement core functionality following established patterns
3. Integrate addins at designated points (telemetry hooks, security layers, accessibility attributes)
4. Synchronize documentation with code changes
5. Execute rapid feedback loops (syntax checks, type validation, local tests)

**Exit Criteria**: Code complete, self-validated, documentation synchronized

### Phase 3: Validation
**Purpose**: Execute size-calibrated testing and addin-specific validation

**Activities**:
1. Run size-appropriate test suites (small: unit tests; medium: integration; large: full pyramid)
2. Apply steering-defined validation protocols (language-specific linters, type checkers, formatters)
3. Execute addin validations (performance benchmarks, security scans, accessibility audits)
4. Collect evidence artifacts (test reports, coverage metrics, scan results)

**Exit Criteria**: All quality gates passed, evidence documented

### Phase 4: Review & Refinement
**Purpose**: Obtain feedback, address concerns, secure approvals

**Activities**:
1. Conduct self-review of diff and documentation
2. Invoke automated code review tool
3. Execute security scanning (CodeQL)
4. Structure PR description with context, changes, testing, deployment notes
5. Address reviewer feedback systematically

**Exit Criteria**: Approvals obtained, feedback addressed

### Phase 5: Deployment & Monitoring
**Purpose**: Rollout feature with appropriate strategy, validate in production

**Activities**:
1. Execute size-appropriate rollout (small: direct merge; medium: feature flag; large: phased deployment)
2. Validate telemetry and monitoring
3. Execute smoke tests in production
4. Maintain rollback readiness

**Exit Criteria**: Deployed successfully, telemetry validated, stakeholders notified

### Phase 6: Retrospective & Knowledge Capture
**Purpose**: Learn from execution, improve processes, update knowledge base

**Activities**:
1. Assess outcome against acceptance criteria
2. Evaluate addin efficacy and steering utility
3. Document novel patterns and learnings
4. Identify process improvement opportunities

**Exit Criteria**: Learnings documented, improvements proposed

## Usage Patterns

### Invoking the Feature Loop

**As a Prompt**:
Use `feature.loop.prompt.md` to guide manual feature development:
```
Reference: .github/prompts/feature.loop.prompt.md

Feature Request: [Describe feature with acceptance criteria]
```

**As an Agent**:
Use `feature.loop.agent.md` for autonomous feature execution:
```
Agent: .github/prompts/feature.loop.agent.md

Task: Implement user authentication with JWT tokens
Requirements: [Detailed requirements]
```

### Selecting Steering Prompts

Steering prompts are automatically loaded based on:
1. **File extensions**: Modified `.py` files → load `python_steering.instructions.md`
2. **Framework markers**: `package.json` present → load `typescript_steering.instructions.md`
3. **Explicit directives**: Feature request specifies required steering
4. **Historical patterns**: Similar past features used specific steering

**Manual Selection**:
```
Steering: python_steering.instructions.md, django_steering.instructions.md
```

### Activating Addins

Addins are triggered by feature characteristics:

**Explicit Activation**:
```
Addins: performance, security
```

**Automatic Triggers**:
- **Performance**: Latency-sensitive operations, database queries, API endpoints
- **Security**: Authentication changes, sensitive data handling, external integrations
- **Accessibility**: UI components, user-facing interfaces
- **Observability**: Critical business logic, distributed system interactions
- **Localization**: User-visible text, regional features

## File Organization

```
.github/
├── prompts/
│   ├── feature.loop.prompt.md           # Main Feature Loop prompt
│   ├── feature.loop.agent.md            # Autonomous agent configuration
│   ├── instructions.md                   # Generic development guidelines
│   ├── python_steering.instructions.md   # Python-specific steering
│   ├── typescript_steering.instructions.md # TypeScript-specific steering
│   └── [other steering prompts]
└── addins/
    ├── performance.md                    # Performance optimization addin
    ├── security.md                       # Security hardening addin
    ├── accessibility.md                  # Accessibility compliance addin
    ├── observability.md                  # Observability instrumentation addin
    └── localization.md                   # Localization support addin
```

## Extending the Feature Loop

### Creating New Steering Prompts

1. **Identify Domain**: Language, framework, or architectural pattern
2. **Create File**: `.github/prompts/{domain}_steering.instructions.md`
3. **Structure**:
   ```markdown
   ---
   title: "{Domain} Steering Instructions"
   extends: "instructions.md"
   domain: "language|framework|architecture"
   applicability: "File patterns or markers"
   ---
   
   # {Domain} Steering Instructions
   *Extends generic `instructions.md` with {domain}-specific context*
   
   ## Domain Conventions
   ## Validation Protocol
   ## Integration with Generic Instructions
   ```
4. **Reference**: Generic instructions, other steering prompts as needed

### Creating New Addins

1. **Identify Need**: Specialized capability required across features
2. **Create File**: `.github/addins/{addin_name}.md`
3. **Structure**:
   ```markdown
   ---
   title: "{Addin Name}"
   summary: "Feature Loop addin for {purpose}"
   trigger_conditions: [list of triggers]
   integration_points: [list of phases]
   ---
   
   # {Addin Name}
   
   ## Purpose
   ## Trigger Conditions
   ## Integration Points
   ## Configuration
   ## Validation Checklist
   ```
4. **Integration**: Document in Feature Loop prompt and agent

## Benefits

### Scalability
- **Small features**: Lightweight process, rapid iteration
- **Large features**: Comprehensive governance, risk management

### Consistency
- **Universal standards**: Generic instructions apply everywhere
- **Domain expertise**: Steering prompts provide specialized knowledge

### Modularity
- **Composable addins**: Mix and match capabilities as needed
- **Clean separation**: Addins don't contaminate core workflow

### Traceability
- **Audit trails**: Link requirements → implementation → validation
- **Evidence-based**: Document decisions and validations

### Quality
- **Size-calibrated validation**: Right rigor for the context
- **Multi-layered checks**: Generic + steering + addin validations

## Examples

### Small Feature: Update API Response Format

**Classification**: Small (single module, <100 LOC, 2 hours)

**Steering**: `typescript_steering.instructions.md` (Node.js API)

**Addins**: None required

**Process**:
1. **Intake**: Parse requirement, confirm small classification
2. **Implementation**: Modify serialization logic, update tests
3. **Validation**: TypeScript type check, unit tests, linting
4. **Review**: Self-review, automated code review
5. **Deployment**: Direct merge, standard CI/CD
6. **Retrospective**: Document serialization pattern used

### Medium Feature: Implement User Profile Caching

**Classification**: Medium (multiple modules, ~500 LOC, 3 days)

**Steering**: `python_steering.instructions.md`, `django_steering.instructions.md`

**Addins**: Performance, Observability

**Process**:
1. **Intake**: Identify cache strategy, select Redis, plan cache invalidation
2. **Implementation**: Cache layer implementation, telemetry hooks, cache middleware
3. **Validation**: Unit/integration tests, performance benchmarks, cache hit rate validation
4. **Review**: Code review focusing on cache coherence, TTL appropriateness
5. **Deployment**: Feature flag rollout, gradual cache enablement, monitoring
6. **Retrospective**: Document cache patterns, evaluate performance gains

### Large Feature: Multi-Region Database Replication

**Classification**: Large (cross-service, ~2000 LOC, 3 weeks)

**Steering**: `postgres_steering.instructions.md`, `microservices_steering.instructions.md`

**Addins**: Performance, Security, Observability

**Process**:
1. **Intake**: Threat model, replication topology design, failover strategy, data consistency model
2. **Implementation**: Replication setup, connection routing, conflict resolution, audit logging
3. **Validation**: Full test pyramid, failover testing, data consistency validation, load testing, security audit
4. **Review**: Architecture review, security review, code review with focus on edge cases
5. **Deployment**: Phased rollout (dev→staging→canary→production), progressive traffic shifting
6. **Retrospective**: Document replication patterns, operational runbooks, lessons learned

## Best Practices

### For Feature Developers
- **Classify honestly**: Don't undersize features to avoid process
- **Load steering early**: Review applicable steering before implementation
- **Select addins deliberately**: Only activate genuinely needed addins
- **Document decisions**: Capture rationale for future maintainers
- **Iterate rapidly**: Use feedback loops to catch issues early

### For Steering Prompt Authors
- **Extend, don't replace**: Build upon generic instructions
- **Be specific**: Provide concrete examples and tool invocations
- **Stay current**: Update as languages/frameworks evolve
- **Avoid redundancy**: Don't duplicate generic instruction content

### For Addin Authors
- **Single responsibility**: Each addin addresses one concern
- **Clear integration**: Document exact integration points
- **Measurable outputs**: Provide quantifiable artifacts
- **Composability**: Design to work alongside other addins

## Troubleshooting

### Feature Size Unclear
- **Action**: Present classification options with rubric application
- **Escalate**: Request human judgment with tradeoff analysis

### Steering Conflict with Generic Instructions
- **Priority**: Security/compliance → Generic → Steering
- **Action**: Document conflict, escalate for policy clarification

### Addin Integration Failure
- **Action**: Review addin documentation, attempt manual integration
- **Escalate**: Provide context, request addin author guidance

### Validation Bottleneck
- **Action**: Parallelize independent validations (tests, linting, security scans)
- **Optimize**: Cache dependencies, incremental builds

## Future Enhancements

### Planned Additions
- Additional steering prompts: Go, Rust, Java, C++
- Framework steering: Spring Boot, Ruby on Rails, Vue.js, Angular
- Additional addins: Accessibility, Localization, Database migration
- Workflow templates: Pre-configured loops for common scenarios

### Community Contributions
- Submit new steering prompts for languages/frameworks
- Propose addin ideas for common concerns
- Share success stories and learnings
- Suggest Feature Loop improvements

## References

- **Main Prompt**: `.github/prompts/feature.loop.prompt.md`
- **Agent Configuration**: `.github/prompts/feature.loop.agent.md`
- **Generic Instructions**: `.github/prompts/instructions.md`
- **Steering Examples**: Python, TypeScript steering prompts
- **Addin Examples**: Performance, Security addins

---

*The Feature Loop is part of the Context Crate, a curated library of prompts and agents designed to supercharge GitHub Copilot users.*
