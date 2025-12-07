---
title: "TypeScript Development Steering Instructions"
summary: "Domain-specific guidance for TypeScript/JavaScript feature development within the Feature Loop"
extends: "instructions.md"
domain: "language"
applicability: "*.ts, *.tsx, *.js, *.jsx files, Node.js and frontend projects"
---

# TypeScript Steering Instructions

*This steering prompt extends the generic `instructions.md` with TypeScript and JavaScript-specific conventions, tooling, and validation protocols. Apply this guidance when developing features involving TypeScript or modern JavaScript code.*

## Language Conventions

### Type System
- **Strict mode**: Enable `strict: true` in `tsconfig.json` for maximum type safety
- **Type annotations**: Prefer explicit types for function parameters and return values
- **Type inference**: Leverage TypeScript's inference for local variables when type is obvious
- **Generics**: Use generics for reusable, type-safe components and utilities
- **Union types**: Prefer union types over enums for string literals: `type Status = 'pending' | 'active' | 'completed'`

### Modern JavaScript Features
- **Arrow functions**: Use for concise syntax and lexical `this` binding
- **Destructuring**: Destructure objects and arrays for cleaner code
- **Spread operator**: Use `...` for object/array copying and merging
- **Optional chaining**: Use `?.` for safe property access: `user?.profile?.email`
- **Nullish coalescing**: Use `??` for null/undefined checks: `value ?? defaultValue`
- **Template literals**: Use backticks for string interpolation: `` `Hello, ${name}!` ``

### Async Patterns
- **Promises**: Use `Promise<T>` for asynchronous operations
- **Async/await**: Prefer `async/await` over `.then()` chains for readability
- **Error handling**: Always wrap `await` in try-catch blocks or handle promise rejections
- **Parallel execution**: Use `Promise.all()` for independent concurrent operations
- **Sequential execution**: Use `for...of` with `await` when operations must be sequential

### Code Organization
- **Module structure**: Use ES modules (`import`/`export`) exclusively, avoid CommonJS
- **Named exports**: Prefer named exports over default exports for better refactoring
- **Barrel files**: Use `index.ts` to re-export from directories for clean imports
- **File naming**: Use kebab-case for files: `user-service.ts`, `auth-middleware.ts`
- **Interface naming**: No "I" prefix, descriptive names: `User` not `IUser`

## Framework-Specific Patterns

### React
- Reference `react_steering.instructions.md` for component patterns, hooks, state management, performance optimization

### Node.js/Express
- Reference `express_steering.instructions.md` for routing, middleware, error handling, async patterns

### NestJS
- Reference `nestjs_steering.instructions.md` for dependency injection, decorators, modules, providers

### Angular
- Reference `angular_steering.instructions.md` for components, services, RxJS patterns, change detection

## Tooling & Validation

### Required Tools
- **TypeScript Compiler**: `tsc` with appropriate `tsconfig.json` configuration
- **Linting**: ESLint with TypeScript plugin (`@typescript-eslint/parser`, `@typescript-eslint/eslint-plugin`)
- **Formatting**: Prettier with ESLint integration
- **Type Checking**: `tsc --noEmit` for type validation without compilation
- **Testing**: Jest or Vitest with TypeScript support

### Validation Protocol
Execute these commands in sequence for TypeScript features:

```bash
# 1. Format code
prettier --write src/

# 2. Lint with auto-fix
eslint --fix src/

# 3. Type check
tsc --noEmit

# 4. Run tests with coverage
jest --coverage

# 5. Build (if applicable)
npm run build
```

