---
title: "Security Hardening Addin"
summary: "Feature Loop addin for implementing and validating security controls"
trigger_conditions:
  - "Authentication or authorization changes"
  - "Sensitive data handling"
  - "External API integrations"
  - "User input processing"
  - "Cryptographic operations"
integration_points:
  - "Implementation phase: Security control injection"
  - "Validation phase: Security scanning and threat analysis"
---

# Security Hardening Addin

## Purpose
Integrate security best practices, threat modeling, and vulnerability scanning into the Feature Loop to ensure implementations maintain appropriate security postures and comply with organizational security policies.

## Trigger Conditions

This addin is **mandatory** when features involve:
- **Authentication**: Login, session management, token handling
- **Authorization**: Access control, permission checks, role-based access
- **Sensitive data**: PII, credentials, payment information, health data
- **External inputs**: User-submitted data, API requests, file uploads
- **Cryptographic operations**: Encryption, hashing, signing, key management
- **External integrations**: Third-party APIs, webhooks, SSO providers
- **Database access**: Direct queries, ORM operations, schema migrations

## Integration Points

### Phase 1: Planning
**Activity**: Threat modeling and security requirement identification
**Actions**:
1. Identify assets requiring protection (data, services, credentials)
2. Enumerate threat vectors (STRIDE analysis: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege)
3. Define security requirements:
   - Authentication mechanisms
   - Authorization rules
   - Data classification and handling
   - Compliance requirements (GDPR, HIPAA, PCI-DSS)
4. Document security assumptions and trust boundaries
5. Plan security testing strategy

### Phase 2: Implementation
**Activity**: Apply security controls and defensive coding practices
**Actions**:
1. Implement input validation and sanitization
2. Apply output encoding to prevent injection attacks
3. Use parameterized queries or ORM for database access
4. Implement proper error handling (avoid information leakage)
5. Apply least-privilege principles for permissions
6. Use secure cryptographic libraries and algorithms
7. Implement audit logging for security-relevant events

**Input Validation (Python)**:
```python
from pydantic import BaseModel, EmailStr, constr, validator
import re

class UserRegistration(BaseModel):
    username: constr(min_length=3, max_length=20, regex=r'^[a-zA-Z0-9_]+$')
    email: EmailStr
    password: constr(min_length=12)
    
    @validator('password')
    def validate_password_strength(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain digit')
        if not re.search(r'[!@#$%^&*]', v):
            raise ValueError('Password must contain special character')
        return v

# Usage
try:
    user_data = UserRegistration(
        username=request.json['username'],
        email=request.json['email'],
        password=request.json['password']
    )
except ValidationError as e:
    return {'error': 'Invalid input', 'details': e.errors()}, 400
```

**SQL Injection Prevention (Python)**:
```python
# ❌ NEVER: String concatenation
query = f"SELECT * FROM users WHERE email = '{email}'"  # VULNERABLE

# ✅ CORRECT: Parameterized query
query = "SELECT * FROM users WHERE email = %s"
cursor.execute(query, (email,))

# ✅ CORRECT: ORM usage
user = db.session.query(User).filter_by(email=email).first()
```

**Authentication & Authorization (TypeScript)**:
```typescript
import jwt from 'jsonwebtoken';
import bcrypt from 'bcrypt';

// Password hashing
async function hashPassword(password: string): Promise<string> {
  const saltRounds = 12; // Adjust based on security requirements
  return bcrypt.hash(password, saltRounds);
}

// Password verification
async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}

// JWT token generation
function generateToken(userId: string, role: string): string {
  const secret = process.env.JWT_SECRET;
  if (!secret) throw new Error('JWT_SECRET not configured');
  
  return jwt.sign(
    { userId, role },
    secret,
    { expiresIn: '1h', algorithm: 'HS256' }
  );
}

// Authentication middleware
function authenticate(req: Request, res: Response, next: NextFunction) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  
  if (!token) {
    return res.status(401).json({ error: 'Authentication required' });
  }
  
  try {
    const secret = process.env.JWT_SECRET!;
    const decoded = jwt.verify(token, secret) as { userId: string; role: string };
    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' });
  }
}

// Authorization middleware
function authorize(...allowedRoles: string[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user || !allowedRoles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}
```

**Secure Secret Management**:
```python
# ❌ NEVER: Hardcoded secrets
API_KEY = "sk_live_abc123xyz"  # VULNERABLE

# ✅ CORRECT: Environment variables
import os
from typing import Optional

def get_secret(name: str) -> str:
    """Retrieve secret from environment with validation."""
    value = os.environ.get(name)
    if value is None:
        raise ValueError(f"Required secret {name} not configured")
    return value

API_KEY = get_secret('API_KEY')
DATABASE_URL = get_secret('DATABASE_URL')
```

