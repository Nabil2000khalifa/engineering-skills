---
name: architecture-first
description: Design before code. Use when building a new feature, module, service, or project, when touching more than one file, when deciding where code should live, when adding a dependency or integration, when the codebase feels messy, or when asked to review or improve architecture. Prevents spaghetti, god files, circular dependencies, and logic in the wrong layer. Make sure to use this before writing any non-trivial code, even if the user only says "just add X".
---

# Architecture First

Most bad codebases are not caused by bad syntax. They are caused by code placed in the wrong spot, with the wrong dependencies, decided without thinking. Spend two minutes designing; save two weeks of untangling.

## Step 1: Learn the existing architecture

Before proposing anything:
- Map the directory structure and identify the pattern in use (layered, feature folders, hexagonal, MVC, monorepo packages...)
- Find where similar functionality already lives and copy that shape
- Find the existing conventions for errors, config, logging, data access, and tests
- Check for docs: README, `docs/`, ADRs, `AGENTS.md`, `CONTRIBUTING.md`

**Follow the existing architecture unless it is the problem.** If you believe it is wrong, say so and propose a change separately. Do not silently introduce a second pattern.

## Step 2: Write a mini design (3-8 lines, in your reply)

For any non-trivial change, state:
- **Goal**: one sentence
- **Where it lives**: files/modules to create or touch, and why there
- **Boundaries**: what it depends on, what depends on it
- **Data flow**: input -> processing -> output/side effects
- **Failure modes**: what can go wrong and how it's handled
- **Rejected alternative**: one option you didn't pick and why

If the change is large or hard to reverse, write an ADR (`references/adr-template.md`).

## Design rules

1. **Dependencies point inward.** Business logic must not import from UI, HTTP framework, or DB driver. Outer layers depend on inner ones, never the reverse.
2. **Separate decisions from effects.** Put pure logic (calculate, validate, transform) in functions with no I/O. Keep I/O (DB, network, filesystem, clock, randomness) at the edges. This makes code testable and replaceable.
3. **One reason to change per module.** If a file mixes parsing, business rules, and persistence, split it.
4. **No cycles.** If A imports B and B imports A, extract the shared piece into C.
5. **Explicit boundaries.** Each module exposes a small public surface (an index/`__init__`/interface). Other modules use only that.
6. **Config in one place.** No `process.env` / `os.environ` scattered through business code. Load once, validate, inject.
7. **Make illegal states unrepresentable.** Use types, enums, and validation at the boundary so bad data can't travel inward.
8. **Don't abstract early.** Wait for the second or third real use before generalizing. Duplication is cheaper than the wrong abstraction. But do wrap external services (see `upgradable-code`).
9. **YAGNI.** No plugin systems, factories, or config flags for needs nobody has.

## Smells that mean "stop and redesign"

- A file over ~400 lines or a function over ~50
- A module imported by "everything"
- `utils`, `helpers`, `common` growing without a clear theme
- Business rules inside controllers/route handlers/components
- Same data shape redefined in several places
- Tests that need a real database/network to test a calculation
- Changes that always require editing 5+ files

## Output

Include the mini design before the code. After coding, note any architectural debt you found but did not fix.
