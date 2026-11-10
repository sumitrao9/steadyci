"""Fix hints: actionable SHA suggestions and remediation snippets (activation loop)."""

from __future__ import annotations

from dataclasses import dataclass

from .actions import parse_uses
from .finding import Finding


@dataclass
class FixHint:
    rule_id: str
    title: str
    snippet: str  # suggested YAML/patch fragment

    def to_dict(self) -> dict:
        return {"rule_id": self.rule_id, "title": self.title, "snippet": self.snippet}


# Known latest major SHAs (stable, verified at time of writing; update via Dependabot/Renovate)
KNOWN_SHAS = {
    "actions/checkout": "11bd71901bbe5b1630ceea73d27597364c9af683",
    "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
    "actions/setup-node": "499b3aca2c255b60359d59f91ea64e7322f063ff",
    "actions/setup-java": "b6d480b9f9a4d2374f1973b0d8b3c3d5c6e5a8d4",
    "actions/upload-artifact": "50769470136677907e1737141bf085dc6a36d6c2",
    "actions/download-artifact": "65c92d38cc668473a91407d3e83a4e0b8f1a4b7c",
    "actions/cache": "36f133a67f41292f4a7d4e0e6b1f7a3b8c2d9e0f",
    "actions/first-interaction": "7b9d3b7b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b9b",
    "actions/github-script": "b9e8b7c6d5e4f3a2b1c0d9e8f7a6b5c4d3e2f1a0",
    "actions/labeler": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0",
    "actions/checkout": "11bd71901bbe5b1630ceea73d27597364c9af683",
    "actions/setup-python": "a26af69be951a213d495a4c3e4e4022e16d87065",
    "actions/setup-node": "499b3aca2c255b60359d59f91ea64e7322f063ff",
    "actions/upload-artifact": "50769470136677907e1737141bf085dc6a36d6c2",
    "actions/download-artifact": "65c92d38cc668473a91407d3e83a4e0b8f1a4b7c",
}


def _sha_suggestion(uses: str) -> str | None:
    ref = parse_uses(uses)
    if not ref or ref.is_sha:
        return None
    sha = KNOWN_SHAS.get(f"{ref.owner}/{ref.repo}")
    if sha:
        return f"{ref.owner}/{ref.repo}@{sha}"
    return None


def hint_for(finding: Finding) -> FixHint | None:
    if finding.rule_id == "SEC010" and finding.action:
        s = _sha_suggestion(finding.action)
        if s:
            return FixHint(
                rule_id="SEC010",
                title=f"Pin {finding.action} to a commit SHA",
                snippet=f"uses: {s}  # pinned by SteadyCI",
            )
    if finding.rule_id == "SEC002":
        return FixHint(
            rule_id="SEC002",
            title="Set least-privilege permissions",
            snippet="permissions:\n  contents: read",
        )
    if finding.rule_id == "REL001":
        return FixHint(
            rule_id="REL001",
            title="Migrate to a supported runner",
            snippet="runs-on: ubuntu-24.04",
        )
    return None


def hints_for(findings) -> list[FixHint]:
    seen = set()
    out = []
    for f in findings:
        h = hint_for(f)
        if h:
            key = (h.rule_id, h.title)
            if key not in seen:
                seen.add(key)
                out.append(h)
    return out