### ESLint Configuration
Essential rules for TypeScript projects:

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
    "@typescript-eslint/no-floating-promises": "error",
    "@typescript-eslint/no-misused-promises": "error"
  }
}
```

### Coverage Requirements
- **Small features**: 75% minimum coverage for modified modules
- **Medium features**: 80% minimum coverage for modified modules
- **Large features**: 85% minimum coverage across feature scope

### Testing Patterns
- **Unit tests**: Use Jest or Vitest with TypeScript preset
- **Mocking**: Use `jest.mock()` or Vitest equivalents for dependencies
- **Type testing**: Use `@ts-expect-error` to validate type errors in tests
- **Async testing**: Use `async/await` in test functions, not callbacks

## Dependency Management

### Package Management
- **Tool**: npm (with `package-lock.json`) or yarn/pnpm
- **Type definitions**: Install `@types/*` packages for libraries without built-in types
- **Version pinning**: Use exact versions in `package-lock.json`, semver ranges in `package.json`
- **Audit**: Run `npm audit` regularly to identify security vulnerabilities

### Type Definitions
- **DefinitelyTyped**: Use `@types/*` packages from DefinitelyTyped for popular libraries
- **Custom types**: Create `.d.ts` files for libraries without type definitions
- **Type declarations**: Use `declare module` for augmenting existing types

### Version Compatibility
- **Node version**: Specify in `engines` field of `package.json`
- **TypeScript version**: Pin TypeScript version to ensure consistent compilation
- **Browser support**: Configure in `browserslist` or `tsconfig.json` `target`

## Performance Considerations

### Optimization Patterns
- **Lazy loading**: Use dynamic `import()` for code splitting
- **Memoization**: Cache expensive computations with memoization utilities
- **Debouncing/Throttling**: Use for frequently called functions (event handlers)
- **Object pooling**: Reuse objects for high-frequency allocation scenarios
- **Tree shaking**: Structure code to enable unused code elimination

### Bundle Size
- **Analysis**: Use `webpack-bundle-analyzer` or similar tools
- **Imports**: Prefer specific imports over barrel imports: `import { func } from 'lodash/func'`
- **Dependencies**: Evaluate bundle impact before adding libraries
- **Code splitting**: Split by route or feature for optimal loading

### Runtime Performance
- **Avoid**: Premature optimization, measure first with profiling tools
- **Array operations**: Be mindful of complexity (avoid nested loops in hot paths)
- **Immutability**: Use immutable patterns for predictable state updates
- **Web Workers**: Offload CPU-intensive tasks to prevent UI blocking

## Documentation Standards

### TSDoc Comments
Use TSDoc for documenting public APIs:

```typescript
/**
 * Calculates the total price including tax.
 * 
 * @param items - Array of item prices
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @returns Total price including tax
 * @throws {Error} If taxRate is negative
 * 
 * @example
 * ```ts
 * const total = calculateTotal([10, 20], 0.08);
 * console.log(total); // 32.4
 * ```
 */
function calculateTotal(items: number[], taxRate: number = 0): number {
  if (taxRate < 0) {
    throw new Error('Tax rate cannot be negative');
  }
  const subtotal = items.reduce((sum, item) => sum + item, 0);
  return subtotal * (1 + taxRate);
}
```

### Type Documentation
- **Complex types**: Add comments explaining business logic or constraints
- **Generic parameters**: Document type parameter intent
- **Branded types**: Explain the purpose of branded/nominal types

## Security Best Practices

### Input Validation
- **Runtime validation**: Use libraries like Zod, Yup, or io-ts for runtime type checking
- **API boundaries**: Validate all external inputs (HTTP requests, user input, file uploads)
- **SQL injection**: Use parameterized queries or ORM query builders
- **XSS prevention**: Sanitize user input, use templating engines with auto-escaping

### Secret Management
- **Environment variables**: Use `.env` files with `dotenv` package, never commit secrets
- **Type safety**: Create typed environment variable interfaces
- **Validation**: Validate environment variables at startup

```typescript
interface Environment {
  DATABASE_URL: string;
  API_KEY: string;
  NODE_ENV: 'development' | 'production' | 'test';
}

