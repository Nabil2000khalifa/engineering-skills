---
name: upgradable-code
description: Write code that is easy to change, extend, test, and upgrade later. Use when adding dependencies or third-party integrations, designing APIs or data models, writing database migrations, handling config, adding tests, planning refactors or version upgrades, or whenever the user mentions maintainability, future changes, tech debt, migration, scalability, or "we may switch X later". Ensures dependencies are isolated, behavior is tested, and changes are reversible.
---

# Upgradable Code

Everything you write will be changed, and every dependency you pick will eventually be replaced or broken by an upgrade. Design so change is cheap and safe.

## 1. Isolate dependencies behind seams

- Wrap third-party SDKs/services (payments, email, storage, LLMs, analytics) behind a small interface owned by *your* code. Business logic calls your interface, not the vendor SDK.
- Keep vendor-specific types from leaking across the codebase. Translate at the boundary.
- One module per external dependency makes upgrading or swapping a single-file change.
- Don't wrap the standard library or trivially stable things. Wrap what's volatile or vendor-owned.

## 2. Tests are the upgrade safety net

- Every new behavior gets a test; every bug fix gets a regression test.
- Test behavior and public interfaces, not private internals, so refactors don't break tests.
- Keep the core logic pure so it's tested without mocks (see `architecture-first`).
- Add contract tests for the seams: the same tests should pass for the real adapter and a fake.
- Don't upgrade without a green test suite first. If coverage is missing around the affected area, add characterization tests before you change anything.

## 3. Make change reversible and incremental

- Small commits, one purpose each. Separate refactors, upgrades, and features.
- DB changes: use migrations only; make them backward compatible (expand -> migrate -> contract). Never edit a shipped migration.
- Roll out risky changes behind a flag with a removal date and owner. Delete flags after rollout.
- API changes: version public APIs, add before you remove, deprecate with a clear message and timeline.
- Persisted/serialized formats carry a version field.

## 4. Configuration and constants

- No hardcoded environment values, URLs, or limits. Centralize and validate config at startup; fail fast on missing config.
- Document each setting (purpose, default, valid values) in one place.

## 5. Dependency hygiene

- Pin via lockfile; update regularly in small batches rather than rarely in a big bang.
- Prefer fewer, well-maintained dependencies. Remove unused ones.
- Before a major upgrade: read the changelog and migration guide (`fresh-knowledge`), upgrade one thing at a time, run tests, and note breaking changes in the PR.
- Automate updates (Dependabot/Renovate) with CI as the gate.

## 6. Leave the next person a map

- Update README / docs when behavior, setup, or architecture changes.
- Record significant decisions as short ADRs (`architecture-first/references/adr-template.md`).
- Mark known debt with `TODO(owner, issue-link): what and why`. No orphan TODOs.
- In your summary, list: what's fragile, what you'd do next, and what to watch on upgrade.

## Quick review questions

- If vendor X vanished tomorrow, how many files change? (Target: 1-2.)
- If this library ships a major version, where does it break and would tests tell us?
- Can this change be rolled back without data loss?
- Would a new hire find where to extend this without reading everything?
