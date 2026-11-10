# Contributing to SteadyCI

## Ground rules
- Authorized/ethical use only. No fake metrics. Credit: Sumit Rao.
- Keep the scanner **local-first** and deterministic. Network features must be opt-in.
- Every rule needs: stable `rule_id`, severity, category, clear message, remediation, and tests.

## Dev setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]" PyYAML
make check
```

## Adding a rule
1. Implement in `steadyci/scanner/rules.py` with a new `SEC|REL|MAINT|COST` ID.
2. Add a doc in `docs/rules/<ID>.md` (what, why, fix, references).
3. Add `unittest` coverage in `tests/`.
4. Run `make check`.

## Pull requests
- One logical change per PR. Include tests. No unrelated refactors.
