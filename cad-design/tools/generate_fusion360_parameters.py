#!/usr/bin/env python3
"""Generate Fusion 360 Python code for User Parameters from a JSON parameter table.

The output is a Fusion 360 add-in script that, when run inside Fusion,
calls `userParameters.add(...)` for every parameter declared in the input
JSON file.

Usage:
    generate_fusion360_parameters.py <parameters.json> <output.py>

Input format (JSON):
    [
      {"name": "outerDiameter",   "value": 80,      "unit": "mm", "comment": "Housing OD"},
      {"name": "wallThickness",   "value": 2.5,     "unit": "mm", "comment": "Default wall"},
      {"name": "innerDiameter",   "value": "outerDiameter - 2 * wallThickness",
                                  "unit": "mm", "comment": "Derived from OD/wall"}
    ]

Security
--------
This tool generates Python source code from external JSON. The generator
validates every field before embedding it:

- `name`   — must match `^[A-Za-z_][A-Za-z0-9_]{0,62}$` (Fusion 360 parameter identifier)
- `value`  — int, float, or a string formula that contains ONLY allowed chars
             (identifiers + digits + decimal point + arithmetic operators + parens + space)
- `unit`   — must be in the allow-list (mm, cm, m, in, ft, deg, rad, "")
- `comment`— string, rendered via `repr()` so no embedded quotes can escape

Any input that fails validation is rejected with a clear message. There is
no path from the JSON file to arbitrary Python execution in the generated
script.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


# ──────────────────────────────────────────────────────────────────────────
# Validators
# ──────────────────────────────────────────────────────────────────────────

_IDENT_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,62}$")
_FORMULA_RE = re.compile(r"^[A-Za-z0-9_+\-*/().\s]+$")
_UNITS = frozenset({"mm", "cm", "m", "in", "ft", "deg", "rad", ""})


def _validate_identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not _IDENT_RE.match(value):
        raise ValueError(
            f"Invalid {field} {value!r}: must match [A-Za-z_][A-Za-z0-9_]{{0,62}}"
        )
    return value


def _validate_value(value: Any) -> tuple[str, str]:
    """Return (kind, normalized_value) where kind in {'real', 'formula'}."""
    if isinstance(value, bool):
        # bool is technically int in Python — reject explicitly to avoid surprises
        raise ValueError(f"Parameter value must not be bool, got: {value!r}")
    if isinstance(value, (int, float)):
        return "real", repr(float(value))
    if isinstance(value, str):
        if not value.strip():
            raise ValueError("Parameter value string must not be empty")
        if not _FORMULA_RE.match(value):
            raise ValueError(
                f"Invalid formula {value!r}: only identifiers + digits + decimal "
                "point + arithmetic operators + parentheses + spaces are allowed"
            )
        return "formula", value
    raise ValueError(
        f"Parameter value must be int, float, or formula string — got {type(value).__name__}"
    )


def _validate_unit(value: Any) -> str:
    unit = value if value is not None else ""
    if not isinstance(unit, str) or unit not in _UNITS:
        raise ValueError(
            f"Invalid unit {value!r}: must be one of {sorted(_UNITS)}"
        )
    return unit


def _validate_comment(value: Any) -> str:
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"Comment must be string or null, got {type(value).__name__}")
    return value


# ──────────────────────────────────────────────────────────────────────────
# Code generation
# ──────────────────────────────────────────────────────────────────────────

_HEADER = '''import adsk.core, adsk.fusion


def create_parameters():
    """Create User Parameters in the active design."""
    app = adsk.core.Application.get()
    design = adsk.fusion.Design.cast(app.activeProduct)

    if not design:
        return False

    userParams = design.userParameters

    # Existing parameters left intact. To clear them, uncomment:
    # for i in range(userParams.count - 1, -1, -1):
    #     userParams.item(i).deleteMe()

'''


_FOOTER = '''    return True


def run(context):
    try:
        if create_parameters():
            print("OK: parameters created")
        else:
            print("FAIL: no active design")
    except Exception as exc:
        print(f"FAIL: {exc!s}")
'''


def generate_parameter_code(parameters: list[dict]) -> str:
    """Generate the Fusion 360 add-in script as a Python source string."""
    if not isinstance(parameters, list):
        raise ValueError("Top-level JSON must be a list of parameter objects")

    lines: list[str] = [_HEADER]
    for idx, raw in enumerate(parameters):
        if not isinstance(raw, dict):
            raise ValueError(f"Parameter at index {idx} must be a JSON object")
        name = _validate_identifier(raw.get("name"), f"parameter[{idx}].name")
        kind, val = _validate_value(raw.get("value"))
        unit = _validate_unit(raw.get("unit"))
        comment = _validate_comment(raw.get("comment"))

        # All string literals embedded in generated source go through repr()
        # so no quotes / escape sequences can break out.
        name_lit = repr(name)
        unit_lit = repr(unit)
        comment_lit = repr(comment)

        if comment:
            lines.append(f"    # {comment}\n")
        if kind == "real":
            lines.append(
                f"    userParams.add({name_lit}, "
                f"adsk.core.ValueInput.createByReal({val}), "
                f"{unit_lit}, {comment_lit})\n\n"
            )
        else:
            formula_lit = repr(val)
            lines.append(
                f"    userParams.add({name_lit}, "
                f"adsk.core.ValueInput.createByString({formula_lit}), "
                f"{unit_lit}, {comment_lit})\n\n"
            )
    lines.append(_FOOTER)
    return "".join(lines)


# ──────────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="generate_fusion360_parameters.py",
        description="Generate a Fusion 360 add-in script from a JSON parameter table.",
    )
    parser.add_argument("input_file", help="JSON file with parameter definitions")
    parser.add_argument("output_file", help="Python file to write (Fusion 360 add-in)")
    args = parser.parse_args()

    src = Path(args.input_file)
    dst = Path(args.output_file)

    try:
        parameters = json.loads(src.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: input file not found: {src}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {src}: {exc}", file=sys.stderr)
        return 2

    try:
        code = generate_parameter_code(parameters)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3

    dst.write_text(code, encoding="utf-8")
    print(f"OK: Fusion 360 parameter add-in written to {dst}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
