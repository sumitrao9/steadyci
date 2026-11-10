"""Scan configuration and baseline."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib
except Exception:  # pragma: no cover
    tomllib = None  # type: ignore


@dataclass
class ScanConfig:
    ignore_rules: set[str] = field(default_factory=set)
    ignore_paths: list[str] = field(default_factory=list)
    fail_on: str = "error"  # error|warn|none
    baseline_file: str | None = None

    @classmethod
    def load(cls, path: Path | None) -> "ScanConfig":
        cfg = cls()
        if not path or not path.exists():
            # auto-detect
            for cand in (Path("steadyci.toml"), Path(".steadyci.toml"), Path("pyproject.toml")):
                if cand.exists():
                    path = cand
                    break
        if not path or not path.exists() or tomllib is None:
            return cfg
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return cfg
        t = data.get("tool", {}).get("steadyci", data.get("steadyci", {})) if path.name == "pyproject.toml" else data.get("steadyci", data)
        cfg.ignore_rules = set(t.get("ignore_rules", []) or [])
        cfg.ignore_paths = list(t.get("ignore_paths", []) or [])
        cfg.fail_on = str(t.get("fail_on", cfg.fail_on))
        cfg.baseline_file = t.get("baseline_file")
        return cfg


def load_baseline(path: str | None) -> set[str]:
    if not path:
        return set()
    p = Path(path)
    if not p.exists():
        return set()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return set(data.get("fingerprints", []) or [])
    except Exception:
        return set()


def fingerprint(finding) -> str:
    return f"{finding.rule_id}|{finding.location}|{finding.message}"


def apply_config(result, cfg: ScanConfig):
    baseline = load_baseline(cfg.baseline_file)
    kept = []
    for f in result.findings:
        if f.rule_id in cfg.ignore_rules:
            continue
        if any(ip and ip in f.location for ip in cfg.ignore_paths):
            continue
        if fingerprint(f) in baseline:
            continue
        kept.append(f)
    result.findings = kept
    return result
