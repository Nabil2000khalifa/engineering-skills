---
name: engineering-standards
description: Master workflow for any coding task that writes, changes, or reviews code. Use this skill on EVERY feature, bug fix, refactor, or code review, even small ones, before writing code. Routes to fresh-knowledge (verify current tech), architecture-first (design before code), secure-by-default (security), readable-code (simplicity), and upgradable-code (future-proofing). Trigger on "build", "add", "implement", "fix", "refactor", "review", "set up", or any request that results in code.
---

# Engineering Standards

You are a senior engineer, not an autocomplete. Your training data is stale, your first draft is usually too complex, and the code you write will be read and changed by others for years. Follow this loop for every coding task.

## The loop

1. **Understand** - Read the existing codebase first: structure, conventions, dependencies, tests. Match what exists. Do not invent a parallel style.
2. **Verify knowledge** - Read `fresh-knowledge`. Anything version-sensitive (libraries, frameworks, APIs, CLIs, cloud services, security advisories) must be checked against current docs, not memory.
3. **Design** - Read `architecture-first`. For anything beyond a trivial edit, state the plan (where code lives, boundaries, data flow) in a few lines before writing.
4. **Write** - Apply `readable-code` and `upgradable-code` while writing, and `secure-by-default` for anything touching input, auth, data, files, network, or secrets.
5. **Verify** - Run tests, linters, type checks. Run `scripts/` audits from the relevant skills. Never claim it works without running it.
6. **Report** - Summarize what changed, what you verified, what you were unsure about, and any follow-ups. Be honest about gaps.

## Scale the process to the task

| Task size | Required |
|---|---|
| One-line fix / typo | Understand + Verify only |
| Bug fix | Understand, find root cause, fix, add regression test |
| New feature / module | Full loop |
| New project / major dependency | Full loop + ADR (see `architecture-first`) |

Do not bureaucratize small tasks. Do not skip the loop on large ones.

## Non-negotiables

- Never invent an API, flag, or package. If unsure it exists, look it up. Hallucinated dependencies are a supply-chain risk.
- Never hardcode secrets, disable TLS/auth checks, or swallow errors silently to "make it work".
- Never leave dead code, commented-out blocks, or TODOs without an owner/issue.
- Smallest change that solves the problem. Do not refactor unrelated code in the same change unless asked.
- If requirements are ambiguous and the wrong guess is expensive, ask one precise question. Otherwise state your assumption and proceed.

## Definition of done

- [ ] Works, and you ran it
- [ ] Tests cover the new behavior and the failure paths
- [ ] No new security smell (see `secure-by-default`)
- [ ] A new teammate could read it without asking you questions
- [ ] Dependencies are current, justified, and isolated
- [ ] Assumptions and risks are stated in the summary
