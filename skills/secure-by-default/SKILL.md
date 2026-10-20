---
name: secure-by-default
description: Security guardrails for all code. Use whenever code handles user input, authentication, authorization, sessions, passwords, tokens, API keys, secrets, databases, SQL, file uploads or paths, HTTP requests, shell commands, deserialization, cryptography, payments, personal data, logging, CORS, or dependencies. Also use for any security review or audit. Apply proactively even if the user never mentions security, since insecure code is the default failure mode of generated code.
---

# Secure by Default

Generated code is often insecure because it optimizes for "works". Assume all input is hostile, all dependencies are suspect, and all secrets will leak if given a chance.

## Core rules (always)

1. **Validate at the boundary.** Parse and validate every external input (HTTP, CLI, files, env, queues, LLM output) with a schema. Allowlist, don't blocklist. Reject early.
2. **Parameterize.** Never build SQL, shell commands, HTML, LDAP, or paths by string concatenation with untrusted data. Use prepared statements, argument arrays (no `shell=True`), templating with auto-escape, and path normalization + base-directory checks.
3. **Authenticate and authorize every request on the server.** Check ownership on every object access (prevents IDOR). Never trust client-side checks, hidden fields, or user-supplied IDs/roles.
4. **No secrets in code, logs, URLs, or git.** Use environment/secret manager. Ship a `.env.example` with fake values. Add `.env` to `.gitignore`. If a secret was ever committed, rotate it. Deleting the commit is not enough.
5. **Use proven crypto, never invent it.** Passwords: argon2id / bcrypt / scrypt. Random: CSPRNG (`secrets`, `crypto.randomBytes`), never `Math.random`/`random`. Encryption: vetted libraries with AEAD (AES-GCM, ChaCha20-Poly1305). No MD5/SHA1 for security, no ECB, no hardcoded IVs/keys.
6. **Least privilege.** Minimal DB grants, scoped tokens, non-root containers, narrow CORS (no `*` with credentials), narrow IAM.
7. **Fail closed, fail quietly to users, loudly to logs.** Generic error messages outward (no stack traces, SQL, or internal paths); detailed structured logs inward, without secrets or PII.
8. **Secure defaults for cookies and headers.** `HttpOnly`, `Secure`, `SameSite`; CSRF protection for cookie auth; CSP, HSTS, `X-Content-Type-Options`.
9. **Rate limit and size limit.** Login, signup, password reset, expensive endpoints, uploads, request bodies.
10. **Supply chain.** Pin versions, commit lockfiles, run an audit tool, avoid obscure packages, and verify the package exists and is the real one (typosquatting, hallucinated names). See `fresh-knowledge`.

## Specific pitfalls

- **Uploads**: check type by content, randomize filenames, store outside web root, cap size, never execute.
- **Deserialization**: no `pickle`/`yaml.load`/Java native deserialization on untrusted data.
- **SSRF**: when fetching user-supplied URLs, allowlist hosts and block internal/metadata IP ranges.
- **Redirects**: allowlist targets to avoid open redirects.
- **JWT**: verify signature and algorithm explicitly, check `exp`/`aud`/`iss`, keep short-lived.
- **Mass assignment**: map explicit fields; don't spread request bodies into models.
- **Race conditions**: use transactions/unique constraints for balance, inventory, and one-time-use tokens.
- **LLM/agent features**: treat model output and retrieved content as untrusted input; never pass it to shell/SQL/eval; limit tool permissions; guard against prompt injection from documents and web pages.

## Procedure

1. Identify trust boundaries in the code you're writing (where untrusted data enters, where secrets live, where privilege changes).
2. Write code applying the rules above.
3. Run `python scripts/scan_secrets.py <dir>` before finishing.
4. For deeper review use `references/checklist.md` (OWASP-aligned).
5. In your summary, list security-relevant decisions and anything deliberately left open.

## If you find a vulnerability in existing code

Report it plainly with severity, location, impact, and fix. Fix it if in scope; otherwise flag it. Never hide it to keep the change small.
