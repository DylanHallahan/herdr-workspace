# Human-owned workspace policy

These are starter defaults. The current user's instructions and repository
requirements take precedence. A directory, role file or past report does not
grant authority over a project.

- Scope: only explicitly assigned repositories and environments.
- Default delivery: local changes, existing checks and a reviewable result.
  Record push, PR, merge, deployment and environment authority in each brief.
  A phase handoff does not require a new approval for an already authorized step.
- Production actions require explicit authorization. DEV access is not PROD access.
- Published schema additions or changes to units, grain and financial meaning
  require approval of a concrete proposal before implementation.
- Workers never merge or tag, never delegate, and push only when their brief
  explicitly permits it. The implementation lead executes authorized merges.
- Use the repository's required checks. Do not add recurring gates or a new
  test framework merely to capture a one-time investigation. Any workspace-wide
  rule on new tests should be decided by the person, not invented by an agent.
- No messages to people, collaborator invitations or external publication
  beyond the user's explicit task. Do not print credentials.
- One writer per shared checkout or other mutable resource. Independent work
  can run in isolated worktrees; shared builds and deployments are serialized.
- Keep normal CLI permissions unless the person explicitly selects bypass.

Before the first real assignment, record any project-specific exceptions in its
project note. Keep credentials in the tools' own authentication stores.
