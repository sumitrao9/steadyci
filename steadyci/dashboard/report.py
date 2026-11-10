"""Growth intelligence dashboard — local metrics summary with auto-recommendations (Mission §5)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field

from .metrics import MetricsStore


@dataclass
class GrowthReport:
    days: int
    events: dict[str, int]
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"days": self.days, "events": self.events, "recommendations": self.recommendations}

    def to_markdown(self) -> str:
        lines = [f"# SteadyCI Growth Report ({self.days}d)", ""]
        lines += ["## Events", "", "| Event | Count |", "|---|---|"]
        for k, v in sorted(self.events.items(), key=lambda x: -x[1]):
            lines.append(f"| `{k}` | {v} |")
        lines += ["", "## Recommendations", ""]
        for r in self.recommendations:
            lines.append(f"- {r}")
        return "\n".join(lines)


def _recommend(events: dict[str, int]) -> list[str]:
    recs = []
    scans = events.get("scan_completed", 0)
    if scans == 0:
        recs.append("No scans recorded yet — run `steadyci scan .` to activate the growth loop.")
    elif scans < 10:
        recs.append(f"Only {scans} scans recorded. Drive adoption via the GitHub Action and SEO landing pages.")
    fixes = events.get("fix_applied", 0)
    if fixes < scans and scans > 0:
        recs.append("Fix-applied rate is low — add PR annotations and SHA-pin suggestions to close the activation loop.")
    if events.get("upgrade_viewed", 0) == 0 and scans > 20:
        recs.append("Activation is decent but no upgrade intent — test a Pro CTA on the report page.")
    if events.get("paid_converted", 0) == 0:
        recs.append("No paid conversions yet — validate willingness-to-pay with 20 interviews before billing.")
    if not recs:
        recs.append("Metrics look healthy. Keep measuring: activation, retention, and referral.")
    return recs


def build(days: int = 30) -> GrowthReport:
    store = MetricsStore()
    summary = store.summary(days=days)
    events = summary.get("events", {})
    return GrowthReport(days=days, events=events, recommendations=_recommend(events))


def main() -> int:
    import argparse

    p = argparse.ArgumentParser(prog="steadyci growth")
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    args = p.parse_args()
    r = build(days=args.days)
    if args.format == "json":
        print(json.dumps(r.to_dict(), indent=2))
    elif args.format == "markdown":
        print(r.to_markdown())
    else:
        print(f"SteadyCI Growth Report ({args.days}d)")
        print(f"Events: {sum(r.events.values())} total")
        for k, v in sorted(r.events.items(), key=lambda x: -x[1]):
            print(f"  {k}: {v}")
        print("\nRecommendations:")
        for rec in r.recommendations:
            print(f"  - {rec}")
    return 0
