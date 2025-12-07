---
title: "Python Development Steering Instructions"
summary: "Domain-specific guidance for Python feature development within the Feature Loop"
extends: "instructions.md"
domain: "language"
applicability: "*.py files, Python projects"
---

# Python Steering Instructions

*This steering prompt extends the generic `instructions.md` with Python-specific conventions, tooling, and validation protocols. Apply this guidance when developing features involving Python code.*

## Language Conventions

### Type Annotations
- **Mandatory**: Type hints required for all function signatures per PEP 484
- **Collections**: Use `list[T]`, `dict[K, V]` (Python 3.9+) or `List[T]`, `Dict[K, V]` from `typing` for older versions
- **Optional values**: Use `Optional[T]` or `T | None` (Python 3.10+)
- **Callable signatures**: Specify parameter and return types: `Callable[[int, str], bool]`

### String Formatting
- **Prefer**: f-strings for readability and performance: `f"Hello, {name}!"`
- **Avoid**: Older `.format()` or `%` formatting unless maintaining legacy code
- **Multi-line**: Use parentheses for implicit concatenation or triple-quoted strings

### Error Handling
- **Context managers**: Use `with` statements for resource management (files, locks, connections)
- **Exception specificity**: Catch specific exceptions; avoid bare `except:` clauses
- **Exception chaining**: Use `raise ... from ...` to preserve exception context
- **Custom exceptions**: Inherit from appropriate base classes, provide meaningful messages

### Code Organization
- **Module structure**: Imports → Constants → Classes → Functions → Main execution guard
- **Import order**: Standard library → Third-party → Local application (enforced by isort)
- **Docstrings**: Required for all public modules, classes, and functions (Google or NumPy style)
- **Naming**: `snake_case` for functions/variables, `PascalCase` for classes, `UPPER_CASE` for constants

### Pythonic Patterns
- **Comprehensions**: Prefer list/dict/set comprehensions over explicit loops when readable
- **Iterators**: Use generators for memory-efficient iteration over large datasets
- **Context protocols**: Implement `__enter__` and `__exit__` for custom resource managers
- **Dataclasses**: Use `@dataclass` decorator for simple data containers (Python 3.7+)
- **Protocols**: Use `typing.Protocol` for structural subtyping (duck typing with type checking)

## Framework-Specific Patterns

### Django
- Reference `django_steering.instructions.md` for ORM patterns, view structure, middleware, template conventions

### Flask
- Reference `flask_steering.instructions.md` for routing, blueprints, request handling, extension integration

### FastAPI
- Reference `fastapi_steering.instructions.md` for async patterns, dependency injection, OpenAPI integration

### Data Science (NumPy/Pandas)
- Reference `datascience_steering.instructions.md` for vectorization, broadcasting, DataFrame operations

## Tooling & Validation

### Required Tools
- **Type Checking**: `mypy --strict` (or configuration in `pyproject.toml`)
- **Linting**: `ruff check` (modern, fast) or `pylint`/`flake8` (traditional)
- **Formatting**: `black` with 88-character line length (or project-configured)
- **Import Sorting**: `isort` with Black-compatible profile
- **Security Scanning**: `bandit` for security issue detection

### Validation Protocol
Execute these commands in sequence for Python features:

```bash
# 1. Format code
black .

# 2. Sort imports
isort .

# 3. Type check
mypy --strict src/

# 4. Lint
ruff check src/

# 5. Security scan
bandit -r src/ -ll

# 6. Run tests with coverage
pytest --cov=src --cov-report=term-missing --cov-report=html
```

### Coverage Requirements
- **Small features**: 80% minimum coverage for modified modules
- **Medium features**: 85% minimum coverage for modified modules
- **Large features**: 90% minimum coverage across feature scope

### Testing Patterns
- **Fixtures**: Use `pytest` fixtures for reusable test setup
- **Parametrization**: Use `@pytest.mark.parametrize` for testing multiple scenarios
- **Mocking**: Use `unittest.mock` or `pytest-mock` for external dependencies
- **Async testing**: Use `pytest-asyncio` for async function testing

## Dependency Management

### Package Management
- **Tool**: `pip` with `requirements.txt` or `poetry` with `pyproject.toml`
- **Version pinning**: Pin exact versions in lock files, use ranges in requirements
- **Virtual environments**: Always use `venv` or `virtualenv`, never install globally
- **Dependency scanning**: Run security advisories check before adding dependencies

### Version Compatibility
- **Target**: Specify minimum Python version in `pyproject.toml` or setup.py
- **Compatibility**: Test against multiple Python versions using `tox` or GitHub Actions matrix
- **Deprecations**: Monitor Python deprecation warnings, plan migrations for EOL versions

## Performance Considerations

