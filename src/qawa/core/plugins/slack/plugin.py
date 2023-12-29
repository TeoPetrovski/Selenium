import logging

import pytest

from src.qawa.core.constants import ROOT_DIR

PAYLOAD_TEMPLATE = f"{ROOT_DIR}/core/plugins/slack/payload_template.json"
PAYLOAD = f"{ROOT_DIR}/reports/slack_payload.json"


def _get_test_run_info(session: pytest.Session):
    """Gets test run info from the terminal reporter."""
    reporter = session.config.pluginmanager.get_plugin("terminalreporter")

    passed_tests = len(reporter.stats.get("passed", []))
    failed_tests = len(reporter.stats.get("failed", []))
    error_tests = len(reporter.stats.get("error", []))
    skipped_tests = len(reporter.stats.get("skipped", []))
    total_test_count = passed_tests + failed_tests + error_tests + skipped_tests

    report_data = {
        "passed": passed_tests,
        "failed": failed_tests,
        "error": error_tests,
        "skipped": skipped_tests,
        "total_test_count": total_test_count,
        "environment": session.config.getoption("--env"),
        "browser": session.config.getoption("--browser"),
    }
    return report_data


def _write_slack_report(session: pytest.Session):
    """Writes collected test run info to the Slack payload file."""
    report_data = _get_test_run_info(session)

    try:
        with open(PAYLOAD_TEMPLATE) as template_file:
            file_data = template_file.read()
            payload = (
                file_data.replace("passed_count", str(report_data["passed"]))
                .replace("failed_count", str(report_data["failed"]))
                .replace("error_count", str(report_data["error"]))
                .replace("skipped_count", str(report_data["skipped"]))
                .replace("total_test_count", str(report_data["total_test_count"]))
                .replace("environment", str(report_data["environment"]))
                .replace("browser", str(report_data["browser"]))
            )

        with open(PAYLOAD, "w") as payload_file:
            payload_file.write(payload)
    except BaseException as e:
        logging.error(f"An error occurred while writing to the payload file:\n{str(e)}")


def pytest_sessionfinish(session: pytest.Session):
    """Generates the Slack payload file."""
    _write_slack_report(session)
