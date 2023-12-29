"""Example page class"""
from selenium.webdriver.common.by import By

from src.qawa.core.base_page import BasePage


class BlogPage(BasePage):
    """Blog page locators"""

    slug = "/blog"
    _blog_name_label_locator = (By.CLASS_NAME, "blog-intro__heading")

    def go_to_page(self):
        self.go_to(self.slug)

    @property
    def blog_name_label(self):
        return self.get_present_element(self._blog_name_label_locator)

    def wait_for_blog_page_to_load(self):
        self.wait_until_element_visible(self._blog_name_label_locator)
