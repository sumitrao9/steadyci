"""Workflow model: parsed representation of a GitHub Actions workflow file."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class Job:
    name: str
    runs_on: list[str] = field(default_factory=list)
    steps: list["Step"] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    if_expr: str | None = None
    needs: list[str] = field(default_factory=list)
    strategy: dict[str, Any] = field(default_factory=dict)
    permissions: dict[str, str] | None = None
    container: Any = None
    services: dict[str, Any] = field(default_factory=dict)


@dataclass
class Step:
    name: str
    uses: str | None = None
    run: str | None = None
    with_: dict[str, Any] = field(default_factory=dict)
    env: dict[str, str] = field(default_factory=dict)
    if_expr: str | None = None


@dataclass
class Workflow:
    path: str
    name: str | None
    on: Any = None
    env: dict[str, str] = field(default_factory=dict)
    permissions: dict[str, str] | None = None
    jobs: list[Job] = field(default_factory=list)
    defaults: dict[str, Any] = field(default_factory=dict)
    concurrency: Any = None

    @property
    def triggers(self) -> list[str]:
        """Return normalized trigger list."""
        if self.on is None:
            return []
        if isinstance(self.on, str):
            return [self.on]
        if isinstance(self.on, list):
            return list(self.on)
        if isinstance(self.on, dict):
            keys = [k for k, v in self.on.items() if v is not False]
            return keys
        return []


def _normalize_runs_on(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, dict):
        # matrix include/exclude
        return [str(value.get("group", value))]
    return [str(value)]


def parse_workflow_file(path: Path) -> Workflow:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return Workflow(path=str(path), name=None)

    jobs_raw = raw.get("jobs") or {}
    jobs: list[Job] = []
    for job_name, job_def in jobs_raw.items():
        if not isinstance(job_def, dict):
            continue
        steps: list[Step] = []
        for s in job_def.get("steps") or []:
            if not isinstance(s, dict):
                continue
            steps.append(
                Step(
                    name=str(s.get("name", "")),
                    uses=s.get("uses"),
                    run=s.get("run"),
                    with_=dict(s.get("with") or {}),
                    env={str(k): str(v) for k, v in (s.get("env") or {}).items()},
                    if_expr=s.get("if"),
                )
            )
        jobs.append(
            Job(
                name=str(job_name),
                runs_on=_normalize_runs_on(job_def.get("runs-on")),
                steps=steps,
                env={str(k): str(v) for k, v in (job_def.get("env") or {}).items()},
                if_expr=job_def.get("if"),
                needs=list(job_def.get("needs") or []),
                strategy=dict(job_def.get("strategy") or {}),
                permissions=job_def.get("permissions"),
                container=job_def.get("container"),
                services=dict(job_def.get("services") or {}),
            )
        )

    on_val = raw.get("on") if "on" in raw else raw.get(True)
    return Workflow(
        path=str(path),
        name=raw.get("name"),
        on=on_val,
        env={str(k): str(v) for k, v in (raw.get("env") or {}).items()},
        permissions=raw.get("permissions"),
        jobs=jobs,
        defaults=dict(raw.get("defaults") or {}),
        concurrency=raw.get("concurrency"),
    )


def parse_workflow_text(text: str, path: str = "<input>") -> Workflow:
    raw = yaml.safe_load(text)
    if not isinstance(raw, dict):
        return Workflow(path=path, name=None)

    jobs_raw = raw.get("jobs") or {}
    jobs: list[Job] = []
    for job_name, job_def in jobs_raw.items():
        if not isinstance(job_def, dict):
            continue
        steps: list[Step] = []
        for s in job_def.get("steps") or []:
            if not isinstance(s, dict):
                continue
            steps.append(
                Step(
                    name=str(s.get("name", "")),
                    uses=s.get("uses"),
                    run=s.get("run"),
                    with_=dict(s.get("with") or {}),
                    env={str(k): str(v) for k, v in (s.get("env") or {}).items()},
                    if_expr=s.get("if"),
                )
            )
        jobs.append(
            Job(
                name=str(job_name),
                runs_on=_normalize_runs_on(job_def.get("runs-on")),
                steps=steps,
                env={str(k): str(v) for k, v in (job_def.get("env") or {}).items()},
                if_expr=job_def.get("if"),
                needs=list(job_def.get("needs") or []),
                strategy=dict(job_def.get("strategy") or {}),
                permissions=job_def.get("permissions"),
                container=job_def.get("container"),
                services=dict(job_def.get("services") or {}),
            )
        )

    on_val = raw.get("on") if "on" in raw else raw.get(True)
    return Workflow(
        path=path,
        name=raw.get("name"),
        on=on_val,
        env={str(k): str(v) for k, v in (raw.get("env") or {}).items()},
        permissions=raw.get("permissions"),
        jobs=jobs,
        defaults=dict(raw.get("defaults") or {}),
        concurrency=raw.get("concurrency"),
    )