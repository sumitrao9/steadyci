# Security Policy

## Reporting
Report security issues privately to the maintainer via GitHub Security Advisories for this repository. Do not open public issues for exploitable vulnerabilities.

## Scope
- SteadyCI scanner/CLI and published packages.
- Findings about *other* GitHub Actions should be reported to their maintainers/upstreams, not as SteadyCI vulnerabilities.

## Supported versions
Only the latest release is supported.

## Principles
- Local-first by default; telemetry is opt-in/disableable (`STEADYCI_TELEMETRY=0`).
- No secrets collection. Do not include tokens or private repo data in reports.
- Evidence-labeled claims; no fake metrics.
