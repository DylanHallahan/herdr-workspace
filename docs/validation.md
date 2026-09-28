# Validation

Prepared on Linux against Herdr 0.9.1 on 2026-09-22. Launch flags were checked
against the installed `herdr`, `codex` and `claude` help. External installation
guides are linked rather than copying installers or installing dependencies.

Local validation covers Python syntax, initialization into a fresh temporary
directory, refusing to overwrite an existing workspace, and launch argument
construction with a stub CLI. It includes paths containing spaces, duplicate
agent names, missing worker arguments, permission mode selection and preserving
a pane when startup fails.

No model sessions are launched as part of that validation. Live model startup,
authentication and remote access on the recipient's machine remain unverified.
The helper does not inspect or copy credentials. A successful script check is
not a claim that all CLI versions or operating systems are supported.

Before publishing, tracked files are checked for accidental machine-specific
paths, account tokens, session IDs and private project details. The workspace
templates are written from reusable workflow rules rather than copied from a
live vault. Shared docs intentionally name the GitHub repository needed to clone
the kit; that is not a credential.

## Consolidation into herdr-workspace — September 28, 2026

The scripts and workspace templates were imported unchanged from starter revision
`fe5720c34d219833cd7e0a91ba3715cfa19b0fd5`. Ten local checks passed: Python syntax,
fresh initialization into a path containing spaces, refusal to overwrite an
existing workspace, both lead launch commands, worker assignment and explicit
bypass arguments, incomplete worker rejection, rejection outside Herdr, duplicate
name rejection, pane preservation on startup failure, and local documentation
links. The generated workspace was also checked to exclude the personal snapshot.

Launch verification used a stub Herdr executable and did not start model sessions.
RainCLI onboarding is linked separately; the initializer does not provision it.
