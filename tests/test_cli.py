import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class TestCLI(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "steadyci.cli", *args],
            cwd=ROOT,
            env={"PYTHONPATH": str(ROOT), "STEADYCI_TELEMETRY": "0"},
            capture_output=True,
            text=True,
            check=False,
        )

    def test_scan_json(self):
        r = self._run("scan", ".", "--format", "json", "--fail-on", "none")
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertIn("score", d)
        self.assertIn("workflows_scanned", d)

    def test_scan_markdown(self):
        r = self._run("scan", ".", "--format", "markdown", "--fail-on", "none")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("SteadyCI Actions Health Report", r.stdout)

    def test_metrics(self):
        r = self._run("metrics")
        self.assertEqual(r.returncode, 0, r.stderr)
        json.loads(r.stdout)


if __name__ == "__main__":
    unittest.main()
