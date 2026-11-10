# SteadyCI — Validation Plan (authorized, evidence-labeled)

## Goal
Prove activation and retention before monetization. No fake metrics. No spend/publish/deploy without explicit approval.

## Steps
1. **Dogfood:** run on own repos/workflows; fix findings; record baseline score and time-to-first-fix.
2. **Authorized pilots (10–20 repos):** scan with maintainer consent; open fix PRs (SHA pinning, permissions, runner upgrades). Track: findings, fixes merged, repeat scans.
3. **Interviews (20):** DevSecOps/platform engineers. Questions: current tooling, pain severity, willingness to pay for dashboard/policy/SSO/API, required integrations.
4. **Public report:** "State of GitHub Actions Health" (sampled, sourced, methodology disclosed) — organic distribution asset.
5. **Decision gates:**
   - ≥100 weekly active repos or ≥10 inbound team-dashboard requests → build Pro.
   - Activation <20% (no fix after scan) → improve fix hints/PR bot before growth spend.
   - Retention <15% repeat scan D30 → add CI integration/reminders.
   - Referral share rate → scale SEO + PR bot.

## Metrics to track (local, opt-in)
- `scan_completed`, `report_viewed`, `fix_applied`, `upgrade_viewed`, `paid_converted`, `share_report`
- Weekly active repos, activation (first fix), retention (D7/D30 repeat scan), organic vs referral, MRR, infra cost, LTV:CAC proxy.
