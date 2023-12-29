"""Example test class"""
from logging import info

import pytest
import pytest_check as check

from src.qawa.core.base_api import BaseApi
from src.qawa.core.plugins.html_report.plugin import save_url
from src.qawa.pages.blog.blog_page import BlogPage
from src.qawa.pages.home.home_page import HomePage
from src.qawa.utilities.api.endpoints import Endpoint


@pytest.mark.usefixtures("open_homepage")
class TestBlog:
    """Blog tests"""

    @pytest.fixture(scope="function", autouse=True)
    def set_up(self, driver, environment):
        """Initializes pages used in the tests.
        Can be used to set up variables and perform actions used in tests.
        """
        self.base_api = BaseApi(environment)
        self.blog_page = BlogPage(driver, environment)
        self.home_page = HomePage(driver, environment)

    @pytest.mark.smoke
    @pytest.mark.regression
    @pytest.mark.xray(["ID-123"])
    def test_navigate_to_blog_page_example_one(self, extra):
        """Test with soft asserts.
        Failed asserts will not stop test execution.
        """
        info("Verify that the blog title is correct.")
        save_url(extra, ["ID-123"])

        # API request example.
        # You can create or update necessary data and configurations as a prerequisite for UI tests in a similar way.
        response = self.base_api.get_page_response(Endpoint.BLOG)
        assert 200 <= response.status_code < 300

        self.home_page.blog_navigation_button.click()
        self.blog_page.wait_for_blog_page_to_load()

        check.equal(self.blog_page.blog_name_label.text, "Random invalid name")  # Expected to fail
        check.equal(self.blog_page.blog_name_label.text, "Typing as we speak")  # Expected to pass
        self.blog_page.save_screenshot(extra)

    @pytest.mark.smoke
    @pytest.mark.xray(["ID-456", "ID-789"])
    def test_navigate_to_blog_page_example_two(self, extra):
        """Test with hard assert."""
        info("Verify that the blog title is correct.")
        save_url(extra, ["ID-456", "ID-789"])

        self.home_page.blog_navigation_button.click()
        self.blog_page.wait_for_blog_page_to_load()

        assert self.blog_page.blog_name_label.text == "Typing as we speak"
        self.blog_page.save_screenshot(extra)
