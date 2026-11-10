# SteadyCI

**Security, cost, and maintenance health for GitHub Actions workflows.** Local-first scanner + SARIF + shareable reports, with a compounding action-reputation registry (opt-in).

> Evidence (2026): GitHub Actions ran 11.5B minutes in 2025 (+35% YoY). Kaspersky found 250k+ workflow misconfigurations in ~30k starred repos. Legit: only 913/19,113 marketplace actions verified (avg OpenSSF Scorecard 4.23/10). lastseen.dev: 80.7% of actions unmaintained overall (head much lower). Supply-chain incidents: tj-actions/Trivy (Mar 2026), Shai-Hulud (May 2026). *Numbers are sourced estimates/snapshots; see `docs/RESEARCH.md`.*

## Checks (rule IDs)
- **SEC010** Unpinned `uses:` (not a commit SHA) — supply chain
- **SEC001/002/003** Missing/broad permissions, workflow-level secrets
- **SEC004/005** `pull_request_target` risk / checkout of untrusted PR head
- **SEC011/012** Script injection in `run:` / `curl|sh`
- **REL001** Deprecated runners (e.g., `ubuntu-20.04`)
- **MAINT001** Deprecated action majors
- **COST001** Matrix blowup heuristic

## Quick start
```bash
pip install steady-ci
steadyci scan .                         # text
steadyci scan . --format sarif --fail-on warn > steadyci.sarif
steadyci scan . --format markdown > report.md
steadyci report . --out report.md
steadyci scan . --write-baseline steadyci-baseline.json
steadyci metrics                        # local, opt-in (STEADYCI_TELEMETRY=0 to disable)
```

## GitHub Action (SARIF + code scanning)
```yaml
- uses: sumitrao9/steadyci@v0
  with:
    path: .
    fail-on: error
```
See `action.yml`. (Pin by SHA in production.)

## Config (`steadyci.toml` or `[tool.steadyci]` in `pyproject.toml`)
```toml
[steadyci]
fail_on = "error"            # error|warn|none
ignore_rules = ["COST001"]
ignore_paths = ["vendor/"]
baseline_file = "steadyci-baseline.json"
```

## Reputation registry (opt-in, read-only)
```bash
export GITHUB_TOKEN=...   # optional, rate limits apply
steadyci refresh-registry actions/checkout actions/setup-python
```
Builds a local SQLite reputation graph (`~/.steadyci/registry.db`). Network calls happen only when explicitly invoked.

## Growth & network effects (product strategy)
- **Distribution:** free scanner + shareable report/badge + SEO problem pages (`docs/index.md`).
- **Compounding moat:** reputation graph improves with scans/refresh (data flywheel).
- **Revenue (after signal):** Pro dashboard/PR bot/alerts → Team policy/SSO/API → Enterprise. No billing before demand validation.

## Dev
```bash
make check   # ruff + unittest + smoke
```

## Docs
- `docs/CHARTER.md`, `docs/RESEARCH.md`, `docs/ARCHITECTURE.md`, `docs/BUSINESS_MODEL.md`, `docs/GROWTH.md`, `docs/VALIDATION.md`
- Rules: `docs/rules/*.md` | Landing: `docs/landing/*.md`

## License
MIT (scanner). © Sumit Rao. Authorized/ethical use only. No fake metrics. No publish/deploy/spend without explicit approval.
