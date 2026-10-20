# Security Review Checklist (OWASP Top 10 aligned)

Use for reviews and before shipping. Mark each: pass / fail / n/a.

## A01 Broken Access Control
- [ ] Every endpoint enforces authN + authZ server-side
- [ ] Object-level ownership checks (no IDOR)
- [ ] Deny by default; admin routes separated and protected
- [ ] CORS restricted; no wildcard with credentials

## A02 Cryptographic Failures
- [ ] TLS everywhere; no cert verification disabled
- [ ] Passwords hashed with argon2id/bcrypt/scrypt
- [ ] No hardcoded keys; keys rotatable
- [ ] Sensitive data not in logs, URLs, or client storage

## A03 Injection
- [ ] Parameterized queries / ORM bindings
- [ ] No shell string building; no `eval`/`exec` on input
- [ ] Output encoding / auto-escaping for HTML, JS, URLs
- [ ] Path inputs normalized and confined

## A04 Insecure Design
- [ ] Threat model considered for new features
- [ ] Rate limits, quotas, and abuse cases handled
- [ ] Business-logic races covered (transactions, unique constraints)

## A05 Security Misconfiguration
- [ ] Debug off in production; no default creds
- [ ] Security headers set; error pages generic
- [ ] Containers non-root; minimal images; least-privilege IAM

## A06 Vulnerable / Outdated Components
- [ ] Lockfile committed; audit run (npm audit, pip-audit, cargo audit, osv-scanner)
- [ ] No deprecated or abandoned dependencies
- [ ] Each dependency exists, is the intended one, and is justified

## A07 Identification & Authentication Failures
- [ ] Brute-force protection; MFA where appropriate
- [ ] Sessions rotate on login, expire, and invalidate on logout
- [ ] Reset flows use single-use, expiring tokens

## A08 Software & Data Integrity Failures
- [ ] No unsafe deserialization
- [ ] CI/CD secrets scoped; third-party actions pinned by SHA
- [ ] Updates/artifacts verified

## A09 Logging & Monitoring Failures
- [ ] Auth events, access denials, and admin actions logged
- [ ] No secrets/PII in logs; logs tamper-resistant

## A10 SSRF
- [ ] Outbound requests to user-supplied URLs are allowlisted
- [ ] Internal/metadata IP ranges blocked
