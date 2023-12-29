import time
from logging import error

from pytest_html import extras
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from core.plugins.html_report.plugin import SCREENSHOT_DIR


class Actions:
    """The class handles actions performed on page elements."""

    def __init__(self, driver: WebDriver):
        self.driver = driver

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
