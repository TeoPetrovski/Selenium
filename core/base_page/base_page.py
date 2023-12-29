import sys

from selenium.webdriver.remote.webdriver import WebDriver

from core.base_page.actions import Actions
from core.base_page.elements import Elements
from core.constants import Environment


class BasePage(Actions, Elements):
    """The base page that is inherited by all pages."""

    def __init__(self, driver: WebDriver, environment: str):
        super().__init__(driver)
        self.environment = environment

    def navigate(self, url_slug):
        if self.environment in Environment.URLS.keys():
            base_url = Environment.URLS[self.environment]
            self.driver.get(f"{base_url}{url_slug}")
        else:
            sys.exit("Environment not defined!")
