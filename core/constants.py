from pathlib import Path

# ROOT DIRECTORY PATH
ROOT_DIR = Path(__file__).parent.parent


class Driver:
    TIMEOUT = 30


class Environment:
    DEV = "dev"
    PROD = "prod"

    URLS = {
        DEV: "https://beta.infinum.com",
        PROD: "https://infinum.com",
    }

    API_URLS = {
        DEV: "https://beta.infinum.com",
        PROD: "https://infinum.com",
    }


class Browser:
    CHROME = "chrome"
    CHROME_HEADLESS = "chrome-headless"
    FIREFOX = "firefox"
    SAFARI = "safari"
    EDGE = "edge"
