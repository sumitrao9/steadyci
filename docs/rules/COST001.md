# COST001 — Large matrix
- **Severity:** info
- **Category:** cost
- **What:** Job matrix expands to a high number of combinations (heuristic).
- **Why:** Multiplies runner minutes and queue time.
- **Fix:** Use `fail-fast`, narrow dimensions, or split into targeted jobs; measure actual minutes before/after.
