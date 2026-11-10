"""Local metrics store for growth intelligence (no external deps)."""

from __future__ import annotations

import json
import os
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any


class MetricsStore:
    def __init__(self, path: Path | None = None):
        self.path = path or Path.home() / ".steadyci" / "metrics.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._init()

    def _init(self) -> None:
        with self._lock:
            self._conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ts REAL NOT NULL,
                    name TEXT NOT NULL,
                    props TEXT NOT NULL DEFAULT '{}'
                );
                CREATE INDEX IF NOT EXISTS idx_events_name_ts ON events(name, ts);
                """
            )
            self._conn.commit()

    def track(self, name: str, props: dict[str, Any] | None = None) -> None:
        # opt-out: STEADYCI_TELEMETRY=0
        if os.environ.get("STEADYCI_TELEMETRY", "1") == "0":
            return
        with self._lock:
            self._conn.execute(
                "INSERT INTO events(ts,name,props) VALUES(?,?,?)",
                (time.time(), name, json.dumps(props or {})),
            )
            self._conn.commit()

    def summary(self, days: int = 30) -> dict[str, Any]:
        since = time.time() - days * 86400
        with self._lock:
            rows = self._conn.execute(
                "SELECT name, COUNT(*) c FROM events WHERE ts>=? GROUP BY name ORDER BY c DESC",
                (since,),
            ).fetchall()
        return {"days": days, "events": {r["name"]: r["c"] for r in rows}}

    def close(self) -> None:
        with self._lock:
            self._conn.close()


_default: MetricsStore | None = None


def track(name: str, props: dict[str, Any] | None = None) -> None:
    global _default
    if _default is None:
        _default = MetricsStore()
    _default.track(name, props)
