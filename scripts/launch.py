#!/usr/bin/env python3
"""Start one explicitly named agent in a new Herdr tab; do not send a task."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def herdr(*args):
    result = subprocess.run(["herdr", *args], text=True, capture_output=True)
    if result.returncode:
        # Do not echo arbitrary terminal output or environment values.
        raise RuntimeError(f"Herdr command failed: {' '.join(args[:2])}; inspect Herdr locally")
    return json.loads(result.stdout)["result"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("role", choices=["lead", "implementation-lead", "builder", "reviewer"])
    parser.add_argument("--workspace", required=True, type=Path)
    parser.add_argument("--model", required=True)
    parser.add_argument("--effort", choices=["low", "medium", "high", "xhigh", "max"])
    parser.add_argument("--name", help="required, unique assignment name for a worker")
    parser.add_argument("--cwd", type=Path, help="existing project worktree or review checkout")
    parser.add_argument("--brief", type=Path, help="existing assignment brief for a worker")
    parser.add_argument("--bypass", action="store_true", help="disable CLI approval/sandbox checks")
    args = parser.parse_args()
    if os.environ.get("HERDR_ENV") != "1":
        parser.error("run this from a shell inside the intended Herdr session")
    worker = args.role in ("builder", "reviewer")
    kind = "codex" if args.role in ("lead", "reviewer") else "claude"
    for binary in ("herdr", kind):
        if not shutil.which(binary):
            parser.error(f"missing executable: {binary}")
    workspace = args.workspace.expanduser().resolve()
    contract = workspace / "roles" / f"{args.role}.md"
    if not contract.is_file() or not (workspace / "POLICY.md").is_file():
        parser.error("workspace is missing role instructions; run init.py first")
    if worker and not (args.name and args.cwd and args.brief):
        parser.error("workers require --name, --cwd and --brief")
    if not worker and (args.cwd or args.brief):
        parser.error("--cwd and --brief apply to workers; leads use their workspace directory")
    name = args.name or args.role
    if not re.fullmatch(r"[a-z][a-z0-9_-]{0,31}", name):
        parser.error("name must be 1-32 lowercase letters, digits, underscores or hyphens")
    cwd = args.cwd.expanduser().resolve() if worker else workspace / (
        "lead-agent" if args.role == "lead" else "implementation-lead")
    if not cwd.is_dir():
        parser.error("working directory does not exist")
    brief = args.brief.expanduser().resolve() if worker else None
    if brief and not brief.is_file():
        parser.error("brief does not exist")
    if args.effort and kind == "claude" and args.effort == "xhigh":
        parser.error("Claude uses max rather than xhigh; check your model's supported effort")
    if args.effort and kind == "codex" and args.effort == "max":
        parser.error("Codex uses xhigh rather than max; check your model's supported effort")

    # Check names before creating any pane. Existing agents are never replaced.
    if any(a.get("name") == name for a in herdr("agent", "list")["agents"]):
        parser.error(f"an agent named {name} already exists; inspect or resume it")
    cli_args = ["--model", args.model, "--add-dir", str(workspace)]
    if args.effort:
        cli_args += (["-c", f'model_reasoning_effort="{args.effort}"']
                     if kind == "codex" else ["--effort", args.effort])
    if args.bypass:
        cli_args += (["--dangerously-bypass-approvals-and-sandbox"]
                     if kind == "codex" else ["--permission-mode", "bypassPermissions"])
    if worker:
        prompt = (f"You are explicitly assigned as {args.role}. Read {contract}, "
                  f"{workspace / 'PLAYBOOK.md'}, {workspace / 'POLICY.md'}, "
                  f"then {brief}. Follow the brief and repository instructions. "
                  "Your immediate parent and report path are specified in the brief. "
                  "Do not discover another lead or expand the assignment.")
    else:
        prompt = (f"Read {contract}, {workspace / 'PLAYBOOK.md'}, "
                  f"{workspace / 'POLICY.md'} and the vault startup notes named there. "
                  "Do not start project work until the person or your assigned parent "
                  "gives you an explicit task. Confirm readiness briefly.")
    # The agent is started with a native positional prompt, not terminal keystrokes.
    # Paths and prompts remain individual argv entries; no shell interpolation.
    tab = herdr("tab", "create", "--cwd", str(cwd), "--label", name, "--no-focus")
    pane = tab["root_pane"]["pane_id"]
    print(f"Created {name} tab; pane {pane}", flush=True)
    try:
        herdr("agent", "start", name, "--kind", kind, "--pane", pane,
              "--", *cli_args, prompt)
    except (RuntimeError, KeyError, ValueError):
        print(f"Startup did not confirm ready. Inspect pane {pane}; it was preserved. "
              "Do not rerun blindly or discard any sign-in/trust prompt.", file=sys.stderr)
        return 1
    print(f"Started {name}. Open its tab. Inspect with: herdr agent get {name}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (RuntimeError, KeyError, ValueError) as error:
        print(f"Launch failed ({type(error).__name__}); inspect the local CLI and session.",
              file=sys.stderr)
        sys.exit(1)
