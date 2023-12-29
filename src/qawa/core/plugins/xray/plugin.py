import json
from typing import List

import pytest

from src.qawa.core.constants import ROOT_DIR

PAYLOAD = f"{ROOT_DIR}/reports/xray_payload.json"
XRAY_MARK = "xray"

# `test_run_report` must be initialized outside `pytest_runtest_logreport`
# in  order to append results after each test. Otherwise, the data is not saved.
test_run_report = []


def pytest_collection_modifyitems(items: List[pytest.Item]):
    """Appends custom Xray markers to `user_properties` in pytest.Item."""
    for item in items:
        for mark in item.iter_markers(XRAY_MARK):
            xray_test_key = mark.args[0]
            item.user_properties.append(("testKey", xray_test_key))


def pytest_runtest_logreport(report: pytest.TestReport):
    """Collects test results from pytest.TestReport and writes them to a JSON file."""
    outcomes = ["skipped", "failed"]

    test_xray_keys = []

    if XRAY_MARK in report.keywords.keys() and report.keywords[XRAY_MARK]:
        if report.when == "setup" and report.outcome in outcomes:
            test_xray_keys = report.user_properties[0][1]
        elif report.when == "call":
            test_xray_keys = report.user_properties[0][1]

        for key in test_xray_keys:
            _write_test_data_to_json(key=key, status=report.outcome, comment=f"{report.nodeid}\n{report.longreprtext}")


def _write_test_data_to_json(key, status, comment):
    """Writes test data to a JSON file.

    Params:
        key: test key (ID)
        status: test status (pass, fail, error, etc.)
        comment: test info
    """
    test_data = dict(testKey=key, status=status, comment=comment)
    test_run_report.append(test_data)

    payload = json.dumps(dict(tests=test_run_report))

    with open(PAYLOAD, "w") as file:
        file.write(payload)
