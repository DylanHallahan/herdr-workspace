#!/usr/bin/env python3
"""Create a private working directory from the bundled, generic templates."""
import argparse
import shutil
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    destination = args.destination.expanduser().absolute()
    source = Path(__file__).resolve().parent.parent / "workspace-template"
    if destination.exists() or destination.is_symlink():
        parser.error("destination already exists; choose a new directory (nothing overwritten)")
    # Reject nesting inside the template, which would recursively copy itself.
    if source == destination.resolve() or source in destination.resolve().parents:
        parser.error("destination must be outside workspace-template")
    shutil.copytree(source, destination)
    for name in ("projects", "briefs", "reports"):
        (destination / "vault" / name).mkdir(exist_ok=True)
    print(f"Created workspace: {destination}")
    print(f"Review {destination / 'POLICY.md'} before assigning work.")
    print("No accounts, global configuration or running sessions were changed.")


if __name__ == "__main__":
    main()
