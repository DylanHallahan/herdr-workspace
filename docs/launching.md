# Launching and recovery

Run these commands in a **shell pane inside the intended Herdr session**. The
helper refuses to control a session when `HERDR_ENV` is not `1`. It creates one
new tab per agent and preserves the user's focus. It refuses duplicate agent
names and never replaces or stops an existing agent.

## Leads

```bash
python3 scripts/launch.py lead --workspace "$HOME/agent-workspace" \
  --model YOUR_CODEX_MODEL --effort high

python3 scripts/launch.py implementation-lead --workspace "$HOME/agent-workspace" \
  --model YOUR_CLAUDE_MODEL --effort high
```

The initial prompt loads the role and waits for an assignment. It does not
dispatch project work or create an autonomous team by itself. Workspace access
is supplied with `--add-dir` so an agent can maintain its local notes. Project
repositories and worker checkouts are provided explicitly through the brief.

This uses the CLI settings and signed-in account already on that machine.
The kit never writes global approval policies, authentication or model defaults.
If an existing global policy enables bypass, omitting `--bypass` does not reset
that global policy; inspect your CLI settings when choosing permissions.

## Workers

Prepare the brief and a fresh builder worktree first. These paths must exist:

```bash
python3 scripts/launch.py builder --workspace "$HOME/agent-workspace" \
  --name export-build --model YOUR_CLAUDE_MODEL --effort high \
  --cwd /path/to/project-export-worktree \
  --brief "$HOME/agent-workspace/vault/briefs/export-build.md"

python3 scripts/launch.py reviewer --workspace "$HOME/agent-workspace" \
  --name export-review --model YOUR_CODEX_REVIEW_MODEL --effort high \
  --cwd /path/to/project-export-worktree \
  --brief "$HOME/agent-workspace/vault/briefs/export-review.md"
```

Pause the builder's edits while the reviewer reads the same worktree, or use a
separate clean review checkout at the exact reviewed revision. Never run a
review against files the builder is changing underneath it. Reviewers do not
need a new worktree when a clean, stable checkout is available.

The worker receives the explicit role and brief as its initial prompt. It still
reads the target repository's own instructions. The launcher does not change
that repository's AGENTS.md or CLAUDE.md.

Choose models explicitly based on availability in your account. Keep the model
that built a change for its fixes; use a fresh session from the other family for
independent review. The source setup uses a Claude implementation lead and
builder with Codex review, but it does not require a particular subscription tier.

## Permissions

Add `--bypass` to a launch command only when you intend to disable technical
approval checks in that environment. The exact native arguments are:

```text
Codex:      --dangerously-bypass-approvals-and-sandbox
Claude:     --permission-mode bypassPermissions
```

The helper applies those flags only to the new process. It does not edit global
configuration. Bypass grants broad machine access; use an environment you intend
the agent to control. Written role boundaries still apply, but are not a sandbox.

## Layout

The original layout is two leads side by side, workers grouped in another tab,
and retained paused work kept separately. The helper starts separate tabs so it
can work without assuming a screen size or touching existing panes. To recreate
the combined layout, inspect the current IDs and use Herdr's move command:

```bash
herdr agent list
herdr tab list
herdr pane move MAIN_PANE --tab IMPLEMENTATION_TAB \
  --target-pane IMPLEMENTATION_PANE --split right --no-focus
herdr tab rename IMPLEMENTATION_TAB Leads
```

Replace every uppercase identifier with the actual returned ID. Merge worker
tabs using the same command when useful. Pane moves may change pane IDs; verify
the agent name and session afterward. Do not move, resize or close another
person's session. Layout does not grant authority or change the parent.

## Startup problems

- Missing command: install that tool and make sure it is on PATH in the Herdr
  shell, not only in another terminal.
- Sign-in or trust prompt: open the created pane and complete it. Do not rerun
  the launcher to create another copy. Herdr integration and hooks may require
  their own approval; follow `herdr integration` and the official docs.
- Unsupported model or effort: select a model offered by that account and check
  `codex --help` or `claude --help`. The helper does not silently substitute one.
- Duplicate name: inspect `herdr agent get <name>` and resume the existing
  assignment or choose an actually distinct assignment name.
- Startup timeout: the helper leaves the pane intact and prints its ID. Inspect
  it before deciding whether to resume, retry or close it.
- Missing queue command: use the handoff alternatives in [workflow.md](workflow.md).

## Reconnect

On the same machine, run `herdr --session agents` again to attach to that session.
Inspect the agents and active work before launching anything new. For a server
setup, SSH to your own host and attach there. Remote-machine setup is separate
from distributing this kit; follow [Herdr's documentation](https://herdr.dev/docs).
