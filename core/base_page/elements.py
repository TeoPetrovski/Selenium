from logging import error

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from core.constants import Driver


class Elements:
    """The class handles getting page elements."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def get_present_element(self, locator: tuple, timeout=Driver.TIMEOUT) -> WebElement:
        condition = expected_conditions.presence_of_element_located
        return self._get_element(locator, condition, timeout)

    def get_visible_element(self, locator: tuple, timeout=Driver.TIMEOUT) -> WebElement:
        condition = expected_conditions.visibility_of_element_located
        return self._get_element(locator, condition, timeout)

    def get_clickable_element(self, locator: tuple, timeout=Driver.TIMEOUT) -> WebElement:
        condition = expected_conditions.element_to_be_clickable
        return self._get_element(locator, condition, timeout)

    def get_invisible_element(self, locator: tuple, timeout=Driver.TIMEOUT) -> WebElement:
        condition = expected_conditions.invisibility_of_element_located
        return self._get_element(locator, condition, timeout)

    def get_present_elements(self, locator: tuple, timeout=Driver.TIMEOUT) -> list[WebElement]:
        condition = expected_conditions.presence_of_all_elements_located
        return self._get_elements(locator, condition, timeout)

    def _get_element(self, locator: tuple, condition, timeout: int) -> WebElement:
        """Returns the element matching the locator.

        Params:
            locator: tuple storing locator strategy and value
            condition: condition expected to be met
            timeout: number of seconds to wait
        """
        try:
            element: WebElement = WebDriverWait(self.driver, timeout).until(condition(locator))
            return element
        except Exception as e:
            error(f"Getting locator '{locator}' until '{condition.__name__}' failed!\n{str(e)}")

    def _get_elements(self, locator: tuple, condition, timeout: int) -> list[WebElement]:
        """Returns a list of elements matching the locator.

        Params:
            locator: tuple storing locator strategy and value
            condition: condition expected to be met
            timeout: number of seconds to wait
        """
        try:
            elements: [WebElement] = WebDriverWait(self.driver, timeout).until(condition(locator))
            return elements
        except Exception as e:
            error(f"Getting locator '{locator}' until '{condition.__name__}' failed!\n{str(e)}")

    def wait_until_element_present(self, locator: tuple, timeout=Driver.TIMEOUT):
        condition = expected_conditions.presence_of_element_located
        self._wait_until(locator, condition, timeout)

    def wait_until_element_visible(self, locator: tuple, timeout=Driver.TIMEOUT):
        condition = expected_conditions.visibility_of_element_located
        self._wait_until(locator, condition, timeout)

    def wait_until_element_clickable(self, locator: tuple, timeout=Driver.TIMEOUT):
        condition = expected_conditions.element_to_be_clickable
        self._wait_until(locator, condition, timeout)

    def wait_until_element_invisible(self, locator: tuple, timeout=Driver.TIMEOUT):
        condition = expected_conditions.invisibility_of_element_located
        self._wait_until(locator, condition, timeout)

    def wait_until_title_matches(self, title: str, timeout=Driver.TIMEOUT):
        condition = expected_conditions.title_is(title)
        WebDriverWait(self.driver, timeout).until(condition)

    def _wait_until(self, locator: tuple, condition, timeout: int):
        """Waits for the locator until condition is met before timing out.

        Params:
            locator: tuple storing locator strategy and value
            condition: condition expected to be met
            timeout: number of seconds before timing out
        """
        try:
            WebDriverWait(self.driver, timeout).until(condition(locator))
        except Exception as e:
            error(f"Waiting for '{locator}' until '{condition.__name__}' timed out!\n{str(e)}")