### Optimization Patterns
- **Profiling**: Use `cProfile` or `line_profiler` to identify bottlenecks before optimizing
- **Data structures**: Choose appropriate collections (list vs. set vs. dict) based on access patterns
- **String operations**: Use `str.join()` for concatenating multiple strings
- **Iteration**: Use `itertools` for memory-efficient iteration patterns
- **Compilation**: Consider `numba` for numerical hot loops, `cython` for extension modules

### Async Programming
- **Event loop**: Use `asyncio` for I/O-bound concurrent operations
- **Libraries**: Use async-compatible libraries (`aiohttp`, `asyncpg`, `aiomysql`)
- **Patterns**: Avoid blocking calls in async functions, use `asyncio.run()` as entry point
- **Pitfalls**: Be aware of GIL limitations, use multiprocessing for CPU-bound parallelism

## Documentation Standards

### Docstring Format
Use Google-style docstrings:

```python
def calculate_total(items: list[float], tax_rate: float = 0.0) -> float:
    """Calculate total price including tax.
    
    Args:
        items: List of item prices.
        tax_rate: Tax rate as decimal (e.g., 0.08 for 8%). Defaults to 0.0.
        
    Returns:
        Total price including tax.
        
    Raises:
        ValueError: If tax_rate is negative.
        
    Examples:
        >>> calculate_total([10.0, 20.0], 0.08)
        32.4
    """
```

### Module Documentation
- **Module docstring**: First element in file, describes module purpose
- **Public API**: Document all public functions, classes, and constants
- **Internal**: Use single leading underscore for internal APIs, document if complex

## Security Best Practices

### Input Validation
- **Sanitization**: Validate and sanitize all external inputs (user input, API requests)
- **SQL injection**: Use parameterized queries, ORM query builders
- **Command injection**: Avoid `os.system()`, use `subprocess` with argument lists
- **Path traversal**: Validate file paths, use `pathlib.Path.resolve()` for normalization

### Secret Management
- **Environment variables**: Use `os.environ` or `python-dotenv` for secrets
- **Never commit**: Secrets must never appear in source code or version control
- **Credential storage**: Use secret management services (AWS Secrets Manager, HashiCorp Vault)

### Cryptography
- **Libraries**: Use `cryptography` package, avoid rolling custom crypto
- **Random values**: Use `secrets` module for cryptographic randomness, not `random`
- **Hashing**: Use `hashlib` with appropriate algorithms (SHA-256, SHA-3)

## Integration with Feature Loop

### Addin Triggers
Python features may automatically trigger these addins:
- **Performance**: When modifying data processing, numerical computation, or API endpoints
- **Security**: When handling authentication, authorization, or sensitive data
- **Observability**: When implementing business logic or distributed system interactions

### Validation Integration
During Feature Loop validation phase, Python-specific checks run:
1. Type checking with mypy ensures type safety
2. Linting with ruff enforces code quality standards
3. Security scanning with bandit identifies vulnerabilities
4. Test suite with pytest validates functionality
5. Coverage analysis ensures adequate test coverage

### Size Classification Impact
- **Small Python features**: Basic validation sufficient (formatting, linting, unit tests)
- **Medium Python features**: Add type checking, security scanning, integration tests
- **Large Python features**: Full validation suite including performance benchmarks, load testing

## Common Pitfalls & Anti-Patterns

### Avoid
- **Mutable default arguments**: Never use `def func(items=[]):`, use `None` and instantiate inside
- **Bare except**: Always catch specific exceptions or use `except Exception:` at minimum
- **Global state**: Minimize global variables, prefer dependency injection
- **String concatenation in loops**: Use list accumulation and `str.join()`
- **Import star**: Never use `from module import *`, import explicitly

### Prefer
- **List comprehensions** over `map()/filter()` for simple transformations
- **Context managers** over manual resource cleanup
- **Generators** over lists for large datasets
- **Dataclasses** over manual `__init__` with many attributes
- **Pathlib** over `os.path` for path manipulation

## Migration Considerations

### Python Version Upgrades
- **Deprecation warnings**: Address all deprecation warnings before upgrading
- **New features**: Adopt new syntax/features gradually (match statements, structural pattern matching)
- **Compatibility**: Maintain backward compatibility within major version

### Library Migrations
- **Breaking changes**: Review changelogs for breaking changes
- **Testing**: Run full test suite after dependency updates
- **Rollback plan**: Maintain ability to revert to previous versions

## References

- **PEP Index**: https://peps.python.org/ (Python Enhancement Proposals)
- **Python Packaging**: https://packaging.python.org/ (Official packaging guide)
- **Type Hints**: https://docs.python.org/3/library/typing.html
- **Testing Best Practices**: https://docs.pytest.org/en/stable/
- **Security Guide**: https://python.readthedocs.io/en/stable/library/security_warnings.html
