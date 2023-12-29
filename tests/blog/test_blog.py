"""Example test class"""
from logging import info

import pytest
import pytest_check as check

from core.base_api import BaseApi
from core.plugins.html_report.plugin import save_url
from pages.blog.blog_page import BlogPage
from pages.home.home_page import HomePage
from utilities.api.endpoints import Endpoint


class TestBlog:
    """Blog tests"""

    @pytest.fixture(scope="function", autouse=True)
    def set_up(self, driver, environment):
        """Initializes pages used in the tests.
        Can be used to set up variables and perform actions used in test.
        """
        self.base_api = BaseApi(environment)
        self.blog_page = BlogPage(driver, environment)
        self.home_page = HomePage(driver, environment)

        self.home_page.navigate_to_page()

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.xray(["ID-123"])
    def test_navigate_to_blog_page_example_one(self, extra):
        """Test with soft asserts.
        Failing asserts do not stop test run but are evaluated at the end.
        """
        info("Verifies that the blog title is correct.")
        save_url(extra, ["ID-123"])

        # API request example.
        # You can create or update necessary data and configurations as a prerequisite for UI tests in a similar way.
        response = self.base_api.get_page_response(Endpoint.BLOG)
        assert 200 <= response.status_code < 300

        self.home_page.blog_navigation_button.click()
        self.blog_page.wait_for_blog_page_to_load()

        check.equal(self.blog_page.blog_name_label.text, "Random invalid name")
        check.equal(self.blog_page.blog_name_label.text, "Typing as we speak")

    @pytest.mark.smoke
    @pytest.mark.xray(["ID-456", "ID-789"])
    def test_navigate_to_blog_page_example_two(self, extra):
        """Test with hard assert."""
        info("Verifies that the blog title is correct.")
        save_url(extra, ["ID-456", "ID-789"])

        self.home_page.blog_navigation_button.click()
        self.blog_page.wait_for_blog_page_to_load()

        assert self.blog_page.blog_name_label.text == "Typing as we speak"
