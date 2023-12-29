"""Example page class"""
from selenium.webdriver.common.by import By

from core.base_page.base_page import BasePage


class BlogPage(BasePage):
    """Blog page locators"""

    slug = "/blog"
    _blog_name_label_locator = (By.CLASS_NAME, "blog-intro__heading")

    def navigate_to_page(self):
        self.navigate(self.slug)

    @property
    def blog_name_label(self):
        return self.get_present_element(self._blog_name_label_locator)

    def wait_for_blog_page_to_load(self):
        self.wait_until_element_visible(self._blog_name_label_locator)
