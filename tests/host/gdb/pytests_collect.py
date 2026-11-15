from __future__ import annotations

import os
import sys

import pytest
from _pytest.skipping import evaluate_skip_marks

TESTS_PATH = os.environ.get("TESTS_PATH")

if TESTS_PATH is None:
    print("'TESTS_PATH' environment variable not set. Failed to collect tests.")
    sys.exit(1)


class CollectTestFunctionNames:
    """See https://github.com/pytest-dev/pytest/issues/2039#issuecomment-257753269"""

    def __init__(self):
        self.collected = []

    def pytest_collection_modifyitems(self, items):
        for item in items:
            try:
                skip = evaluate_skip_marks(item)
            except (Exception, pytest.fail.Exception):
                skip = None  # a bad mark still errors when the test runs
            self.collected.append((item.nodeid, skip))


collector = CollectTestFunctionNames()
rv = pytest.main(["--collect-only", TESTS_PATH], plugins=[collector])

if rv == pytest.ExitCode.INTERRUPTED:
    print("Failed to collect all tests, perhaps there is a syntax error in one of test files?")
    sys.exit(1)


print("Listing collected tests:")
for nodeid, skip in collector.collected:
    print("Test:", nodeid)
    # The host skips these without starting GDB; stderr keeps reasons out of the test-name scan.
    if skip and isinstance(skip.reason, str) and "\n" not in skip.reason:
        print(f"Skip: {nodeid}\t{skip.reason}", file=sys.stderr)

# easy way to exit GDB session
sys.exit(0)
