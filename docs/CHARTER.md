# SteadyCI — Product Charter

**One-line:** Security, cost, and maintenance health for GitHub Actions — the compounding reputation graph for the CI layer.

## The problem (verified)
- 11.5B GitHub Actions minutes in 2025 (+35% YoY). 30k+ marketplace actions.
- 250k+ security misconfigurations found in ~30k starred repos (Kaspersky GReAT, Jun 2026).
- Only 913/19,113 Actions verified; avg OpenSSF Scorecard 4.23/10 (Legit).
- 80.7% of all Actions unmaintained; 762 archived (lastseen.dev, Aug 2026).
- Supply-chain incidents: tj-actions/Trivy (Mar 2026), Shai-Hulud npm worm hit 170+ packages (May 2026).

**Gap:** The official registry verifies namespace ownership, not runtime safety, maintenance, or cost. There is no authoritative, compounding reputation graph for Actions.

## Product
- **Open-source scanner (MIT):** parses `.github/workflows`, flags pinning, permissions, injection, deprecated runners, cost blowup, and known-bad patterns. Runs locally, in CI, or as a bot.
- **Reputation registry (data asset):** per-action metadata (archived, last commit/release, CVE correlation, verified, adoption signals). Updated as repos scan. This is the moat.
- **SaaS dashboard:** trends, alerts, policy, team rollups, API.

## Growth engine
1. **Organic:** free CLI + GitHub Action; shareable "Actions Health Report"; SEO landing pages for "GitHub Actions security", "pin actions to SHA", "deprecated ubuntu-20.04", "actions supply chain".
2. **Distribution loops:** scanner outputs a badge/link; "fix PR" bot invites repo maintainers; public registry pages rank for action names.
3. **Network effect (real):** more scans → more accurate reputation graph → better answers for everyone. Not vanity growth.
4. **Ecosystem:** open rules format, community rule packs, integrations (Dependabot, Renovate, OpenSSF Scorecard).

## Revenue (sequenced)
- **Free:** local scan, public report.
- **Pro ($/repo/mo):** dashboard, history, alerts, Slack/PR bot.
- **Team/Enterprise:** SSO, audit logs, policy-as-code, private registry, API, SLA.
- **Usage/API:** reputation-graph API for platforms.

## Founder opportunity engine
- Open-source core with transparent benchmarks and incident writeups.
- Publish the "State of GitHub Actions Health" report (data-backed).
- Conference talks (supply chain, DevSecOps), OSS contributions.

## Growth intelligence (track)
New/active/returning users, scans, repos onboarded, organic/referral, activation (first fix), retention (repeat scan), paid conversions, MRR, infra cost, LTV. Recommend next highest-impact improvement weekly from data.

## Selection fit (1-8)
1. Organic distribution: high (CI is universal). 2. Recurring revenue: high. 3. Network effects: high (reputation data). 4. Dev ecosystem: high. 5. Low opex: high (YAML parsing + API). 6. International: high. 7. Founder reputation: high. 8. Defensibility: high (compounding data + integrations).

## Principles
Authorized/ethical only. No fake metrics. Evidence-labeled claims. No spend/publish/deploy without explicit approval.
