---
title: "Generic Development Instructions"
summary: "Universal coding standards and practices referenced by Feature Loop and steering prompts"
scope: "repository-wide"
---

# Generic Development Instructions

*These instructions establish baseline development standards applicable across all codebases, languages, and frameworks. Domain-specific steering prompts extend these guidelines with specialized context.*

## Purpose
Provide universal development guidance that ensures consistency, quality, and maintainability across all features developed within the Feature Loop methodology. These instructions serve as the foundation upon which steering prompts layer domain-specific knowledge.

## Code Quality Principles

### Readability
- **Clarity over cleverness**: Write code for humans first, machines second
- **Self-documenting**: Choose descriptive names that convey intent
- **Consistent style**: Follow established patterns within the codebase
- **Reasonable complexity**: Keep functions focused, cyclomatic complexity low

### Maintainability
- **DRY (Don't Repeat Yourself)**: Extract common logic into reusable functions
- **SOLID Principles**: 
  - Single Responsibility: Each module/class has one reason to change
  - Open/Closed: Open for extension, closed for modification
  - Liskov Substitution: Subtypes must be substitutable for base types
  - Interface Segregation: Many specific interfaces better than one general
  - Dependency Inversion: Depend on abstractions, not concretions
- **Modular design**: Loose coupling, high cohesion
- **Refactoring**: Continuously improve code structure

### Testability
- **Unit testable**: Functions should be independently testable
- **Dependency injection**: Pass dependencies rather than hardcoding
- **Avoid global state**: Minimize mutable global variables
- **Pure functions**: Prefer functions without side effects when feasible

## Error Handling

### General Principles
- **Fail fast**: Detect and report errors as early as possible
- **Specific exceptions**: Catch specific error types, not generic exceptions
- **Error context**: Provide meaningful error messages with context
- **Graceful degradation**: Maintain partial functionality when possible
- **Logging**: Log errors with appropriate severity levels

### Error Messages
- **User-facing**: Clear, actionable, no technical jargon or sensitive data
- **Developer-facing**: Include context, stack traces, relevant state
- **Localization**: Support internationalization for user-facing errors
- **Security**: Never expose system internals or security details

## Testing Standards

### Test Coverage
- **Minimum thresholds**: 
  - Small features: 80% coverage
  - Medium features: 85% coverage
  - Large features: 90% coverage
- **Critical paths**: 100% coverage for security-sensitive and business-critical code
- **Edge cases**: Test boundary conditions, null/empty inputs, error paths

### Test Organization
- **Structure**: Arrange-Act-Assert (AAA) pattern
- **Naming**: Descriptive test names indicating scenario and expected outcome
- **Independence**: Tests should not depend on execution order
- **Determinism**: Tests should be repeatable with consistent results

### Test Types
- **Unit tests**: Test individual functions/methods in isolation
- **Integration tests**: Test interaction between components
- **End-to-end tests**: Test complete user workflows
- **Performance tests**: Validate latency, throughput, resource usage
- **Security tests**: Validate authentication, authorization, input handling

## Documentation Standards

### Code Documentation
- **Public APIs**: Document all public functions, classes, modules
- **Complex logic**: Explain non-obvious algorithms or business rules
- **Assumptions**: Document preconditions, postconditions, invariants
- **TODO/FIXME**: Use sparingly, link to issues for tracking

### Repository Documentation
- **README**: Project overview, setup instructions, basic usage
- **CONTRIBUTING**: Development workflow, coding standards, PR process
- **CHANGELOG**: Notable changes, version history, migration notes
- **Architecture docs**: System design, key decisions, diagrams

### Documentation Style
- **Conciseness**: Clear and brief, avoid unnecessary verbosity
- **Examples**: Include code examples for complex APIs
- **Current**: Keep documentation synchronized with code changes
- **Searchable**: Use consistent terminology for easy discovery

## Version Control

### Commit Messages
Follow conventional commit format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, test, chore
**Subject**: Imperative mood, lowercase, no period, ≤50 characters
**Body**: Explain what and why, not how, wrap at 72 characters
**Footer**: Breaking changes, issue references

**Examples**:
```
feat(auth): add JWT token refresh endpoint

Implement automatic token refresh to improve UX. Tokens expire after
1 hour but refresh tokens valid for 30 days.

Closes #123
```

### Branching Strategy
- **Main/Master**: Production-ready code, protected
- **Feature branches**: `feature/<description>` or `<username>/<description>`
- **Bug fixes**: `fix/<description>`
- **Releases**: `release/<version>` (if applicable)
- **Hotfixes**: `hotfix/<description>`

### Pull Request Process
1. **Create branch**: From latest main/master
2. **Implement feature**: Following Feature Loop methodology
3. **Self-review**: Check diff, verify tests, update documentation
4. **Create PR**: Descriptive title, comprehensive description, link issues
5. **Address feedback**: Respond to reviewer comments
6. **Merge**: After approvals, using squash or merge commit per repo policy

## Security Standards

### Authentication & Authorization
- **Strong passwords**: Enforce minimum complexity requirements
- **Secure storage**: Hash passwords with bcrypt/argon2, never plain text
- **Session management**: Secure session IDs, appropriate timeouts
- **Token handling**: JWTs with signatures, secure storage, proper validation
- **Least privilege**: Grant minimum necessary permissions

### Data Protection
- **Encryption**: Encrypt sensitive data in transit (TLS) and at rest
- **PII handling**: Comply with privacy regulations (GDPR, CCPA, HIPAA)
- **Secret management**: Use environment variables or secret managers
- **Data validation**: Validate and sanitize all external inputs
- **Output encoding**: Prevent injection attacks (XSS, SQL injection)

### Audit & Compliance
- **Logging**: Log security-relevant events (authentication, authorization, data access)
- **Monitoring**: Alert on suspicious patterns or anomalies
- **Incident response**: Documented procedures for security events
- **Regular audits**: Periodic security reviews and penetration testing

## Performance Standards

### Optimization Approach
- **Measure first**: Profile before optimizing
- **Optimize hotspots**: Focus on code paths with highest impact
- **Algorithmic complexity**: Consider Big O notation for scalability
- **Premature optimization**: Avoid unless performance requirements demand it

### Resource Management
- **Memory**: Monitor memory usage, prevent leaks, release resources promptly
- **CPU**: Avoid unnecessary computation, cache expensive operations
- **I/O**: Minimize network calls, batch operations, use connection pooling
- **Concurrency**: Use async/parallel execution for independent operations

### Monitoring
- **Metrics**: Expose relevant metrics (latency, throughput, error rate)
- **Logging**: Structured logs with appropriate verbosity
- **Tracing**: Distributed tracing for microservices
- **Alerting**: Define alerts for SLA violations or anomalies

## Dependency Management

### Adding Dependencies
1. **Evaluate necessity**: Prefer standard library, consider maintenance burden
2. **Assess quality**: Check activity, stars, issues, documentation
3. **Security scan**: Run vulnerability checks before adding
4. **License compatibility**: Ensure license compatible with project
5. **Size impact**: Consider bundle size for frontend dependencies

### Updating Dependencies
- **Regular updates**: Keep dependencies current with security patches
- **Test thoroughly**: Run full test suite after updates
- **Review changelogs**: Understand breaking changes and new features
- **Pin versions**: Use lock files for reproducible builds

## Collaboration Standards

### Code Reviews
- **Timely**: Review PRs within 1 business day
- **Constructive**: Provide actionable feedback with rationale
- **Thorough**: Check logic, tests, documentation, security
- **Questions welcome**: Encourage learning and knowledge sharing
- **Approval criteria**: Tests pass, meets standards, no blocking issues

### Communication
- **Async-first**: Document decisions, minimize synchronous meetings
- **Clear**: Use precise language, avoid ambiguity
- **Respectful**: Assume positive intent, critique code not people
- **Transparent**: Share context, reasoning, trade-offs
- **Escalation**: Raise blockers promptly with context

### Knowledge Sharing
- **Documentation**: Capture decisions in ADRs or wiki
- **Code comments**: Explain complex or non-obvious logic
- **Team presentations**: Share learnings from features or incidents
- **Pair programming**: Collaborate on complex or critical work
- **Onboarding materials**: Keep onboarding docs current

## Continuous Integration/Deployment

### CI Pipeline
- **Automated testing**: Run full test suite on every commit
- **Linting**: Enforce code style automatically
- **Security scanning**: Scan for vulnerabilities in dependencies and code
- **Build verification**: Ensure code compiles/builds successfully
- **Fast feedback**: Keep pipeline execution under 15 minutes

### Deployment
- **Automated deployment**: Use CD pipeline for consistent deployments
- **Environment parity**: Dev/staging/production should be similar
- **Rollback capability**: Maintain ability to quickly revert changes
- **Monitoring**: Validate deployment success with health checks
- **Communication**: Notify stakeholders of deployments

## Quality Gates

Features must satisfy these gates before merging:

### Functional
- [ ] All acceptance criteria met
- [ ] Manual testing completed (when applicable)
- [ ] Edge cases handled appropriately
- [ ] Error handling implemented

### Code Quality
- [ ] Code review approved
- [ ] Coding standards followed
- [ ] No code smells or anti-patterns
- [ ] Refactoring opportunities addressed

### Testing
- [ ] Test coverage meets threshold
- [ ] All tests passing
- [ ] Integration tests pass
- [ ] Performance tests pass (when applicable)

### Security
- [ ] Security review completed (for sensitive changes)
- [ ] Input validation implemented
- [ ] No secrets in code
- [ ] Dependency vulnerabilities resolved

### Documentation
- [ ] Code documented (public APIs, complex logic)
- [ ] README updated (if applicable)
- [ ] CHANGELOG updated
- [ ] Migration guide provided (for breaking changes)

### Operational
- [ ] Monitoring/alerting configured
- [ ] Logging implemented
- [ ] Performance characteristics documented
- [ ] Rollback procedure documented

## References & Resources

### General Software Engineering
- **Clean Code** by Robert C. Martin
- **The Pragmatic Programmer** by Hunt & Thomas
- **Design Patterns** by Gang of Four
- **Refactoring** by Martin Fowler

### Testing
- **Test Driven Development** by Kent Beck
- **Growing Object-Oriented Software, Guided by Tests** by Freeman & Pryce

### Architecture
- **Domain-Driven Design** by Eric Evans
- **Building Microservices** by Sam Newman
- **Designing Data-Intensive Applications** by Martin Kleppmann

### Security
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Security Engineering** by Ross Anderson
- **The Web Application Hacker's Handbook** by Stuttard & Pinto

## Steering Prompt Integration

These generic instructions serve as the foundation. Steering prompts extend them with:
- **Language-specific conventions**: Syntax, idioms, standard libraries
- **Framework patterns**: Configuration, architecture, best practices
- **Domain expertise**: Specialized knowledge for specific problem domains

When conflicts arise between generic instructions and steering prompts:
1. **Security & compliance**: Generic instructions take precedence
2. **Language/framework specifics**: Steering prompts take precedence
3. **Ambiguity**: Escalate for clarification and documentation

Example structure for steering prompts:
```markdown
# {Domain} Steering Instructions
*Extends: instructions.md*

## {Domain}-Specific Conventions
[Language/framework specific guidance]

## Validation Protocol
[Domain-specific tools and commands]

## Integration with Generic Instructions
[How this steering extends generic instructions]
```
