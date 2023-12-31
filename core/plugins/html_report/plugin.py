import logging
import time

import pytest
from pytest_html import extras

from core.constants import ROOT_DIR

REPORT_DIR = f"{ROOT_DIR}/reports"
REPORT_NAME = "Infinum_Web_Test_Report"
SCREENSHOT_DIR = f"{ROOT_DIR}/reports/screenshots"

# Base URL of the test repository
COMMON_URL = "https://www.website.com/test-case-repository/"


@pytest.hookimpl
def pytest_configure(config: pytest.Config):
    """Configures HTML report."""
    timestamp = time.strftime("%Y-%m-%d_%H-%M")
    report_name = f"{REPORT_NAME}_{timestamp}.html"
    config.option.htmlpath = f"{REPORT_DIR}/{report_name}"


def pytest_html_report_title(report):
    """Formats the name on the HTML report."""
    report.title = REPORT_NAME.replace("_", " ")


def save_url(extra, test_id: list):
    """Appends URL(s) to the Links column in the HTML report.

    Args:
        extra: extra (pytest-html content object)
        test_id: test case identifier in the URL, e.g. "ID-123"
    """
    for id in test_id:
        extra.append(extras.url(f"{COMMON_URL}{id}", name=id))


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item):
    """Takes screenshot when test fails and appends it to the HTML report."""
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.failed:
        timestamp = str(int(time.time()))
        image_name = f"{item.name}_failure_{timestamp}.png"
        image_path = f"{SCREENSHOT_DIR}/{image_name}"

        try:
            driver = item.funcargs["driver"]
            driver.save_screenshot(image_path)
            screenshot = driver.get_screenshot_as_base64()
            extra.append(extras.image(screenshot))
            setattr(report, "extra", extra)
        except Exception as e:
            logging.info(f"Saving screenshot failed!\n{str(e)}")
