"""Scan orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .finding import Finding, Severity
from .model import Workflow, parse_workflow_file
from .rules import check_workflow


@dataclass
class ScanResult:
    workflows: list[Workflow] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == Severity.ERROR]

    @property
    def warnings(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == Severity.WARN]

    @property
    def infos(self) -> list[Finding]:
        return [f for f in self.findings if f.severity == Severity.INFO]

    @property
    def score(self) -> int:
        """0-100 health score. Simple weighted penalty."""
        penalty = len(self.errors) * 12 + len(self.warnings) * 4 + len(self.infos) * 1
        return max(0, 100 - penalty)

    def to_dict(self) -> dict:
        return {
            "workflows_scanned": len(self.workflows),
            "score": self.score,
            "counts": {
                "error": len(self.errors),
                "warn": len(self.warnings),
                "info": len(self.infos),
            },
            "findings": [f.to_dict() for f in self.findings],
        }


def discover_workflow_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    candidates = []
    wf_dir = path / ".github" / "workflows" if (path / ".github").is_dir() else path
    if wf_dir.is_dir():
        for p in sorted(wf_dir.iterdir()):
            if p.suffix in (".yml", ".yaml") and p.is_file():
                candidates.append(p)
    return candidates


def scan_path(path: Path) -> ScanResult:
    result = ScanResult()
    for wf_path in discover_workflow_files(path):
        try:
            wf = parse_workflow_file(wf_path)
        except Exception as e:
            result.findings.append(
                Finding(
                    "PARSE001",
                    Severity.ERROR,
                    __import__("steadyci.scanner.finding", fromlist=["Category"]).Category.RELIABILITY,
                    f"Failed to parse workflow: {e}",
                    location=str(wf_path),
                )
            )
            continue
        result.workflows.append(wf)
        result.findings.extend(check_workflow(wf))
    return result
