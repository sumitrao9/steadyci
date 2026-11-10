import json
import unittest

from steadyci.scanner import parse_workflow_text
from steadyci.scanner.engine import ScanResult
from steadyci.scanner.rules import check_workflow
from steadyci.scanner.sarif import to_sarif


class TestSarif(unittest.TestCase):
    def test_sarif_shape(self):
        wf = parse_workflow_text("name: CI\non: [push]\njobs:\n  b:\n    runs-on: ubuntu-latest\n    steps:\n      - run: echo hi\n", "ci.yml")
        r = ScanResult(workflows=[wf], findings=check_workflow(wf))
        s = to_sarif(r, "0.1.0")
        self.assertEqual(s["version"], "2.1.0")
        self.assertIn("runs", s)
        json.dumps(s)


if __name__ == "__main__":
    unittest.main()
