# GitHub Actions permissions: least privilege

## The problem
Without explicit `permissions:`, workflows may inherit broad token access. 250k+ misconfigurations were found in starred repos (Kaspersky, Jun 2026).

## The fix
Set top-level `permissions: contents: read` (or `{}`) and grant only what each job needs.

## Check your repo
Run `steadyci scan .github/workflows` to check your repo.

---
*SteadyCI is an open-source GitHub Actions health scanner. MIT licensed.*
