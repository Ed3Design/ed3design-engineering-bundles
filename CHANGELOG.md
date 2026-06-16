# Changelog

All notable changes to this repository are tracked here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html) at the per-bundle level.

## [Unreleased]

### Added

- `CHANGELOG.md` (this file)
- `.github/dependabot.yml` — weekly batched updates for GitHub Actions and the Claude Code CLI (npm); major-version bumps need manual review
- `.github/CODEOWNERS` — default + per-bundle ownership
- `scripts/test-tools-smoke.sh` — behavioral smoke-test that invokes `generate_fusion360_parameters.py` against a real fixture and compiles the generated add-in (CI step added). `--help`-only checks are insufficient; this exercises the documented happy path end-to-end
- CI step running the behavioral tool smoke-test

### Fixed

- 3 cross-references in skill bodies pointed at skills that are not published in any public bundle. `review-qa` (in `cad-construction`) and `ed3dworks-brand` (in `bom-validation-workflow`) were genericized so a public user is not promised an unavailable skill; a "Hardware-stock vault note" reference was genericized to "a hardware-stock inventory"
- `bom-validation-workflow` origin-narrative referenced a non-existent `bom-validator` skill name — reworded to a neutral design note

## [0.1.0] — 2026-06-15

First marketplace release (merge commit `9b06875`, PR #1 — 4-axis audit, 11 release-blocking findings fixed). A `v0.1.0` git tag is not yet cut:

- 4 broken YAML frontmatters fixed (block-scalar conversion) — `cad-api-scripting`, `mechanical-design-principles`, `bom-validation-workflow`, `embedded-ui-svg-doc-from-source` had previously loaded with empty metadata
- Private paths and machine identifiers scrubbed from skill bodies and the helper tool
- 3-bundle structure: `cad-design` (5 skills + 1 tool), `maker-fdm` (2 skills), `embedded-systems` (1 skill)
- CI uses official `claude plugin validate --strict` per bundle
- Governance files added: `SECURITY.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, issue + PR templates

Sibling repository: [`ed3design-skill-bundles`](https://github.com/Ed3Design/ed3design-skill-bundles) for software-engineering disciplines.

[Unreleased]: https://github.com/Ed3Design/ed3design-engineering-bundles/compare/9b06875...HEAD
[0.1.0]: https://github.com/Ed3Design/ed3design-engineering-bundles/commit/9b06875
