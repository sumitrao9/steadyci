"""Growth intelligence dashboard (local MVP).

Tracks the metrics defined in the SteadyCI charter:
- usage/activation (scans, repos, findings fixed)
- acquisition (referrers, share links)
- revenue-ready signals (Pro feature hits)
- retention proxies (repeat scans)

Stores events in a local SQLite DB; exports JSON for a static dashboard.
"""

from .metrics import MetricsStore, track

__all__ = ["MetricsStore", "track"]
