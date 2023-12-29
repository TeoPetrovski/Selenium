from enum import Enum
from pathlib import Path

# ROOT DIRECTORY PATH
ROOT_DIR = Path(__file__).parent.parent


class Timeout(Enum):
    SHORT = 15
    MID = 30
    LONG = 60


class Environment(Enum):
    DEV = "dev"
    PROD = "prod"

    @property
    def base_url(self):
        match self:
            case Environment.DEV:
                return "https://beta.infinum.com"
            case Environment.PROD:
                return "https://infinum.com"

    @property
    def api_url(self):
        match self:
            case Environment.DEV:
                return "https://beta.infinum.com"
            case Environment.PROD:
                return "https://infinum.com"


class Browser(Enum):
    CHROME = "chrome"
    CHROME_HEADLESS = "chrome-headless"
    FIREFOX = "firefox"
    FIREFOX_HEADLESS = "firefox-headless"
    SAFARI = "safari"
    EDGE = "edge"
