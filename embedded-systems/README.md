# embedded-systems

Embedded systems integration disciplines for energy management and device onboarding under Claude Code.

## Skills

| Skill | Trigger | Value |
|---|---|---|
| **victron-cerbo-modbus-device-onboarding** | New Victron Modbus-TCP device (EV charger, energy meter, inverter) on the Cerbo GX LAN but not visible in the UI or D-Bus | Encodes the non-obvious `Enabled=0` default: `dbus-modbus-client` discovers new devices on the Modbus subnet scan but registers them disabled. 5-step diagnostic sequence + `dbus-send` fix + BusyBox compatibility table for Venus OS shell quirks. |

## Why this bundle?

Embedded energy management and IoT integration repeatedly hit the same class of failure mode: a device is **physically connected and network-reachable**, but **invisible to the management UI** because of a default setting hidden inside the host's settings store. Without explicit documentation, diagnosing this takes hours of generic-troubleshooting false trails (VLAN, firmware, power-cycle).

The first skill in this bundle encodes one such case — Victron's Cerbo GX with its `Enabled=0` Modbus-default. The pattern itself (subnet-scan-discovers + UI-hides-by-default) recurs across other ecosystems; future skills in this bundle will cover analogous cases for other embedded platforms.

## Installation

```
/plugin marketplace add Ed3Design/ed3design-engineering-bundles
/plugin install embedded-systems@ed3design-engineering-bundles
```

Or manual:

```bash
git clone https://github.com/Ed3Design/ed3design-engineering-bundles ~/.claude/plugins/
```

## Cross-references

- `cad-design` bundle — for the design side of physical engineering (parametric CAD, Fusion 360 MCP-Bridge)
- `maker-fdm` bundle — for the build side (BOM validation, embedded GUI documentation)

## License

MIT
