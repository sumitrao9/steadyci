"""Action reference parsing utilities."""

from __future__ import annotations

import re
from dataclasses import dataclass

# Matches: owner/repo@ref  (ref may contain / for paths like subdirs)
_USES_RE = re.compile(r"^([A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+)@(.+)$")
# docker://image@sha256:...
_DOCKER_RE = re.compile(r"^docker://(.+)$")

# Known deprecated GitHub-hosted runners (as of late 2026)
DEPRECATED_RUNNERS = {
    "ubuntu-18.04",
    "ubuntu-20.04",
    "ubuntu-22.04-arm",
    "macos-11",
    "macos-12",
    "windows-17",
    "windows-18",
}

# Known deprecated official action versions
DEPRECATED_ACTION_VERSIONS = {
    ("actions/checkout", "v1"),
    ("actions/checkout", "v2"),
    ("actions/checkout", "v3"),
    ("actions/setup-node", "v1"),
    ("actions/setup-node", "v2"),
    ("actions/setup-node", "v3"),
    ("actions/setup-python", "v1"),
    ("actions/setup-python", "v2"),
    ("actions/setup-python", "v3"),
    ("actions/setup-java", "v1"),
    ("actions/setup-java", "v2"),
    ("actions/setup-go", "v1"),
    ("actions/setup-go", "v2"),
    ("actions/cache", "v1"),
    ("actions/cache", "v2"),
    ("actions/upload-artifact", "v1"),
    ("actions/upload-artifact", "v2"),
    ("actions/download-artifact", "v1"),
    ("actions/download-artifact", "v2"),
    ("github/codeql-action", "v1"),
    ("github/codeql-action", "v2"),
    ("actions/dependency-review-action", "v1"),
    ("actions/first-interaction", "v1"),
    ("actions/github-script", "v3"),
    ("actions/github-script", "v4"),
    ("actions/labeler", "v3"),
    ("actions/labeler", "v4"),
    ("actions/checkout", "main"),
}

# Expensive / slow runners (cost heuristic)
EXPENSIVE_RUNNERS = {
    "ubuntu-latest",
    "ubuntu-latest-arm",
    "windows-latest",
    "macos-latest",
    "macos-14",
    "macos-15",
    "ubuntu-24.04",
}

# Official action repos that are still fine; everything else is a third-party Action
OFFICIAL_ACTIONS_PREFIX = "actions/"


@dataclass
class ActionRef:
    owner: str
    repo: str
    ref: str
    is_pin: bool = False
    is_sha: bool = False

    @property
    def full(self) -> str:
        return f"{self.owner}/{self.repo}@{self.ref}"

    @property
    def is_docker(self) -> bool:
        return self.owner == "docker"

    @property
    def is_official(self) -> bool:
        return self.owner == "actions"


def parse_uses(uses: str) -> ActionRef | None:
    """Parse a `uses:` value into an ActionRef."""
    if not uses:
        return None
    if uses.startswith("docker://"):
        rest = uses[len("docker://"):]
        if "@" in rest:
            owner, repo, ref = "docker", rest.split("/")[0], rest.split("@", 1)[1]
            return ActionRef(owner="docker", repo=repo, ref=ref, is_pin=True, is_sha=True)
        return ActionRef(owner="docker", repo=rest, ref="latest", is_pin=False)
    m = _USES_RE.match(uses)
    if not m:
        return None
    owner, repo = m.group(1).split("/", 1)
    ref = m.group(2)
    is_sha = bool(re.match(r"^[0-9a-f]{7,40}$", ref))
    is_pin = is_sha or ref.startswith("v")
    return ActionRef(owner=owner, repo=repo, ref=ref, is_pin=is_pin, is_sha=is_sha)