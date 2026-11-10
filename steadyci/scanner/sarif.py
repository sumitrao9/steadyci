"""SARIF 2.1.0 output for GitHub code scanning."""

from __future__ import annotations

from .engine import ScanResult
from .finding import Severity

_LEVEL = {Severity.ERROR: "error", Severity.WARN: "warning", Severity.INFO: "note"}


def to_sarif(result: ScanResult, tool_version: str = "0.1.0") -> dict:
    rules = {}
    results = []
    for f in result.findings:
        if f.rule_id not in rules:
            rules[f.rule_id] = {
                "id": f.rule_id,
                "name": f.rule_id,
                "shortDescription": {"text": f.message[:120]},
                "fullDescription": {"text": f.message},
                "help": {"text": f.remediation or f.message},
                "defaultConfiguration": {"level": _LEVEL.get(f.severity, "warning")},
                "properties": {"category": str(f.category)},
            }
        # parse location "path > job:X > step:Y"
        path = f.location.split(" > ")[0] if f.location else ""
        results.append(
            {
                "ruleId": f.rule_id,
                "level": _LEVEL.get(f.severity, "warning"),
                "message": {"text": f.message},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": path, "uriBaseId": "%SRCROOT%"},
                            "region": {"startLine": 1},
                        }
                    }
                ]
                if path
                else [],
            }
        )
    return {
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "SteadyCI",
                        "informationUri": "https://github.com/sumitrao9/steadyci",
                        "version": tool_version,
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
                "invocations": [{"executionSuccessful": True}],
            }
        ],
    }
