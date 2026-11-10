# Pin GitHub Actions to a commit SHA

## The problem
Tags like `@v4` can be moved by a maintainer. The tj-actions/Trivy incident (Mar 2026) showed how a compromised tag can run attacker code in your CI.

## The fix
Replace `uses: owner/repo@v4` with `uses: owner/repo@<full-commit-sha>` and keep the version as a comment. Update via Dependabot/Renovate.

## Check your repo
Run `steadyci scan .github/workflows` to check your repo.

---
*SteadyCI is an open-source GitHub Actions health scanner. MIT licensed.*
