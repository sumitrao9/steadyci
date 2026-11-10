"""SteadyCI command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .dashboard.growth import build as growth_build
from .dashboard.metrics import track
from .scanner.config import ScanConfig, apply_config, fingerprint
from .scanner.engine import scan_path
from .scanner.report import to_markdown
from .scanner.sarif import to_sarif


def _print_text(result, path: Path) -> int:
    print(f"SteadyCI scan: {path}")
    print(f"Workflows: {len(result.workflows)}  Score: {result.score}/100")
    print(
        f"Findings: {len(result.errors)} error, {len(result.warnings)} warn, {len(result.infos)} info"
    )
    if not result.findings:
        print("No issues found.")
        return 0
    print()
    for f in result.findings:
        loc = f" [{f.location}]" if f.location else ""
        act = f" ({f.action})" if f.action else ""
        print(f"  {f.severity:5} {f.rule_id}  {f.message}{act}{loc}")
        if f.remediation:
            print(f"         → {f.remediation}")
    return 0


def _exit_code(result, fail_on: str) -> int:
    if fail_on == "none":
        return 0
    if result.errors:
        return 1
    if fail_on == "warn" and result.warnings:
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="steadyci", description="GitHub Actions health scanner")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    scan = sub.add_parser("scan", help="Scan workflows in a path")
    scan.add_argument("path", nargs="?", default=".", help="Repo root, workflows dir, or workflow file")
    scan.add_argument("--format", choices=["text", "json", "sarif", "markdown"], default="text")
    scan.add_argument("--fail-on", choices=["error", "warn", "none"], default=None)
    scan.add_argument("--config", help="Path to steadyci.toml / pyproject.toml")
    scan.add_argument("--baseline", help="Path to baseline JSON (fingerprints to ignore)")
    scan.add_argument("--write-baseline", help="Write current findings as baseline JSON")
    scan.add_argument("--no-telemetry", action="store_true", help="Disable local metrics event")

    sub.add_parser("metrics", help="Show local growth metrics summary")
    rep = sub.add_parser("report", help="Export a shareable report")
    rep.add_argument("path", nargs="?", default=".")
    rep.add_argument("--out", help="Output markdown file")
    rep.add_argument("--no-telemetry", action="store_true")

    sub.add_parser("growth", help="Growth intelligence dashboard with recommendations")

    ref = sub.add_parser("refresh-registry", help="(opt-in) Refresh action reputation from GitHub API")
    ref.add_argument("actions", nargs="+", help="Action repos: owner/repo")
    ref.add_argument("--token", help="GitHub token (or set GITHUB_TOKEN/GH_TOKEN)")

    args = p.parse_args(argv)

    if args.cmd == "metrics":
        from .dashboard.metrics import MetricsStore

        print(json.dumps(MetricsStore().summary(), indent=2))
        return 0

    if args.cmd == "growth":
        r = growth_build()
        print(json.dumps(r.to_dict(), indent=2))
        return 0

    if args.cmd == "refresh-registry":
        from .registry.refresh import refresh_actions

        n = refresh_actions(args.actions, token=args.token)
        print(json.dumps({"refreshed": n, "actions": args.actions}))
        return 0

    if args.cmd in ("scan", "report"):
        path = Path(args.path).resolve()
        if not path.exists():
            print(f"Path not found: {path}", file=sys.stderr)
            return 2
        cfg = ScanConfig.load(Path(args.config).resolve() if getattr(args, "config", None) else None)
        if getattr(args, "baseline", None):
            cfg.baseline_file = args.baseline
        if getattr(args, "fail_on", None):
            cfg.fail_on = args.fail_on
        raw = scan_path(path)
        if getattr(args, "write_baseline", None):
            out = {"fingerprints": [fingerprint(f) for f in raw.findings]}
            Path(args.write_baseline).write_text(json.dumps(out, indent=2), encoding="utf-8")
            print(f"Wrote baseline: {args.write_baseline} ({len(out['fingerprints'])} findings)")
            return 0
        result = apply_config(raw, cfg)
        if not args.no_telemetry:
            track(
                "scan_completed",
                {
                    "workflows": len(result.workflows),
                    "score": result.score,
                    "errors": len(result.errors),
                    "warnings": len(result.warnings),
                },
            )
            if result.findings:
                track("report_viewed", {"findings": len(result.findings)})
        if args.cmd == "report" or getattr(args, "format", "") == "markdown":
            md = to_markdown(result)
            if getattr(args, "out", None):
                Path(args.out).write_text(md, encoding="utf-8")
                print(f"Wrote report: {args.out}")
            else:
                print(md)
            return _exit_code(result, getattr(cfg, "fail_on", "error"))
        if args.format == "json":
            print(json.dumps(result.to_dict(), indent=2))
        elif args.format == "sarif":
            print(json.dumps(to_sarif(result, __version__), indent=2))
        else:
            _print_text(result, path)
        return _exit_code(result, cfg.fail_on)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
