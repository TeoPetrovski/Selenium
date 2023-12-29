"""Example of conftest.py on the tests level.
Here you can define fixtures needed in every test, such as before and after hooks.
Additional conftest.py files can be put in each of the tests sub-folders.
https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files

These fixtures can be called on a test and/or on a class level.
They can also be called automatically with "autouse" option (autouse=True).

To call a fixture on a class level, use the `@pytest.mark.usefixtures` decorator above the class definition:

    @pytest.mark.usefixtures("open_homepage")
    class TestBlog:

To call it on a test level, provide the fixture as an argument in the test function:

    def test_navigate_to_blog_page(self, extra, open_homepage):

You can also provide the fixture as an argument in the `set_up` fixture to avoid calling it in every test:

    @pytest.fixture(scope="function", autouse=True)
    def set_up(self, driver, environment, open_homepage):
"""
import pytest

from src.qawa.pages.home.home_page import HomePage


@pytest.fixture(scope="function")
def get_test_name(request):
    """Returns the name of the current test."""
    return request.node.name


@pytest.fixture(scope="function")
def get_test_class_name(request):
    """Returns the name of the current test class."""
    return request.node.parent.name


@pytest.fixture(scope="function")
def open_homepage(driver, environment):
    """Opens the home page."""
    home_page = HomePage(driver, environment)

    home_page.go_to_page()
