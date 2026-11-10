# SteadyCI — Research Notes (evidence-labeled)

## Market signals (verified, web sources 2026)
- **Scale:** GitHub Actions used 11.5B minutes in 2025 (+35% YoY); Marketplace has 30k+ actions; 40M developers on GitHub. (Stack Overflow / GitHub ecosystem reporting, Oct 2026)
- **Security:** Kaspersky GReAT examined ~30k starred repos and found 250k+ potential misconfigurations in Actions workflows (Jun 2026). Common: overly broad permissions, unpinned actions/deps, exposed secrets, unsafe triggers, insecure external input.
- **Supply-chain incidents:** Trivy/tj-actions compromise (Mar 2026) showed tag-pinning risk; Shai-Hulud npm worm (May 2026) compromised 170+ packages incl. TanStack, Mistral AI, OpenSearch via pipeline weaknesses.
- **Quality/maintenance:** Legit Security: only 913/19,113 marketplace actions verified; avg OpenSSF Scorecard 4.23/10; 762 archived; many maintained by a single dev. lastseen.dev (Aug 2026): 80.7% of all Actions unmaintained, but the head (widely adopted) is ~10–25% — meaning real repos see less abandonment than the long tail, but the tail is huge and risky.
- **SBOM/compliance:** EU CRA and buyers push SBOMs/attestations; SBOM adoption in OSS still low (IEEE SANER 2026 study, 3100+ repos). CI pipeline components are often missing from SBOM thinking.

## Competitive landscape (high-level)
- **Linters/scanners:** `actionlint`, `zizmor`, `poutine`/StepSecurity checks, OpenSSF Scorecard — strong on point-in-time checks; weak on *compounding reputation data* and cost/maintenance trends over time.
- **Hosted security:** StepSecurity, GitHub Advanced Security/Dependabot — enterprise-grade; opportunity for an open-core, developer-first wedge with a public reputation graph.

## Differentiation hypothesis
1. **Compounding data moat:** a per-action reputation graph (archived/last-commit/CVE-correlation/adoption) that improves with every scan.
2. **Unified view:** security + maintenance + cost in one score (not three tools).
3. **Open core + viral distribution:** free CLI/bot + shareable report + SEO problem pages.

## Risks
- GitHub could ship native action reputation/scoring (platform risk). Mitigation: be the open, cross-platform data layer; integrate early.
- Data accuracy for maintenance/CVE correlation. Mitigation: cite sources, show confidence, allow overrides.
- False positives erode trust. Mitigation: severity calibration, rule tests, "why this matters" links.

## Validation plan (no spend)
- Ship scanner + 5 SEO pages + 1 "State of GitHub Actions Health" report.
- Measure: scans, activation (first fix), repeat scans, GitHub stars/installs, inbound requests for Pro.
- Talk to 20 DevSecOps/platform engineers; test willingness-to-pay for team dashboard/policy.
