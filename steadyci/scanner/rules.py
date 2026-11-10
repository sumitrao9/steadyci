"""Security, maintenance, and cost rules for GitHub Actions workflows."""

from __future__ import annotations

import re
from typing import Iterable

from .actions import DEPRECATED_ACTION_VERSIONS, DEPRECATED_RUNNERS, parse_uses
from .finding import Category, Finding, Severity
from .model import Workflow

_UNTRUSTED = re.compile(
    r"github\.event\.(issue|pull_request|comment|review|head_ref)|github\.head_ref|github\.event\.pull_request\.title|github\.event\.pull_request\.body"
)


def _loc(wf: Workflow, job: str | None = None, step: str | None = None) -> str:
    parts = [wf.path]
    if job:
        parts.append(f"job:{job}")
    if step:
        parts.append(f"step:{step}")
    return " > ".join(parts)


def check_workflow(wf: Workflow) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_check_permissions(wf))
    findings.extend(_check_workflow_secrets(wf))
    findings.extend(_check_triggers(wf))
    findings.extend(_check_pr_head_checkout(wf))
    for job in wf.jobs:
        findings.extend(_check_job(wf, job))
        for i, step in enumerate(job.steps):
            findings.extend(_check_step(wf, job, step, i))
    return findings


def _check_permissions(wf: Workflow) -> Iterable[Finding]:
    if wf.permissions is None:
        # default in many cases is write-all for older repos; flag as warn
        yield Finding(
            "SEC001",
            Severity.WARN,
            Category.SECURITY,
            "No top-level permissions declared; defaults may be overly broad",
            location=_loc(wf),
            remediation="Add `permissions:` with least privilege, e.g. `contents: read`.",
        )
        return
    if wf.permissions == "write-all" or wf.permissions == {}:
        yield Finding(
            "SEC002",
            Severity.ERROR,
            Category.SECURITY,
            "Workflow grants write-all or empty permissions (effectively broad access)",
            location=_loc(wf),
            remediation="Declare minimal `permissions:` per job.",
        )


def _check_workflow_secrets(wf: Workflow) -> Iterable[Finding]:
    if wf.env:
        for k, v in wf.env.items():
            if "secrets." in str(v).lower() or "token" in k.lower():
                yield Finding(
                    "SEC003",
                    Severity.WARN,
                    Category.SECURITY,
                    f"Secret-like value referenced at workflow-level env (`{k}`)",
                    location=_loc(wf),
                    remediation="Move secrets to the smallest step/job scope that needs them.",
                )


def _check_triggers(wf: Workflow) -> Iterable[Finding]:
    triggers = set(wf.triggers)
    if "pull_request_target" in triggers and "pull_request" not in triggers:
        yield Finding(
            "SEC004",
            Severity.WARN,
            Category.SECURITY,
            "`pull_request_target` runs with base-repo permissions; treat PR code as untrusted",
            location=_loc(wf),
            remediation="Avoid checking out untrusted PR code with write permissions; prefer `pull_request` or isolate.",
        )


def _check_job(wf: Workflow, job) -> Iterable[Finding]:
    for runner in job.runs_on:
        r = runner.lower()
        if r in DEPRECATED_RUNNERS:
            yield Finding(
                "REL001",
                Severity.ERROR,
                Category.RELIABILITY,
                f"Deprecated runner `{runner}` may be removed; CI will break",
                location=_loc(wf, job.name),
                remediation="Use a supported runner (e.g., `ubuntu-24.04`, `windows-latest`).",
            )
    if job.permissions == "write-all" or job.permissions == {}:
        yield Finding(
            "SEC002",
            Severity.ERROR,
            Category.SECURITY,
            "Job grants write-all or empty permissions",
            location=_loc(wf, job.name),
            remediation="Set minimal job `permissions:`.",
        )
    strat = job.strategy or {}
    matrix = strat.get("matrix") or {}
    if isinstance(matrix, dict):
        # rough size estimate
        size = 1
        for k, v in matrix.items():
            if k in ("include", "exclude"):
                continue
            if isinstance(v, list):
                size *= max(len(v), 1)
        if size >= 64:
            yield Finding(
                "COST001",
                Severity.INFO,
                Category.COST,
                f"Matrix expands to ~{size} combinations; check runner minutes cost",
                location=_loc(wf, job.name),
                remediation="Use `fail-fast`, narrow matrix, or split into targeted jobs.",
            )


def _check_step(wf: Workflow, job, step, idx: int) -> Iterable[Finding]:
    step_label = step.name or f"#{idx+1}"
    if step.uses:
        ref = parse_uses(step.uses)
        if ref and not ref.is_docker:
            if not ref.is_sha:
                sev = Severity.ERROR if not ref.is_official else Severity.WARN
                yield Finding(
                    "SEC010",
                    sev,
                    Category.SECURITY,
                    f"Action `{step.uses}` is not pinned to a commit SHA",
                    location=_loc(wf, job.name, step_label),
                    remediation="Pin to a full commit SHA and optionally keep a version comment.",
                    action=f"{ref.owner}/{ref.repo}",
                )
            key = (f"{ref.owner}/{ref.repo}", ref.ref)
            if key in DEPRECATED_ACTION_VERSIONS or (f"{ref.owner}/{ref.repo}", ref.ref.split("@")[-1]) in DEPRECATED_ACTION_VERSIONS:
                yield Finding(
                    "MAINT001",
                    Severity.WARN,
                    Category.MAINTENANCE,
                    f"Action `{step.uses}` uses a known-deprecated major version",
                    location=_loc(wf, job.name, step_label),
                    remediation="Upgrade to the latest supported major and pin by SHA.",
                    action=f"{ref.owner}/{ref.repo}",
                )
    if step.run:
        if _UNTRUSTED.search(step.run):
            yield Finding(
                "SEC011",
                Severity.ERROR,
                Category.SECURITY,
                "Untrusted event data interpolated into `run:` (script injection risk)",
                location=_loc(wf, job.name, step_label),
                remediation="Pass untrusted values via `env:` and reference as `$VAR` (quoted), not `${{ }}` in shell.",
            )
        if "curl" in step.run and "| sh" in step.run:
            yield Finding(
                "SEC012",
                Severity.WARN,
                Category.SECURITY,
                "`curl | sh` pattern executes remote code at runtime",
                location=_loc(wf, job.name, step_label),
                remediation="Download, verify checksum/signature, then execute.",
            )


def _check_pr_head_checkout(wf: Workflow) -> Iterable[Finding]:
    triggers = set(wf.triggers)
    if "pull_request_target" not in triggers:
        return []
    findings = []
    for job in wf.jobs:
        for i, step in enumerate(job.steps):
            if step.uses and "actions/checkout" in step.uses:
                ref = (step.with_ or {}).get("ref", "")
                if "pull_request.head" in str(ref) or "github.event.pull_request" in str(ref):
                    findings.append(
                        Finding(
                            "SEC005",
                            Severity.ERROR,
                            Category.SECURITY,
                            "Checking out PR head in `pull_request_target` grants write-token context to untrusted code",
                            location=_loc(wf, job.name, step.name or f"#{i+1}"),
                            remediation="Do not checkout untrusted PR code under pull_request_target; use `pull_request` or run untrusted code in an unprivileged job.",
                        )
                    )
    return findings
