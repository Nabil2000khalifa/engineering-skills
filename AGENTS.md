# Agent Instructions: Engineering Standards

For agents without native `SKILL.md` support. Full detail lives in `skills/*/SKILL.md`; read the relevant file when a rule applies.

## Loop for every coding task
1. **Understand**: read existing code, conventions, tests. Match them.
2. **Verify knowledge**: your training data is stale. Check current docs/changelogs for any library, API, version, or tool before using it. Never invent APIs or packages. If you can't verify, say so. (`skills/fresh-knowledge`)
3. **Design**: for non-trivial work, state goal, where code lives, boundaries, data flow, failure modes before coding. Follow the existing architecture. (`skills/architecture-first`)
4. **Write**: simple, readable, small functions, intent-revealing names, no dead code (`skills/readable-code`); wrap third-party dependencies behind your own interface and add tests (`skills/upgradable-code`).
5. **Secure**: validate all input, parameterize queries/commands, check authz on every access, no secrets in code, vetted crypto only, least privilege (`skills/secure-by-default`).
6. **Verify**: run tests, linter, type checker, and the scripts below. Don't claim it works unless you ran it.
7. **Report**: what changed, what you verified, assumptions, risks, follow-ups.

## Scripts
- `python skills/fresh-knowledge/scripts/check_deps.py .`
- `python skills/secure-by-default/scripts/scan_secrets.py .`
- `python skills/readable-code/scripts/complexity_check.py .`

## Never
- Hardcode secrets, disable TLS/auth checks, swallow errors silently
- Leave commented-out code or ownerless TODOs
- Mix refactors with feature changes
- Add a dependency without checking it exists, is maintained, and is needed
