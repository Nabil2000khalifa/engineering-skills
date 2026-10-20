# engineering-skills

Skills that make AI coding agents write **current, secure, simple, upgradable** code.

Coding agents fail in predictable ways. Each skill here targets one failure:

| Problem | Skill | What it does |
|---|---|---|
| Agent only knows old tech, invents APIs and packages | [`fresh-knowledge`](skills/fresh-knowledge) | Forces verification against current docs, changelogs, and registries. Includes a dependency checker script. |
| Messy architecture, logic in the wrong place | [`architecture-first`](skills/architecture-first) | Design before code, follow existing patterns, dependency rules, ADR template. |
| Insecure code (injection, leaked secrets, weak auth) | [`secure-by-default`](skills/secure-by-default) | Security rules applied by default, OWASP checklist, secret/risk scanner. |
| Hard to read, over-engineered code | [`readable-code`](skills/readable-code) | Naming, small functions, simplification pass, complexity checker. |
| Code that's painful to change or upgrade | [`upgradable-code`](skills/upgradable-code) | Dependency seams, tests as upgrade net, reversible changes. |
| Agent skips all of the above | [`engineering-standards`](skills/engineering-standards) | Master loop that routes to the other skills on every coding task. |

## Install

Skills follow the open `SKILL.md` format (folder with a `SKILL.md` + optional `scripts/` and `references/`).

**Claude Code**
```bash
git clone https://github.com/<you>/engineering-skills
mkdir -p ~/.claude/skills && cp -r engineering-skills/skills/* ~/.claude/skills/
# or per-project:  .claude/skills/
```

**Claude.ai / Claude app**: zip each folder in `skills/` and upload under Settings -> Capabilities -> Skills.

**Other agents (Cursor, Codex, Copilot, Gemini CLI, Windsurf, etc.)**: they don't all load `SKILL.md` natively. Copy [`AGENTS.md`](AGENTS.md) into your project root (or the tool's rules file). It inlines the core rules and points at the skill files.

## Use the scripts directly

```bash
python skills/fresh-knowledge/scripts/check_deps.py .        # outdated/deprecated deps
python skills/secure-by-default/scripts/scan_secrets.py .    # secrets + risky patterns
python skills/readable-code/scripts/complexity_check.py .    # long/complex functions
```
Stdlib only, Python 3.9+. These are also run in CI (`.github/workflows/ci.yml`).

## Honest limitations

- Skills guide the agent; they don't force it. Trigger rates depend on the agent. Descriptions are written to trigger often, but test on your own tasks.
- `fresh-knowledge` only helps if the agent has web/docs access. Without it, the skill makes the agent *admit uncertainty* instead of guessing, which is still an improvement.
- The scanners are heuristics. Use real tools (gitleaks, semgrep, `npm audit`, `pip-audit`) in CI as well.

## Evaluate it

`evals/evals.json` has test prompts with pass/fail expectations. Run each prompt with and without the skills and compare. Add a case every time you see an agent fail in a new way; that's how this repo improves.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Roadmap ideas: language-specific packs (`python-pro`, `typescript-pro`, `go-pro`), `testing-strategy`, `api-design`, `performance`, `observability`, `db-migrations`, an MCP server for live "what's current" lookups.

## License

MIT
