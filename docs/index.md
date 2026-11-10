# SteadyCI

Open-core GitHub Actions health: **security + maintenance + cost**.

- [Pin GitHub Actions to a commit SHA](landing/pin-github-actions-to-sha.md)
- [Least-privilege permissions](landing/github-actions-least-privilege-permissions.md)
- [Fix deprecated runners](landing/fix-deprecated-ubuntu-runner.md)
- [Prevent script injection](landing/prevent-script-injection-github-actions.md)
- [Supply chain checklist](landing/github-actions-supply-chain-security.md)

## Quick start
```bash
pip install steady-ci
steadyci scan .
steadyci scan . --format sarif --fail-on warn > steadyci.sarif
```