function loadEnvironment(): Environment {
  const { DATABASE_URL, API_KEY, NODE_ENV } = process.env;
  
  if (!DATABASE_URL || !API_KEY || !NODE_ENV) {
    throw new Error('Missing required environment variables');
  }
  
  return { DATABASE_URL, API_KEY, NODE_ENV };
}
```

### Dependency Security
- **Audit**: Run `npm audit` before releases
- **Updates**: Keep dependencies current, review changelogs
- **Lockfiles**: Commit lockfiles to ensure reproducible builds

## Integration with Feature Loop

### Addin Triggers
TypeScript features may automatically trigger these addins:
- **Performance**: For API endpoints, data processing, or rendering-heavy components
- **Accessibility**: For React or frontend UI components
- **Security**: For authentication, authorization, or data handling logic
- **Observability**: For critical business logic or distributed system interactions

### Validation Integration
During Feature Loop validation phase, TypeScript-specific checks run:
1. Type checking with `tsc --noEmit` ensures type safety
2. Linting with ESLint enforces code quality and catches common errors
3. Formatting with Prettier ensures consistent code style
4. Test suite with Jest/Vitest validates functionality
5. Coverage analysis ensures adequate test coverage

### Size Classification Impact
- **Small TypeScript features**: Format, lint, type check, unit tests
- **Medium TypeScript features**: Add integration tests, bundle size analysis, performance validation
- **Large TypeScript features**: Full validation suite including E2E tests, load testing, security audits

## Common Pitfalls & Anti-Patterns

### Avoid
- **Any type**: Never use `any`, use `unknown` and narrow with type guards if needed
- **Type assertions**: Minimize use of `as`, prefer type guards or proper typing
- **Implicit any**: Always enable `noImplicitAny` in `tsconfig.json`
- **Null vs undefined**: Be consistent, prefer `undefined` for optional values
- **Loose equality**: Never use `==`, always use `===`
- **Callback hell**: Use async/await instead of nested callbacks

### Prefer
- **Const assertions**: Use `as const` for literal types
- **Type guards**: Use type predicates (`value is Type`) for narrowing
- **Discriminated unions**: Use for type-safe state machines
- **Branded types**: Use for nominal typing when needed
- **Utility types**: Leverage built-in utility types (`Partial`, `Pick`, `Omit`, `Record`)

## Error Handling

### Error Types
Define custom error classes for domain errors:

```typescript
class ValidationError extends Error {
  constructor(
    message: string,
    public readonly field: string,
    public readonly value: unknown
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}
```

### Error Boundaries
- **React**: Use error boundaries for component error handling
- **Express**: Use error-handling middleware
- **Promises**: Always handle rejections, use `.catch()` or try-catch with async/await

### Result Types
Consider using Result types for operations that can fail:

```typescript
type Result<T, E = Error> = 
  | { success: true; value: T }
  | { success: false; error: E };
```

## Migration Considerations

### JavaScript to TypeScript
- **Gradual migration**: Use `allowJs: true`, migrate file by file
- **Type definitions**: Add `@ts-check` to JS files for gradual type checking
- **Any escape hatch**: Use `any` temporarily during migration, refine later

### TypeScript Version Upgrades
- **Breaking changes**: Review TypeScript release notes for breaking changes
- **Strict flags**: Enable additional strict flags incrementally
- **Deprecated APIs**: Address deprecation warnings promptly

### Framework Upgrades
- **Dependencies**: Update type definitions alongside framework updates
- **Testing**: Run full test suite after upgrades
- **Rollback plan**: Maintain ability to revert if issues emerge

## References

- **TypeScript Handbook**: https://www.typescriptlang.org/docs/handbook/
- **TypeScript Deep Dive**: https://basarat.gitbook.io/typescript/
- **ESLint TypeScript**: https://typescript-eslint.io/
- **Testing Library**: https://testing-library.com/docs/
- **Node.js Best Practices**: https://github.com/goldbergyoni/nodebestpractices
