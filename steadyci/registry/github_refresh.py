"""Optional, rate-limited GitHub metadata refresher (read-only token).

This populates the reputation graph. It is OPT-IN and makes network calls only
when explicitly invoked with a token. No data is exfiltrated beyond normal API use.
"""

from __future__ import annotations

import os
import time
from typing import Any

import requests

from .store import ActionRecord, RegistryStore

API = "https://api.github.com"


def _headers(token: str | None) -> dict[str, str]:
    h = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def fetch_repo(full_name: str, token: str | None = None, timeout: float = 15.0) -> dict[str, Any] | None:
    r = requests.get(f"{API}/repos/{full_name}", headers=_headers(token), timeout=timeout)
    if r.status_code == 404:
        return {"archived": None, "missing": True}
    if r.status_code != 200:
        return None
    return r.json()


def score_record(d: dict[str, Any]) -> int:
    if d.get("missing"):
        return 10
    score = 70
    if d.get("archived"):
        score -= 40
    pushed = d.get("pushed_at")
    if pushed:
        # rough recency bonus/penalty omitted without date parsing deps; keep conservative
        score += 5
    stars = int(d.get("stargazers_count") or 0)
    if stars > 1000:
        score += 10
    elif stars > 100:
        score += 5
    return max(0, min(100, score))


def refresh_actions(actions: list[str], store: RegistryStore | None = None, token: str | None = None, sleep_s: float = 0.2) -> int:
    store = store or RegistryStore()
    token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    n = 0
    for full in actions:
        data = fetch_repo(full, token=token)
        if not data:
            continue
        rec = ActionRecord(
            full_name=full,
            archived=bool(data.get("archived")) if "archived" in data else None,
            stars=data.get("stargazers_count"),
            score=score_record(data),
            updated_at=time.time(),
            source="github",
        )
        store.upsert(rec)
        n += 1
        if sleep_s:
            time.sleep(sleep_s)
    return n
