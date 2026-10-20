---
name: fresh-knowledge
description: Prevents stale-knowledge bugs. Use whenever code involves a library, framework, SDK, API, CLI tool, cloud service, language feature, or dependency version, and whenever choosing a technology, adding a package, upgrading, or when something "should work" but errors. Forces verification against current official docs, changelogs, and registries instead of trusting training memory. Use even when you feel confident, since confidence is exactly when stale knowledge hurts.
---

# Fresh Knowledge

Your training data has a cutoff. Libraries ship breaking changes, APIs get deprecated, new tools replace old ones, and CVEs appear after your cutoff. Treat your memory as a **hypothesis to verify**, not a fact.

## When you MUST verify

- Adding or using any third-party package, SDK, or framework API
- Picking a version, or writing install commands / config files
- Anything touching auth, crypto, payments, cloud, or AI model APIs (fast-moving, high-impact)
- Any error that suggests a signature, import path, or option changed
- Choosing between technologies ("what should I use for X?")
- The user mentions a tool, version, or release you don't recognize. Unknown does not mean fake, and does not mean you can guess.

## Verification procedure

1. **Detect what's pinned.** Read lockfiles/manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`...). Code must target the version actually installed, not the one you remember.
2. **Run** `python scripts/check_deps.py <project-dir>` to compare declared versions with the latest in the registry and flag deprecated packages.
3. **Read primary sources, in this order:**
   1. Official docs for the *installed* version
   2. Changelog / release notes / migration guide
   3. Source repo (README, issues, releases)
   4. Registry page (npm, PyPI, crates.io, pkg.go.dev)

   Prefer a docs tool (Context7 MCP, web search, web fetch) if available. Blog posts and Stack Overflow are last resort and often outdated.
4. **Check the date.** Anything older than ~12 months on a fast-moving tool needs a second source.
5. **Check security.** Look for advisories (`npm audit`, `pip-audit`, `cargo audit`, GitHub Advisories, OSV) before adding or keeping a dependency.
6. **If you cannot verify**, say so explicitly: "I believe X, but couldn't confirm against current docs." Never present a guess as fact.

## Choosing a dependency (checklist)

Before adding a package, confirm:
- Actively maintained (recent release and commits, issues answered)
- Compatible license
- No known critical vulnerabilities
- Reasonable size and transitive dependency count
- The standard library or an existing dependency doesn't already do this. If it does, use that.
- Would removing it later be hard? If yes, wrap it (see `upgradable-code`).

## Output habit

When you used external knowledge, add a short note in your summary: what you verified, the version you targeted, and the source. Example:
> Targeted `zod@4.x` (checked official migration guide). `z.string().email()` is deprecated there; used `z.email()`.

## Anti-patterns

- "I remember this API" with no check
- Copying install commands from memory
- Using a deprecated API because it's what appears most in training data
- Upgrading everything blindly. Read breaking changes first, upgrade in small steps, run tests.
