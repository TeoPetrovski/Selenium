"""Example of conftest.py on the tests level.
Here you can define fixtures needed in every test, such as before and after hooks.
Additional conftest.py files can be put in each of the tests sub-folders.
https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files

These fixtures can be called on a test and/or on a class level.
They can also be called automatically with "autouse" option (autouse=True).

To call it on a class level, use the `usefixtures` mark above the class definition:
Example:
    @pytest.mark.usefixtures("get_test_class_name")
    class TestBlog:

To call it on a test level, provide the fixture as an argument in the test function:
Example:
    def test_navigate_to_blog_page(self, extra, get_test_name):
"""
import pytest


@pytest.fixture(scope="function")
def get_test_name(request):
    """Returns the name of the current test."""
    return request.node.name


@pytest.fixture(scope="function")
def get_test_class_name(request):
    """Returns the name of the current test class."""
    return request.node.parent.name
