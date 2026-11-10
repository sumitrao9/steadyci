# SteadyCI — Architecture (MVP)

```
steadyci/
  scanner/   # pure analysis: model + rules + engine (no network)
  registry/  # SQLite reputation graph (local-first; refreshable from GitHub API)
  dashboard/ # growth metrics (local opt-in events → summary/export)
  landing/   # problem-first SEO pages (static)
  cli.py     # `steadyci scan <path> [--format json]`
```

## Data flow
1. **Scan:** `engine.scan_path()` discovers `.github/workflows/*.yml` → parses → runs rules → returns findings + score.
2. **Reputation (optional):** rules can consult `registry.store` for action metadata (archived/last-commit/CVE flags). Refresh is a separate, rate-limited job.
3. **Metrics (opt-in):** CLI emits local events (`scan_completed`, counts, score hash). Exportable JSON; no external telemetry by default (`STEADYCI_TELEMETRY=0`).

## Design choices
- **Local-first, zero mandatory network:** builds trust and keeps opex near zero.
- **Rules are deterministic and testable:** each rule has an ID, severity, category, and remediation.
- **Compounding asset is the registry:** not the scanner. Scanner is distribution; registry is defensibility.
- **Open core:** scanner MIT; hosted registry/SaaS proprietary later.

## Next increments
- GitHub Action wrapper + PR annotation output (SARIF).
- Remote scan mode (GitHub API, read-only token).
- Reputation refresh worker (GitHub REST/GraphQL, rate-limit aware).
- Static dashboard site generated from metrics export.
