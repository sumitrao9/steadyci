# GitHub Actions supply chain security checklist

## The problem
CI pipelines execute third-party code with repo credentials. Unpinned, unverified, or abandoned actions expand your attack surface.

## The fix
Pin by SHA, restrict permissions, audit untrusted triggers, remove abandoned actions, and monitor with SteadyCI.

## Check your repo
Run `steadyci scan .github/workflows` to check your repo.

---
*SteadyCI is an open-source GitHub Actions health scanner. MIT licensed.*
