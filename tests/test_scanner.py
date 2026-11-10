"""Scanner tests (unittest)."""

import unittest

from steadyci.scanner import parse_workflow_text
from steadyci.scanner.rules import check_workflow


def _scan(text: str):
    wf = parse_workflow_text(text, "ci.yml")
    return check_workflow(wf)


class TestScanner(unittest.TestCase):
    def test_unpinned_action_flagged(self):
        yml = """
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo hi
"""
        findings = _scan(yml)
        self.assertTrue(any(f.rule_id == "SEC010" for f in findings))

    def test_sha_pinned_ok(self):
        yml = """
name: CI
on: [push]
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
      - run: echo hi
"""
        findings = _scan(yml)
        self.assertFalse(any(f.rule_id == "SEC010" for f in findings))

    def test_deprecated_runner(self):
        yml = """
name: CI
on: [push]
jobs:
  build:
    runs-on: ubuntu-20.04
    steps:
      - run: echo hi
"""
        findings = _scan(yml)
        self.assertTrue(any(f.rule_id == "REL001" for f in findings))

    def test_script_injection(self):
        yml = """
name: CI
on: [pull_request_target]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo ${{ github.event.pull_request.title }}
"""
        findings = _scan(yml)
        self.assertTrue(any(f.rule_id == "SEC011" for f in findings))
        self.assertTrue(any(f.rule_id == "SEC004" for f in findings))

    def test_write_all_permissions(self):
        yml = """
name: CI
on: [push]
permissions: write-all
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo hi
"""
        findings = _scan(yml)
        self.assertTrue(any(f.rule_id == "SEC002" for f in findings))


if __name__ == "__main__":
    unittest.main()
