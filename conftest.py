"""Main conftest.py file that provides fixtures for the entire project.

Fixtures defined in this file can be used by all tests
and do not have to be imported (discovered automatically by pytest).

Configuration settings are also defined in this file.
"""
import os
import sys

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.service import Service

from core.constants import Browser, Environment

pytest_plugins = [
    "core.plugins.html_report.plugin",
    "core.plugins.xray.plugin",
    "core.plugins.slack.plugin",
]


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--browser", action="store", default=Browser.CHROME)
    parser.addoption("--env", action="store", default=Environment.PROD)


@pytest.fixture(scope="session")
def browser(request: pytest.FixtureRequest):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def environment(request: pytest.FixtureRequest):
    return request.config.getoption("--env")


@pytest.fixture(scope="function", autouse=True)
def driver(browser):
    if browser == Browser.CHROME:
        driver = webdriver.Chrome()
        driver.maximize_window()
    elif browser == Browser.CHROME_HEADLESS:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=chrome_options)
    elif browser == Browser.FIREFOX:
        firefox_service = Service(executable_path="geckodriver", log_path=os.devnull)
        driver = webdriver.Firefox(service=firefox_service)
        driver.maximize_window()
    elif browser == Browser.SAFARI:
        driver = webdriver.Safari()
        driver.maximize_window()
    elif browser == Browser.EDGE:
        driver = webdriver.Edge()
        driver.maximize_window()
    else:
        sys.exit("Browser not supported!")

    yield driver
    driver.quit()
