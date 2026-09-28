# Running the workflow

## First assignment

Give the main agent an outcome, a local project path and the actions you allow.
For example:

> In my checkout at `/path/to/project`, fix the CSV export so it preserves
> quoted line breaks. Prepare a reviewed draft PR into dev. You may push the
> feature branch and open the PR. Do not merge, deploy or contact anyone.
> Use the implementation lead for execution and a fresh reviewer.

The main agent records that assignment in a project note and gives the
implementation lead a self-contained brief. The implementation lead owns
execution through the draft PR. It does not need to ask again to push, since
that action was explicitly authorized. Changing the production export schema
would be a new decision, not an ordinary implementation choice.

The example is a template, not an instruction to act on any repository.

## Builder and reviewer

Use `git worktree add -b <branch> <new-path> <base>` in the project repository
to create the builder's isolated checkout. Fetch the intended base first.
Write the brief with exact paths, source revision, permitted writes, parent and
report destination. Then launch the builder as described in [launching.md](launching.md).

Do not give a reviewer the coding conversation. Give it intent, accepted
decisions, the source/diff, important invariants, real data access boundaries,
and an output path. For a changed source, schema or served behavior, review the
plan before implementation. Review the resulting code independently afterward.
The implementation lead checks and triages findings; it does not blindly obey
the reviewer or repeat every step of its investigation.

Read-only means no source-code or external-data mutations; explicitly allow
writing the findings file. A sandbox that also blocks the report can prevent
the reviewer from completing its assignment.

## Handoffs that actually reach the parent

Use `herdr agent list` and `herdr agent get <name>` to verify the immediate
parent and record its identity in the brief. The implementation lead is usually
the worker's parent; the main agent is the implementation lead's parent.

For a Claude parent:

```bash
herdr agent prompt implementation-lead \
  '[WORKER export-build] local build complete - report: /absolute/report/path.md'
```

For a Codex parent, some CLI versions provide a queue command:

```bash
codex queue --help
codex queue --thread VERIFIED_SESSION_UUID \
  --message '[IMPLEMENTATION] outcome complete - report: /absolute/report/path.md'
```

Use that route only when the installed CLI supports it, and retain its queued
message ID. The UUID comes from the current parent's `agent_session`, not a
copied example. If queue is unavailable, wait for the Codex parent to be idle
before `herdr agent prompt <verified-name> ...`; input sent to a working Codex
session is not a reliable delivery mechanism. If the parent cannot be reached,
record a pending handoff for the human rather than notifying another agent.
The kit does not install an unattended queue fallback or a polling daemon.

A toast is not message delivery. A report written to disk is not message
delivery. The recipient must receive the handoff through a supported route.

## What a useful status looks like

> The export fix is in draft PR 12 and existing checks pass. The independent
> review found one edge case; the builder is fixing it in the same worktree.
> Production is unchanged. Report: [path].

The full report contains evidence. A status message is not a dump of agent IDs,
query logs, costs and every phase transition. Report verified outcomes, material
scope changes, decisions and external blockers. Keep routine waits internal.

## Finishing and recovery

Keep the builder and worktree until review and corrections are accepted. Verify
commits, uncommitted edits and reports before closing a pane or deleting a
worktree. A user pause preserves work; it does not grant cleanup authority.

After a dropped connection, inspect existing agents and reports before starting
another session. When a process really crashed, recover its session using the
installed CLI's resume command and its verified session ID. Reconcile active
builds first, so recovery cannot duplicate a deployment.

Scheduled check-ins are optional and require a separate instruction. This kit
installs none. If you later add one, give it an expiry, a single owner, a precise
scope and a removal condition. Worker events remain the normal trigger.
