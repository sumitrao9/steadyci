# Fix deprecated GitHub Actions runners (ubuntu-20.04)

## The problem
Deprecated runners (ubuntu-20.04, macOS-11/12) are removed on a schedule and cause CI to fail without warning.

## The fix
Migrate to supported runners like `ubuntu-24.04` or `ubuntu-latest` and test your workflow.

## Check your repo
Run `steadyci scan .github/workflows` to check your repo.

---
*SteadyCI is an open-source GitHub Actions health scanner. MIT licensed.*
