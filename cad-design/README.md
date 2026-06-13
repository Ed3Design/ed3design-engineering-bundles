# cad-design

> Parametric CAD design disciplines for makers, mechanical engineers, and product designers.

## Skills (5)

| Skill | Domain |
|---|---|
| `cad-api-scripting` | Python for commercial CAD platforms (Fusion 360, etc.) + OpenSCAD scripts. Programmatic modeling, geometry generation, automation |
| `cad-construction` | Structured workflow: design concept → parametric CAD model. Component decomposition, parameter hierarchy, construction sequencing. The **HOW** of CAD work |
| `mechanical-design-principles` | Design rules for elegant + manufacturable + serviceable solutions. Tool-less assembly, monolithic parts, overhang/wall guidelines. The **WHAT and WHY** of mechanical design |
| `image-to-mesh-cad-workflow` | End-to-end: 2D concept image → 3D parametric CAD. Uses image-to-3D-mesh services (Tripo3D etc.) when manual outline tracing is unreliable |
| `fusion-mcp-bridge` | Fusion 360 driven from Claude Code via a localhost MCP-Bridge (HTTP server + bearer-token + single-threaded Custom-Event handler). Encodes the API quirks that consistently bite without explicit guidance: component activation, single-revolve over loft+combine, cut-before-shell sequencing, bridge timeout/lock recovery |

## Pattern Compound

`mechanical-design-principles` (WHAT/WHY) → `cad-construction` (HOW) → `cad-api-scripting` (AUTOMATE) → `fusion-mcp-bridge` (AUTOMATE-VIA-CLAUDE). These four skills layer naturally: principles inform construction, construction informs scripting, scripting can be driven directly by Claude through the MCP-Bridge for closed-loop iteration. `image-to-mesh-cad-workflow` is the pre-step when you have an image but no clean outline.

## Installation

```bash
git clone https://github.com/Ed3Design/ed3design-engineering-bundles
ln -s "$(pwd)/ed3design-engineering-bundles/cad-design/skills"/* ~/.claude/skills/
```

Or via Claude Code marketplace (when registered):
```
/plugin marketplace add Ed3Design/ed3design-engineering-bundles
/plugin install cad-design@ed3design-engineering-bundles
```

## Related Bundles

- `maker-fdm` — BOM validation + embedded UI documentation for physical builds
- `embedded-systems` — Victron Cerbo GX Modbus device onboarding (and future embedded integration patterns)

## License

MIT.
