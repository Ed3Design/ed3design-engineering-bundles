# Contributing

Thanks for considering a contribution. This repository concentrates on **physical engineering disciplines** — CAD design, FDM/maker workflows, and embedded device integration — and follows a few specific conventions because skills need to be predictable for Claude Code to load and apply them correctly.

The sibling repository [`ed3design-skill-bundles`](https://github.com/Ed3Design/ed3design-skill-bundles) covers the **software-engineering** disciplines (token optimization, code-quality, planning, async-forensics, schema-discipline, skill-system-meta). If your contribution is software-engineering-flavoured, propose it there instead.

## Quick Start

```bash
git clone https://github.com/Ed3Design/ed3design-engineering-bundles
cd ed3design-engineering-bundles

# Install Claude Code CLI (if not already)
npm install -g @anthropic-ai/claude-code

# Validate all bundles
for d in cad-design embedded-systems maker-fdm; do
  claude plugin validate --strict "$d"
done

# Run the audit suite (matches what CI runs on PR)
python3 -m pip install pyyaml
python3 scripts/audit-skill-descriptions.py --check
```

## Adding a Skill to a Bundle

### Decide on the right bundle

A skill belongs in a bundle if it matches one of the 3 thematic domains:

- **`cad-design`** — parametric CAD (Fusion 360, SolidWorks, Onshape, FreeCAD, Inventor), construction workflows, mechanical design rules, CAD-API automation, image-to-mesh-to-CAD bridges
- **`maker-fdm`** — FDM 3D-printing (BOM validation, embedded GUI documentation from source, slicer profiles, support strategies, material matching)
- **`embedded-systems`** — device integration via Modbus / CAN / I2C / SPI / serial / dbus (battery monitors, energy controllers, Victron / Cerbo / VE.Direct, ESP32 / Arduino patterns that target physical hardware)

If your skill doesn't fit any of these, propose a new bundle in an issue first.

### Skill format

Each skill lives in `<bundle>/skills/<skill-name>/SKILL.md` with this frontmatter:

```markdown
---
name: <skill-name>
description: |-
  Use when <trigger conditions>. <one-line value proposition>. Trigger on phrases like "<phrase 1>", "<phrase 2>". Do NOT load for <anti-trigger conditions>.
---

# <Skill Title>

## When to use
...

## When NOT to use
...

## How to use
...

## Anti-patterns
...
```

The `description` field is critical — Claude Code uses it for auto-discovery. Make sure:

- It contains specific trigger phrases users would type (verbatim, in quotes)
- It contains explicit `Do NOT load for ...` patterns to prevent over-triggering
- It is **third-person narrative** outside the quoted trigger phrases (no "I", "we", "my", "our" in the wrapping prose — these inject into the system prompt as Claude's narration)
- It stays **≤ 1024 characters** (a soft spec limit; CI now hard-fails on this)
- It uses block-scalar form (`description: |-`) when the value contains a colon or any character YAML treats specially — otherwise the frontmatter silently parses to empty metadata at runtime and the skill never triggers

### Promotion before merge

Promotion of a draft skill follows the workflow in [`ed3design-skill-bundles`](https://github.com/Ed3Design/ed3design-skill-bundles)'s `skill-system-meta/skills/skill-tdd-promotion-workflow`:

1. **RED subagent** (without skill) tries to solve the trigger scenario → demonstrates the natural anti-pattern
2. **GREEN subagent** (with skill) tries the same scenario → demonstrates the skill's value
3. Both subagents reflect on the skill (Self-Reflection section)
4. If RED shows a clear anti-pattern AND GREEN shows clear compliance → PROMOTE
5. Otherwise: refactor skill and re-run cycle

Once promoted, do NOT carry an `⚠️ DRAFT` banner or a `## Promotion Checklist` section in the public skill body — CI rejects both. Internal TDD-progression notes belong in private maintainer notes, not in a marketplace artifact.

## Adding a Python Tool

Python tools live in `<bundle>/tools/<tool-name>.py` (NOT inside an individual skill's `scripts/` directory — that pattern hides them from `${CLAUDE_PLUGIN_ROOT}/tools` discovery). Style conventions:

- Shebang `#!/usr/bin/env python3`, file is `chmod +x`
- Docstring at the top with usage examples — and the filename in the usage MUST match the actual filename
- `argparse` for CLI args; `--help` must work even if optional dependencies are missing (lazy import them inside the subcommands that need them)
- JSON output as primary format (token-efficient)
- Standard library + 1-2 well-tested deps only
- For tools that GENERATE code from external input: never interpolate the input directly into the generated source. Validate the schema first, then use `repr()` / `json.dumps()` / allow-listed identifier patterns to produce safe literals. Code-injection via parameter files is a real attack surface even for "internal" tools.

When a skill references a tool, use the portable path pattern:

```bash
${CLAUDE_PLUGIN_ROOT:-$HOME/.claude}/tools/<tool-name>.py
```

This works both in the plugin context and when installed locally.

## Pull Request Workflow

1. Fork the repo
2. Create a feature branch: `git checkout -b add-<bundle>-<skill-name>`
3. Add your skill / tool
4. Update the bundle's `README.md` with a row in the trigger table
5. Update `plugin.json` if the structure changed
6. Bump the bundle's `version` in `plugin.json` (semver: patch for fixes, minor for additions, major for breaking)
7. Run the local audit suite (validator + description audit + py_compile) — CI runs the same gates and will fail the PR otherwise
8. Open a PR with:
   - **Title**: `feat(<bundle>): add <skill-name>` (or `fix:` / `docs:` / `refactor:`)
   - **Body**: empirical value proposition + (for new skills) a RED-vs-GREEN comparison from the promotion cycle

## Code of Conduct

See `CODE_OF_CONDUCT.md`. Short version: be specific, be direct about technical disagreements, no personal attacks, no gatekeeping.

## License

By contributing, you agree your contributions will be licensed under the same MIT license as the rest of the repo.
