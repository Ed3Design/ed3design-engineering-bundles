# ed3design-engineering-bundles

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Engineering-discipline library for Claude Code power users — hardware/maker focus. 8 skills across 3 thematic bundles covering parametric CAD, FDM/maker workflows, and embedded systems integration.

Sibling to [`ed3design-skill-bundles`](https://github.com/Ed3Design/ed3design-skill-bundles) (software-engineering focus). This repo concentrates on the **physical engineering** disciplines: CAD design, 3D-printed builds, embedded device onboarding.

## 📦 Bundles

| Bundle | Skills | Status |
|---|---|---|
| [`cad-design`](./cad-design/) | 5 (CAD API scripting, construction workflows, mechanical design principles, image-to-mesh, Fusion MCP-Bridge) | ✅ v0.1.0 |
| [`maker-fdm`](./maker-fdm/) | 2 (BOM validation, embedded GUI documentation) | ✅ v0.1.0 |
| [`embedded-systems`](./embedded-systems/) | 1 (Victron Cerbo GX Modbus onboarding — `Enabled=0` default trap) | ✅ v0.1.0 |

**Total**: 8 skills — patterns extracted from real-world physical engineering practice and structured for reuse.

## 🚀 Quickstart

### Via Claude Code Marketplace

```
/plugin marketplace add Ed3Design/ed3design-engineering-bundles
/plugin install cad-design@ed3design-engineering-bundles
/plugin install maker-fdm@ed3design-engineering-bundles
/plugin install embedded-systems@ed3design-engineering-bundles
```

### Manual Install

```bash
git clone https://github.com/Ed3Design/ed3design-engineering-bundles
ln -s "$(pwd)/ed3design-engineering-bundles/cad-design/skills"/* ~/.claude/skills/
ln -s "$(pwd)/ed3design-engineering-bundles/maker-fdm/skills"/* ~/.claude/skills/
ln -s "$(pwd)/ed3design-engineering-bundles/embedded-systems/skills"/* ~/.claude/skills/
```

## 🧭 Why a separate repo from `ed3design-skill-bundles`?

The software-engineering bundles (token-savers, code-quality, planning, schema-discipline, etc.) share an audience: developers who write code. The hardware/maker bundles share a different audience: makers, mechanical engineers, embedded-systems hobbyists. Splitting them into two repos makes discovery clearer for both audiences and lets each repo grow without bloating the other.

## 🔗 Related

- **`ed3design-skill-bundles`** — software engineering: token optimization, code quality, planning, async/SQL debugging, skill-system meta
- **`ed3design`** brand: maker-focused engineering tools for makers, makers' AI workflows, and CAD/3D-printing automation

## 📚 Pattern Compound

A typical hardware engineering session might layer these bundles:

1. **`cad-design`** — design the part (parametric CAD, MCP-Bridge for closed-loop iteration)
2. **`maker-fdm`** — validate the BOM before ordering, document the embedded UI from source
3. **`embedded-systems`** — onboard the new Victron/Modbus device on first connection

Each bundle works standalone, but loaded together they cover the design → build → integrate flow end-to-end.

## License

MIT. See [LICENSE](LICENSE).
