"""
Contains logic for loading and validating YAML workflow files.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


# ── Schema Constants ────────────────────────────────────────────────
WORKFLOW_DIR = Path("workflow")

VALID_ACTIONS = {"goto", "click", "fill", "select", "wait_for", "screenshot", "download", "notify"}

# Fields that are required per-action.  Everything else is optional.
REQUIRED_FIELDS: dict[str, set[str]] = {
    "goto":       {"url"},
    "click":      {"selector"},
    "fill":       {"selector"},              # must also have value OR value_from_env
    "wait_for":   {"selector"},
    "screenshot": {"path"},
    "download":   set(),
    "select":     {"selector", "value"},
    "notify":     {"message"},
}


# ── Public helpers ──────────────────────────────────────────────────

def discover_workflows() -> list[Path]:
    """Return a sorted list of .yaml / .yml files in WORKFLOW_DIR."""
    if not WORKFLOW_DIR.is_dir():
        return []
    return sorted(
        p for p in WORKFLOW_DIR.iterdir()
        if p.suffix in (".yaml", ".yml") and p.name != "example.yaml"
    )


def load_workflow(path: Path) -> dict[str, Any]:
    """
    Read a YAML workflow file and return its parsed dict.

    Raises FileNotFoundError or yaml.YAMLError on problems.
    """
    with open(path) as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: top-level value must be a mapping, got {type(data).__name__}")
    return data


def validate_workflow(data: dict[str, Any]) -> list[str]:
    """
    Check a parsed workflow dict for structural errors.

    Returns a list of human-readable error strings (empty == valid).
    """
    errors: list[str] = []

    # Top-level keys
    if "name" not in data:
        errors.append("Missing required key: 'name'")
    if "steps" not in data:
        errors.append("Missing required key: 'steps'")
        return errors  # can't check steps if missing

    steps = data["steps"]
    if not isinstance(steps, list) or len(steps) == 0:
        errors.append("'steps' must be a non-empty list")
        return errors

    for i, step in enumerate(steps, start=1):
        prefix = f"Step {i}"
        if not isinstance(step, dict):
            errors.append(f"{prefix}: must be a mapping")
            continue

        action = step.get("action")
        if action is None:
            errors.append(f"{prefix}: missing 'action' key")
            continue
        if action not in VALID_ACTIONS:
            errors.append(f"{prefix}: unknown action '{action}'")
            continue

        for field in REQUIRED_FIELDS[action]:
            if field not in step:
                errors.append(f"{prefix} ({action}): missing required field '{field}'")

        # fill needs either value or value_from_env
        if action == "fill":
            if "value" not in step and "value_from_env" not in step:
                errors.append(f"{prefix} (fill): must have 'value' or 'value_from_env'")

    return errors


def resolve_env_values(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    For any step that has 'value_from_env', resolve the environment variable
    into a concrete 'value' field.  Returns a *new* list (original is not mutated).

    Raises KeyError if the env var is not set.
    """
    resolved: list[dict[str, Any]] = []
    for step in steps:
        step = dict(step)  # shallow copy
        env_key = step.pop("value_from_env", None)
        if env_key is not None:
            val = os.environ.get(env_key)
            if val is None:
                raise KeyError(f"Environment variable '{env_key}' is not set")
            step["value"] = val
        resolved.append(step)
    return resolved