"""
Contains commands like:
- run
- validate
- list
- init
"""

from argparse import ArgumentParser

def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(
        description=""
    )
    parser.add_argument(
        "--run",
        action="",
        help="Run a workflow. workflow/ directory is scanned for yaml files."
    )
    parser.add_argument(
        "--validate",
        action="",
        help="Validate a workflow yaml file."
    )
    parser.add_argument(
        "--list",
        action="",
        help="List all available workflow yaml files."
    )
    parser.add_argument(
        "--init",
        action="",
        help="Generate a new workflow yaml file with example steps."
    )
    args = parser.parse_args(argv)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())