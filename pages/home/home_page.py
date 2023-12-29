"""Example page class"""
from selenium.webdriver.common.by import By

from core.base_page import BasePage


class HomePage(BasePage):
    """Home page locators"""

    slug = ""
    _blog_navigation_button_locator = (By.XPATH, "//span[text()='Blog']")

    def navigate_to_page(self):
        self.navigate(self.slug)

    @property
    def blog_navigation_button(self):
        return self.get_present_element(self._blog_navigation_button_locator)
