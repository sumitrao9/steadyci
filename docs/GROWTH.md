# SteadyCI — Growth & Metrics Spec

## North star
**Weekly Active Repos with ≥1 fix applied** (activation + retention + value).

## Funnel
1. **Acquire:** GitHub/SEO/search → README, landing page, action page, blog.
2. **Activate:** run `steadyci scan` → see first actionable finding → apply first fix (pin SHA / set permissions).
3. **Retain:** add to CI or schedule → weekly trend.
4. **Revenue:** team needs dashboard/policy/SSO → Pro/Enterprise.
5. **Refer:** shareable health report/badge; "fixed by SteadyCI" PR.

## Events (local-first, opt-out)
- `scan_started`, `scan_completed` (repo hash, workflow count, score, error/warn/info counts)
- `report_shared` (channel)
- `fix_suggested`, `fix_applied` (rule_id)
- `repo_connected`, `alert_sent`
- `upgrade_viewed`, `checkout_started`, `paid_converted`

## Dashboard (autonomous growth intelligence)
Panels: new/active/returning repos, acquisition source, activation rate, retention (D7/D30 repeat scan), top rules triggered, top rules fixed, paid conversion, MRR, infra cost, LTV:CAC proxy. 
**Recommendation engine (rule-based v1):** if activation low → improve first-run output; if retention low → add CI bot/reminders; if acquisition low → double down on highest-converting landing page; if paid low but active high → test Pro gate.

## SEO landing pages (problem-first)
- "Pin GitHub Actions to a commit SHA"
- "GitHub Actions permissions: least privilege"
- "Fix deprecated ubuntu-20.04 runner"
- "Prevent script injection in GitHub Actions"
- "GitHub Actions supply chain security checklist"

## Loops (no spam)
- Public action reputation pages (e.g., `/actions/actions/checkout`) — organic search.
- Badge: "Actions Health: A/B/C" links to report.
- PR bot suggests fixes; maintainer merges = proof.