**Audit Logging**:
```typescript
interface AuditLogEntry {
  timestamp: Date;
  userId: string;
  action: string;
  resource: string;
  result: 'success' | 'failure';
  metadata?: Record<string, unknown>;
}

function auditLog(entry: AuditLogEntry): void {
  logger.info({
    ...entry,
    timestamp: entry.timestamp.toISOString(),
  }, 'Security audit log');
  
  // Persist to dedicated audit log storage
  auditLogStore.write(entry);
}

// Usage
auditLog({
  timestamp: new Date(),
  userId: req.user.userId,
  action: 'user.login',
  resource: 'authentication',
  result: 'success',
  metadata: { ipAddress: req.ip, userAgent: req.headers['user-agent'] }
});
```

### Phase 3: Validation
**Activity**: Security scanning and vulnerability assessment
**Actions**:
1. Run static analysis security scanning (SAST)
2. Execute dependency vulnerability scanning
3. Perform secrets detection in code and commits
4. Review authentication/authorization implementation
5. Validate input handling and output encoding
6. Test error handling for information disclosure
7. Execute security-focused test cases

**Python Security Tools**:
```bash
# Static analysis with Bandit
bandit -r src/ -ll -f json -o bandit-report.json

# Dependency vulnerability scanning
safety check --json
pip-audit

# Secrets detection
detect-secrets scan --all-files --force-use-all-plugins

# Type safety (prevents certain bug classes)
mypy --strict src/
```

**TypeScript/Node.js Security Tools**:
```bash
# Dependency vulnerability audit
npm audit --json
npm audit fix  # Apply safe fixes

# Yarn alternative
yarn audit --json

# Static analysis with ESLint security plugins
npx eslint --plugin security --plugin no-secrets src/

# Secrets detection
npx detect-secrets-launcher scan
```

**CodeQL Security Scanning**:
```bash
# Initialize CodeQL database
codeql database create --language=python codeql-db

# Run security queries
codeql database analyze codeql-db security-queries.qls \
  --format=sarif-latest --output=results.sarif

# Review results
codeql database interpret-results codeql-db results.sarif
```

## Output Artifacts

### Threat Model
Document identified threats and mitigations:

```markdown
## Threat Model: User Authentication Feature

### Assets
- User credentials (passwords, tokens)
- Session data
- User profile information

### Threats (STRIDE Analysis)

**Spoofing**
- Threat: Attacker impersonates legitimate user
- Mitigation: Strong password requirements, MFA support, rate limiting
- Status: Implemented

**Tampering**
- Threat: Session token modification
- Mitigation: HMAC signature on JWTs, secure token storage
- Status: Implemented

**Repudiation**
- Threat: User denies performed actions
- Mitigation: Audit logging of authentication events
- Status: Implemented

**Information Disclosure**
- Threat: Password leak through error messages
- Mitigation: Generic error messages, no password echoing
- Status: Implemented

**Denial of Service**
- Threat: Brute force password guessing
- Mitigation: Rate limiting (5 attempts per 15 min), account lockout
- Status: Implemented

**Elevation of Privilege**
- Threat: JWT role manipulation
- Mitigation: Server-side role verification, signed tokens
- Status: Implemented
```

### Security Scan Results
```markdown
## Security Scan Summary

### Static Analysis (Bandit)
- Files Scanned: 45
- Issues Found: 3
- Critical: 0
- High: 1 (False positive - documented)
- Medium: 2 (Addressed)
- Low: 0

**High Severity (False Positive):**
- Issue: Use of `pickle` module
- Location: `src/cache.py:23`
- Justification: Internal cache serialization only, no untrusted input
- Status: Documented and accepted

**Medium Severity:**
1. Issue: Insufficient password complexity validation
   - Location: `src/auth.py:45`
   - Fix: Enhanced regex pattern, added strength requirements
   - Status: ✅ Resolved

2. Issue: Missing HTTP security headers
   - Location: `src/middleware.py:12`
   - Fix: Added helmet middleware with CSP, HSTS, X-Frame-Options
   - Status: ✅ Resolved

### Dependency Vulnerabilities (npm audit)
- Total Dependencies: 234
- Vulnerabilities: 2 (both resolved)
- Critical: 0
- High: 0
- Medium: 0
- Low: 0

**Previously Detected:**
1. lodash@4.17.20 (Prototype Pollution)
   - Fix: Updated to lodash@4.17.21
   - Status: ✅ Resolved

2. jsonwebtoken@8.5.0 (Algorithm confusion)
   - Fix: Updated to jsonwebtoken@9.0.0, explicit algorithm specification
   - Status: ✅ Resolved

### Secrets Detection
- Files Scanned: 120
- Secrets Found: 0
- Status: ✅ Clean
```

