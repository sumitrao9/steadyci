# SteadyCI — Business Model

## Who pays
- **Platform/DevSecOps teams** (B2B): need policy, audit, SSO, and fleet-wide visibility across many repos.
- **Security-conscious startups/SMBs:** want "safe CI" without a dedicated security team.
- **Individual maintainers/OSS:** free tier drives adoption and data; convert via hosted convenience.

## Offers
| Tier | Price anchor (estimate, validate) | Includes |
|---|---|---|
| Free | $0 | Local CLI scan, public report, basic rules, opt-in telemetry |
| Pro | $9–$29/repo/mo or $49–$199/team/mo | Dashboard, history, alerts, PR bot, fix suggestions |
| Enterprise | $500+/mo custom | SSO/SAML, audit logs, policy-as-code, private registry, API, SLA, support |
| API | usage-based | Reputation-graph lookups for platforms/marketplaces |

*Anchors are estimates; validate with 10 pilot customers before publishing pricing.*

## Unit economics (hypothesis)
- **COGS:** mostly compute for scheduled scans/API + storage for reputation graph. Low per-scan cost (YAML parse + cached metadata). Target gross margin >80% at scale.
- **CAC:** primarily organic (OSS, SEO, GitHub). Paid acquisition only after activation/retention proven.
- **LTV:** driven by retention (CI is sticky once integrated). Track repo-level churn.

## Sequencing
1. **Now:** free scanner + report + data collection (no billing).
2. **Signal:** 100+ weekly active repos or 10+ inbound "dashboard/team" requests.
3. **Monetize:** Pro dashboard + PR bot (self-serve). Enterprise later.
