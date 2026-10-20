# Contributing

## Adding or changing a skill
1. One skill = one failure mode. Keep `SKILL.md` under ~500 lines; push detail into `references/`.
2. `description` frontmatter is the trigger. State what it does AND when to use it, with concrete trigger words.
3. Write instructions as reasoning ("do X because Y"), not just commands.
4. Put deterministic work in `scripts/` (stdlib only where possible).
5. Add at least one case to `evals/evals.json` showing the failure your change fixes.
6. Run `python -m py_compile` on scripts and the CI checks locally.

## Style
- Be specific and verifiable. "Functions under ~30 lines" beats "keep functions small".
- No vendor hype, no filler.
