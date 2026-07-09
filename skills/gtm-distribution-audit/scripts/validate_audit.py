#!/usr/bin/env python3
"""Validate a GTM audit-data JSON file against audit-data.schema.json.

Stdlib-only. Implements the subset of JSON Schema draft-07 that the schema uses
(type, required, enum, minimum/maximum, minItems/maxItems, items, properties),
so there is no third-party dependency.

Usage:
    python3 validate_audit.py path/to/audit-data.json [--schema path/to/schema.json]

Exit code 0 = valid, 1 = invalid, 2 = usage/IO error.
"""
import argparse
import json
import os
import sys

TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "null": type(None),
}


def _type_ok(value, type_name):
    py = TYPE_MAP[type_name]
    if type_name == "integer":
        # bool is a subclass of int in Python; reject it for integer fields.
        return isinstance(value, int) and not isinstance(value, bool)
    if type_name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if type_name == "boolean":
        return isinstance(value, bool)
    return isinstance(value, py)


def validate(node, schema, path, errors):
    # type (may be a string or a list of allowed types)
    t = schema.get("type")
    if t is not None:
        types = t if isinstance(t, list) else [t]
        if not any(_type_ok(node, tn) for tn in types):
            errors.append(f"{path or '<root>'}: expected type {types}, got {type(node).__name__}")
            return  # further checks assume the type matched

    if "enum" in schema and node not in schema["enum"]:
        errors.append(f"{path}: value {node!r} not in enum {schema['enum']}")

    if isinstance(node, (int, float)) and not isinstance(node, bool):
        if "minimum" in schema and node < schema["minimum"]:
            errors.append(f"{path}: {node} < minimum {schema['minimum']}")
        if "maximum" in schema and node > schema["maximum"]:
            errors.append(f"{path}: {node} > maximum {schema['maximum']}")

    if isinstance(node, list):
        if "minItems" in schema and len(node) < schema["minItems"]:
            errors.append(f"{path}: {len(node)} items < minItems {schema['minItems']}")
        if "maxItems" in schema and len(node) > schema["maxItems"]:
            errors.append(f"{path}: {len(node)} items > maxItems {schema['maxItems']}")
        item_schema = schema.get("items")
        if item_schema:
            for i, item in enumerate(node):
                validate(item, item_schema, f"{path}[{i}]", errors)

    if isinstance(node, dict):
        for req in schema.get("required", []):
            if req not in node:
                errors.append(f"{path or '<root>'}: missing required field '{req}'")
        props = schema.get("properties", {})
        for key, subschema in props.items():
            if key in node:
                child_path = f"{path}.{key}" if path else key
                validate(node[key], subschema, child_path, errors)


def main():
    ap = argparse.ArgumentParser(description="Validate GTM audit-data JSON.")
    ap.add_argument("data", help="Path to audit-data.json")
    ap.add_argument(
        "--schema",
        default=os.path.join(os.path.dirname(__file__), "..", "templates", "audit-data.schema.json"),
        help="Path to the JSON schema (defaults to the bundled schema).",
    )
    args = ap.parse_args()

    try:
        with open(args.data, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR reading data: {e}", file=sys.stderr)
        return 2
    try:
        with open(args.schema, encoding="utf-8") as f:
            schema = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR reading schema: {e}", file=sys.stderr)
        return 2

    errors = []
    validate(data, schema, "", errors)

    # Cross-field sanity checks beyond plain schema.
    dims = data.get("dimensions", []) if isinstance(data, dict) else []
    if dims and len(dims) < 11:
        errors.append(f"dimensions: expected the 12 rubric dimensions, found {len(dims)}")

    if errors:
        print(f"INVALID — {len(errors)} problem(s):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"VALID — {os.path.basename(args.data)} conforms to the audit schema.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
