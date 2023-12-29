"""Example page class"""
from selenium.webdriver.common.by import By

from src.qawa.core.base_page import BasePage


class HomePage(BasePage):
    """Home page locators"""

    slug = ""
    _blog_navigation_button_locator = (By.XPATH, "//span[text()='Blog']")
    _initial_loader_locator = (By.CSS_SELECTOR, "[class*='js-barba-loader-background']")

    def go_to_page(self):
        self.go_to(self.slug)
        self.wait_until_element_invisible(self._initial_loader_locator)

    @property
    def blog_navigation_button(self):
        return self.get_clickable_element(self._blog_navigation_button_locator)
