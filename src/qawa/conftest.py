"""Main conftest.py file that provides fixtures for the entire project.

Fixtures defined in this file can be used by all tests
and do not have to be imported (discovered automatically by pytest).

Configuration settings are also defined in this file.
"""
import sys
from logging import error

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from src.qawa.core.constants import Browser, Environment

pytest_plugins = [
    "src.qawa.core.plugins.html_report.plugin",
    "src.qawa.core.plugins.xray.plugin",
    "src.qawa.core.plugins.slack.plugin",
]


def pytest_addoption(parser: pytest.Parser):
    parser.addoption("--browser", action="store", default=Browser.CHROME.value)
    parser.addoption("--env", action="store", default=Environment.PROD.value)


@pytest.fixture(scope="session")
def browser(request: pytest.FixtureRequest) -> str:
    browser = request.config.getoption("--browser")

    for b in Browser:
        if browser.lower() == b.value:
            return b.value
    else:
        raise KeyError(f"Unsupported browser '{browser}'")


@pytest.fixture(scope="session")
def environment(request: pytest.FixtureRequest) -> str:
    environment = request.config.getoption("--env")

    for env in Environment:
        if environment.lower() == env.value:
            return env.value
    else:
        raise KeyError(f"Unsupported environment '{environment}'")


@pytest.fixture(scope="function", autouse=True)
def driver(browser):
    try:
        if browser == Browser.CHROME.value:
            driver = webdriver.Chrome()
            driver.maximize_window()
        elif browser == Browser.CHROME_HEADLESS.value:
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--headless=new")
            driver = webdriver.Chrome(options=chrome_options)
        elif browser == Browser.FIREFOX.value:
            driver = webdriver.Firefox()
            driver.maximize_window()
        elif browser == Browser.FIREFOX_HEADLESS.value:
            firefox_options = FirefoxOptions()
            firefox_options.add_argument("--headless")
            driver = webdriver.Firefox(options=firefox_options)
        elif browser == Browser.SAFARI.value:
            driver = webdriver.Safari()
            driver.maximize_window()
        elif browser == Browser.EDGE.value:
            driver = webdriver.Edge()
            driver.maximize_window()
        else:
            sys.exit()

        yield driver
        driver.quit()
    except SystemExit as e:
        error(f"SystemExit: an error occurred.\n{str(e)}")
