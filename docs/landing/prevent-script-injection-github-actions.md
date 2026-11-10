# Prevent script injection in GitHub Actions

## The problem
Interpolating untrusted event data (PR titles, issue bodies) into `run:` via `${{ }}` lets attackers inject shell commands.

## The fix
Pass untrusted values through `env:` and reference them as quoted shell variables (`"$VAR"`).

## Check your repo
Run `steadyci scan .github/workflows` to check your repo.

---
*SteadyCI is an open-source GitHub Actions health scanner. MIT licensed.*
