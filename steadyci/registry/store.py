"""SQLite-backed registry for action reputation data.

This is the compounding data asset: the more repos scan, the richer the graph.
It stores observed metadata (last release, archived flag, verified status) and
can be refreshed from GitHub API.
"""

from __future__ import annotations

import sqlite3
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class ActionRecord:
    full_name: str  # owner/repo
    archived: Optional[bool] = None
    verified: Optional[bool] = None
    last_commit_ts: Optional[float] = None
    last_release_ts: Optional[float] = None
    stars: Optional[int] = None
    score: Optional[int] = None  # 0-100 reputation
    updated_at: Optional[float] = None
    source: str = "local"  # local|github


class RegistryStore:
    def __init__(self, path: Path | None = None):
        self.path = path or Path.home() / ".steadyci" / "registry.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(self.path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init()

    def _init(self) -> None:
        with self._lock:
            self._conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS actions (
                    full_name TEXT PRIMARY KEY,
                    archived INTEGER,
                    verified INTEGER,
                    last_commit_ts REAL,
                    last_release_ts REAL,
                    stars INTEGER,
                    score INTEGER,
                    updated_at REAL,
                    source TEXT NOT NULL DEFAULT 'local'
                );
                CREATE INDEX IF NOT EXISTS idx_actions_score ON actions(score);
                """
            )
            self._conn.commit()

    def upsert(self, rec: ActionRecord) -> None:
        now = time.time()
        with self._lock:
            self._conn.execute(
                """INSERT INTO actions(full_name,archived,verified,last_commit_ts,last_release_ts,stars,score,updated_at,source)
                   VALUES(?,?,?,?,?,?,?,?,?)
                   ON CONFLICT(full_name) DO UPDATE SET
                     archived=excluded.archived, verified=excluded.verified,
                     last_commit_ts=excluded.last_commit_ts, last_release_ts=excluded.last_release_ts,
                     stars=excluded.stars, score=excluded.score, updated_at=excluded.updated_at, source=excluded.source""",
                (
                    rec.full_name,
                    None if rec.archived is None else int(rec.archived),
                    None if rec.verified is None else int(rec.verified),
                    rec.last_commit_ts,
                    rec.last_release_ts,
                    rec.stars,
                    rec.score,
                    rec.updated_at or now,
                    rec.source,
                ),
            )
            self._conn.commit()

    def get(self, full_name: str) -> Optional[ActionRecord]:
        with self._lock:
            row = self._conn.execute("SELECT * FROM actions WHERE full_name=?", (full_name,)).fetchone()
        if not row:
            return None
        return ActionRecord(
            full_name=row["full_name"],
            archived=None if row["archived"] is None else bool(row["archived"]),
            verified=None if row["verified"] is None else bool(row["verified"]),
            last_commit_ts=row["last_commit_ts"],
            last_release_ts=row["last_release_ts"],
            stars=row["stars"],
            score=row["score"],
            updated_at=row["updated_at"],
            source=row["source"] or "local",
        )

    def close(self) -> None:
        with self._lock:
            self._conn.close()
