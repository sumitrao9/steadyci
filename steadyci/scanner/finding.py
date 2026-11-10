"""Finding model: a single issue detected in a workflow."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    ERROR = "error"
    WARN = "warn"
    INFO = "info"

    def __str__(self) -> str:
        return self.value.upper()


class Category(str, Enum):
    SECURITY = "security"
    MAINTENANCE = "maintenance"
    COST = "cost"
    RELIABILITY = "reliability"

    def __str__(self) -> str:
        return self.value


@dataclass
class Finding:
    rule_id: str
    severity: Severity
    category: Category
    message: str
    location: str = ""
    remediation: str = ""
    action: str | None = None  # the Action being referenced, if applicable

    def to_dict(self) -> dict:
        return {
            "rule_id": self.rule_id,
            "severity": str(self.severity),
            "category": str(self.category),
            "message": self.message,
            "location": self.location,
            "remediation": self.remediation,
            "action": self.action,
        }