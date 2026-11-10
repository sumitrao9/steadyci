.PHONY: lint test scan smoke check
lint:
	python3 -m ruff check .

test:
	PYTHONPATH=. python3 -m unittest discover -s tests -p "test_*.py" -v

scan:
	PYTHONPATH=. python3 -m steadyci.cli scan . --format text

smoke:
	PYTHONPATH=. python3 -m steadyci.cli scan . --format json --fail-on none --no-telemetry

check: lint test smoke
