"""
Contains commands like:
- run
- validate
- list
- init
"""

from __future__ import annotations

import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from app.runner import run_workflow
from app.workflow import (
    WORKFLOW_DIR,
    discover_workflows,
    load_workflow,
    validate_workflow,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.FileHandler(Path("logs/browser-bot.log")),
        logging.StreamHandler(sys.stdout),
    ],
)


def _cmd_run(workflow_path: Path | None, head: bool = False) -> int:
    """Load, validate, and run a workflow."""
    if workflow_path is None:
        workflows = discover_workflows()
        if not workflows:
            print("No workflow files found in workflow/")
            return 1
        # If there's exactly one, use it. Otherwise ask.
        if len(workflows) == 1:
            workflow_path = workflows[0]
        else:
            print("Multiple workflows found. Pick one with --file <path>:")
            for wf in workflows:
                print(f"  {wf}")
            return 1

    data = load_workflow(workflow_path)
    errors = validate_workflow(data)
    if errors:
        print(f"Validation errors in {workflow_path}:")
        for err in errors:
            print(f"  ✗ {err}")
        return 1

    run_workflow(data, head)
    return 0


def _cmd_validate(workflow_path: Path) -> int:
    """Validate a workflow file and print results."""
    data = load_workflow(workflow_path)
    errors = validate_workflow(data)
    if errors:
        print(f"✗ {workflow_path}:")
        for err in errors:
            print(f"  {err}")
        return 1
    print(f"✓ {workflow_path} is valid")
    return 0


def _cmd_list() -> int:
    """Print all discovered workflows."""
    workflows = discover_workflows()
    if not workflows:
        print("No workflows found in workflow/")
        return 0
    for wf in workflows:
        print(f"  {wf}")
    return 0


def _cmd_init(name: str) -> int:
    """Generate a new workflow YAML from the example template."""
    dest = WORKFLOW_DIR / f"{name}.yaml"
    if dest.exists():
        print(f"Already exists: {dest}")
        return 1
    template = WORKFLOW_DIR / "example.yaml"
    if not template.exists():
        print("Missing workflow/example.yaml template")
        return 1
    dest.write_text(template.read_text())
    print(f"Created {dest} — edit it to build your workflow")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description="Run YAML browser workflows")
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run a workflow. workflow/ directory is scanned for yaml files.",
    )
    parser.add_argument(
        "--validate", action="store_true", help="Validate a workflow yaml file."
    )
    parser.add_argument(
        "--list", action="store_true", help="List all available workflow yaml files."
    )
    parser.add_argument(
        "--head", action="store_true", help="Run Playwright with a head."
    )
    parser.add_argument(
        "--init",
        type=str,
        metavar="NAME",
        help="Generate a new workflow yaml file with example steps.",
    )
    parser.add_argument(
        "--file",
        "-f",
        type=Path,
        default=None,
        help="Path to a specific workflow yaml file.",
    )
    args = parser.parse_args(argv)

    if args.list:
        return _cmd_list()
    if args.init:
        return _cmd_init(args.init)
    if args.validate:
        if args.file is None:
            print("--validate requires --file <path>")
            return 1
        return _cmd_validate(args.file)
    if args.run:
        if args.file is None:
            print("--run requires --file <path>")
            return 1
        return _cmd_run(args.file, args.head)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
