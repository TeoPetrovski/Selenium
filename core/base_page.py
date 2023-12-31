import sys
import time
from logging import error

from pytest_html import extras
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from core.constants import Driver, Environment
from core.plugins.html_report.plugin import SCREENSHOT_DIR


class BasePage:
    """The base page that is inherited by all pages."""

    def __init__(self, driver: WebDriver, environment: str):
        self.driver = driver
        self.environment = environment

    def navigate(self, url_slug):
        if self.environment in Environment.URLS.keys():
            base_url = Environment.URLS[self.environment]
            self.driver.get(f"{base_url}{url_slug}")
        else:
            sys.exit("Environment not defined!")

    # GETTING ELEMENT(S)
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

    # WAITING FOR ELEMENT
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

    # INTERACTING WITH ELEMENTS
    def hover_over_element(self, element: WebElement):
        try:
            action = ActionChains(self.driver)
            action.move_to_element(element).perform()
        except Exception as e:
            error(f"Hovering on '{element}' failed!\n{str(e)}")

    def drag_and_drop(self, start_element: WebElement, end_element: WebElement):
        try:
            action = ActionChains(self.driver)
            action.click_and_hold(start_element).move_by_offset(10, 0).release(end_element).perform()
        except Exception as e:
            error(f"Dragging '{start_element}' failed!\n{str(e)}")

    def browser_go_back(self):
        try:
            self.driver.execute_script("window.history.go(-1)")
        except Exception as e:
            error(f"Going back failed!\n{str(e)}")

    def scroll_to_element(self, element: WebElement):
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
        except Exception as e:
            error(f"Scrolling to {element} failed!\n{str(e)}")

    def set_local_storage_key(self, key: str, value: str):
        try:
            self.driver.execute_script(f"window.localStorage.setItem({key}, {value});")
        except Exception as e:
            error(f"Setting local storage key failed!\n{str(e)}")

    # TAKING SCREENSHOT
    def save_screenshot(self, extra):
        """Takes screenshot and appends it to the HTML report.

        Params:
            extra: extra (pytest-html content object)
        """
        timestamp = str(int(time.time()))
        image_name = f"{timestamp}.png"
        image_path = f"{SCREENSHOT_DIR}/{image_name}"

        try:
            self.driver.save_screenshot(image_path)
            screenshot = self.driver.get_screenshot_as_base64()
            extra.append(extras.image(screenshot))
        except Exception as e:
            error(f"Saving screenshot failed!\n{str(e)}")
