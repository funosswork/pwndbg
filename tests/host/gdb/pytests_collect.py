from __future__ import annotations

import os
import sys

import pytest

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
            self.collected.append((item.nodeid, item.get_closest_marker("skip")))


collector = CollectTestFunctionNames()
rv = pytest.main(["--collect-only", TESTS_PATH], plugins=[collector])

if rv == pytest.ExitCode.INTERRUPTED:
    print("Failed to collect all tests, perhaps there is a syntax error in one of test files?")
    sys.exit(1)


print("Listing collected tests:")
for nodeid, skip in collector.collected:
    print("Test:", nodeid)
    if skip is not None:
        # Lets the host report the skip without starting a GDB session for it.
        print(
            "Skip:", skip.kwargs.get("reason", skip.args[0] if skip.args else "unconditional skip")
        )

# easy way to exit GDB session
sys.exit(0)
