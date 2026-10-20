---
name: readable-code
description: Keep code simple, readable, and maintainable. Use whenever writing, refactoring, or reviewing code, and when the user says code is hard to read, too complex, messy, over-engineered, long, confusing, or needs cleanup or simplification. Also use before finishing any implementation to simplify your own first draft. Enforces small functions, clear names, flat control flow, no dead code, and comments that explain why.
---

# Readable Code

Code is read far more than it is written. Your first draft is almost always more complex than necessary. Simplify it before you hand it over.

## The test

> Could a competent teammate who has never seen this file understand what it does in under a minute, and change it safely?

If not, simplify.

## Rules

**Naming**
- Names reveal intent: `daysUntilExpiry`, not `d`; `isEligible`, not `flag`.
- Functions are verbs (`parseInvoice`), booleans read as questions (`hasAccess`), no abbreviations unless universal.
- If you need a comment to explain a name, rename it.

**Functions**
- Do one thing. Aim for under ~30 lines, 4 or fewer parameters (use an object/dataclass beyond that).
- Use early returns / guard clauses instead of deep nesting. Keep nesting to 3 levels or fewer.
- Avoid boolean flag parameters that switch behavior. Split into two functions.
- Prefer pure functions. Isolate side effects.

**Structure**
- Group by feature/domain, not by technical type, when the codebase allows.
- Keep related code together; keep files focused (under ~300 lines is a good target).
- Public API first, helpers after. Consistent ordering across files.

**Control flow and data**
- Replace magic numbers/strings with named constants or enums.
- Prefer clear straight-line code over clever one-liners, nested ternaries, or dense chained expressions.
- Use language built-ins and standard idioms before custom helpers.
- Model data with types/classes instead of anonymous dicts/arrays passed around.

**Comments**
- Code says *what*; comments say *why* (business rule, trade-off, workaround, link to issue).
- Delete comments that restate code. Delete commented-out code. Version control remembers.
- Public APIs get docstrings: purpose, params, returns, errors.

**Errors**
- Handle errors where you can act on them; otherwise let them propagate with context.
- Never use empty `catch`/`except`. Never return `null`/`None` to signal failure when an error or result type is clearer.
- Error messages say what happened and what to do.

**Delete**
- Remove unused code, imports, parameters, and flags. The best code is code that doesn't exist.
- Don't build for hypothetical futures (see `architecture-first`: YAGNI).

## Simplification pass (do this before finishing)

1. Re-read your diff as a reviewer. What would confuse you?
2. Run `python scripts/complexity_check.py <dir>` and fix flagged functions.
3. Inline abstractions used once. Extract blocks that need a comment into a named function.
4. Remove anything the task didn't require.
5. Run formatter, linter, and tests. Use the project's own config; don't introduce new tools.

## Refactoring existing code

- Refactor only with tests around it. If there are none, write characterization tests first.
- Small, behavior-preserving steps; run tests between them.
- Keep refactors separate from feature changes (separate commits).
- Never rewrite wholesale when incremental change works.

## Before / after

```python
# Before: nested, flag-driven, cryptic
def p(d, f):
    if d:
        if d.get("u"):
            if f:
                return d["u"].upper()
            else:
                return d["u"]
    return None

# After: guard clauses, intent-revealing, no flag
def normalized_username(data: dict) -> str | None:
    username = data.get("u")
    return username.upper() if username else None
```