### Security Test Results
```markdown
## Security Testing

### Authentication Tests
- [x] Strong password validation
- [x] Password hashing with bcrypt (12 rounds)
- [x] JWT token generation and validation
- [x] Token expiration enforcement
- [x] Refresh token rotation
- [x] Failed login rate limiting
- [x] Account lockout after 5 failed attempts

### Authorization Tests
- [x] Role-based access control
- [x] Resource-level permissions
- [x] Privilege escalation prevention
- [x] Cross-user data access prevention

### Input Validation Tests
- [x] SQL injection prevention (parameterized queries)
- [x] XSS prevention (output encoding)
- [x] CSRF protection (token validation)
- [x] File upload restrictions (type, size)
- [x] Path traversal prevention

### Cryptography Tests
- [x] Secure random token generation
- [x] Proper encryption algorithm usage (AES-256-GCM)
- [x] Secure key derivation (PBKDF2)
- [x] Certificate validation for HTTPS

### Error Handling Tests
- [x] Generic error messages (no information leakage)
- [x] Stack traces disabled in production
- [x] Proper logging without sensitive data
```

## Configuration

### Security Policies
Define in `.github/security-policies.yaml`:

```yaml
authentication:
  password_min_length: 12
  password_require_uppercase: true
  password_require_lowercase: true
  password_require_digit: true
  password_require_special: true
  session_timeout_minutes: 60
  max_failed_attempts: 5
  lockout_duration_minutes: 15

authorization:
  default_role: "user"
  admin_approval_required: true
  permission_model: "rbac"  # rbac, abac

data_classification:
  pii_fields: ["email", "phone", "ssn", "address"]
  requires_encryption: ["password", "api_key", "token"]
  audit_log_required: ["login", "permission_change", "data_access"]

compliance:
  gdpr_applicable: true
  data_retention_days: 365
  right_to_deletion: true
  consent_tracking: true
```

## Validation Checklist

Before completing validation phase with security addin:

- [ ] Threat model documented with STRIDE analysis
- [ ] Security requirements identified and implemented
- [ ] Input validation implemented for all external inputs
- [ ] Output encoding applied to prevent injection attacks
- [ ] Authentication implemented with secure mechanisms
- [ ] Authorization enforced with least-privilege principles
- [ ] Sensitive data encrypted in transit and at rest
- [ ] Secrets managed via environment variables or secret managers
- [ ] Error handling prevents information disclosure
- [ ] Audit logging implemented for security events
- [ ] Static analysis security scanning executed and clean
- [ ] Dependency vulnerabilities scanned and resolved
- [ ] Secrets detection scan executed and clean
- [ ] Security test cases implemented and passing
- [ ] Compliance requirements validated (GDPR, HIPAA, etc.)

## Best Practices

### Defense in Depth
- **Multiple layers**: Don't rely on single security control
- **Fail secure**: Default to deny access, explicit allow
- **Least privilege**: Grant minimum necessary permissions
- **Separation of duties**: Divide responsibilities to prevent abuse

### Secure by Default
- **Safe defaults**: Secure configuration out of the box
- **Opt-in privileges**: Users must request elevated access
- **Automatic protection**: Security controls enabled automatically

### Continuous Validation
- **Regular scanning**: Automated security scans in CI/CD
- **Dependency updates**: Keep libraries current with security patches
- **Penetration testing**: Periodic security assessments
- **Incident response**: Documented procedures for security events

## Common Vulnerabilities & Prevention

### OWASP Top 10

1. **Broken Access Control**: Enforce authorization checks, principle of least privilege
2. **Cryptographic Failures**: Use strong algorithms, proper key management
3. **Injection**: Parameterized queries, input validation, output encoding
4. **Insecure Design**: Threat modeling, security requirements in planning
5. **Security Misconfiguration**: Secure defaults, configuration reviews
6. **Vulnerable Components**: Dependency scanning, timely updates
7. **Authentication Failures**: Strong password policies, MFA, session management
8. **Data Integrity Failures**: Digital signatures, checksums, secure deserialization
9. **Logging Failures**: Comprehensive audit logs, anomaly detection
10. **SSRF**: URL validation, network segmentation, allowlist

## Tool References

### Static Analysis
- **Bandit** (Python): Security-focused static analyzer
- **ESLint security plugins** (JavaScript/TypeScript)
- **Semgrep**: Pattern-based code scanning
- **CodeQL**: Semantic code analysis

### Dependency Scanning
- **Safety** (Python): Known vulnerability database
- **npm audit** (Node.js): Built-in vulnerability scanner
- **Snyk**: Multi-language dependency security
- **Dependabot**: Automated dependency updates

### Secrets Detection
- **detect-secrets**: Prevents secrets in code
- **git-secrets**: Git hook for secret prevention
- **TruffleHog**: Searches for high entropy strings

### Dynamic Testing
- **OWASP ZAP**: Web application security scanner
- **Burp Suite**: Web vulnerability scanner
- **sqlmap**: Automated SQL injection testing

## References

- **OWASP**: https://owasp.org/
- **CWE**: https://cwe.mitre.org/ (Common Weakness Enumeration)
- **NIST Cybersecurity Framework**: https://www.nist.gov/cyberframework
- **Security Headers**: https://securityheaders.com/
