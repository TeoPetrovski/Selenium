# qawa ☕

`qawa` stands for `QA Web Automation.`

It is a `template project` based on the [pytest framework](https://docs.pytest.org/en/7.2.x/) and [Selenium](https://www.selenium.dev/) that will help you quickly start writing maintainable UI tests for your web projects.

## Contents

- [Setup](#-setup)
  - [Virtual environment](#virtual-environment)
  - [Dependencies](#dependencies)
  - [Pre-commit hook](#pre-commit-hook)
  - [Drivers](#drivers)
- [Project structure](#-project-structure)
- [Minimum setup for running tests](#-minimum-setup-for-running-tests)
- [Test setup](#-test-setup)
- [Interface for specifying options](#-interface-for-specifying-options)
- [Running tests](#-running-tests)
- [Parallel run](#-parallel-run)


## 🔧 Setup

After cloning the repository, navigate to the project root and do the following:

### Virtual environment

Create virtual environment:

````
python3 -m venv venv
````

Activate virtual environment:

````
source venv/bin/activate
````

### Dependencies

Install dependencies specified in the `requirements.txt` file:

````
pip install -r requirements.txt
````

### Pre-commit hook

Install the [pre-commit](https://pre-commit.com/) hook:

````
pre-commit install
````

Run pre-commit manually on all files:

````
pre-commit run --all-files
````

### Drivers

Documentation and download links:

* [ChromeDriver](https://chromedriver.chromium.org/) (or `brew install chromedriver`)
* [geckodriver](https://github.com/mozilla/geckodriver/releases) (or `brew install geckodriver`)
* [safaridriver](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari) (you have to enable `Allow Remote Automation` in Safari's settings)
* [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) (extract the `msedgedriver` executable to `/usr/local/bin`)

## 🧱 Project structure

The project is structured using the `page object pattern`.

### Root

* `conftest.py`
  * Used to define configuration fixtures and hooks available throughout the entire project.

* `pytest.ini`
  * Contains configuration values that are applied to all test runs. It is the primary _pytest_ configuration file that allows you to change default behavior (e.g., the log level and report configurations).
  * Markers used on tests should be defined in `pytest.ini`. If registered, they are listed when the `pytest --markers` command is run.

* `requirements.txt`
  * Contains project dependencies.

For more info on `conftest.py` and `fixtures` check the [pytest documentation](https://docs.pytest.org/en/7.2.x/how-to/fixtures.html).


### Main packages

* `core`
  * `base_page.py`
    * Base class containing base methods that should be inherited by all page objects.
  * `constants.py`
    * Project configuration constants.
  * `plugins.py`
    * Contains plugins integrated into the project.

* `pages`
    * Contains page classes.
    * Every page class should inherit from the `BasePage` class which is defined in `base_page.py`.

* `tests`
    * Contains the tests.
    * Contains an optional `conftest.py` file with hooks and fixtures used only in tests.

* `utilities`
    * Should be used for test data, helper methods, etc.

* `reports`
  * Contains generated reports and screenshots.


## 🪛 Minimum setup for running tests

1. Update the following in `core/constants.py`:
   * `URLS` in the `Environment` class.
     * Should match the URLs used in your project
   * `TIMEOUT` in the `Driver` class.
     * You can adjust the timeout according to your project needs.
2. Update the following in `core/plugins/html_report/plugin.py`:
   * `REPORT_NAME`
   * `COMMON_URL`
3. Create a page object class extending `BasePage` in the `pages` directory.
4. Create a test class in the `tests` directory.
5. Run the test suite: `python3 -m pytest`.


## 🔨 Test setup

In order to be automatically discovered by `pytest`:
* All test methods must be prefixed with `test_`.
* All test `.py` files must be prefixed with `test_` (example: `test_blog.py`).
* All test classes within `test_*.py` files must be prefixed with `Test` (example: _TestBlog_).

Test methods within a test class should have the following arguments: `self`, `extra`.

Example: `def test_navigate_to_blog_page(self, extra)`
* `extra` is a [pytest-html](https://pytest-html.readthedocs.io/en/latest/user_guide.html) fixture used to append data (e.g., images) to the HTML report. It has to be used within a test method only if the `save_screenshot` method is used.


## ⚙ Interface for specifying options

### Optional arguments

* The default environment is `dev`, however you can specify a different one using the `env` argument:
    * `--env=prod`

* The default browser is `Chrome`. Other supported browsers include:
    * `--browser=chrome-headless`
    * `--browser=firefox`
    * `--browser=safari`
    * `--browser=edge`

* Use the `-m` argument to specify the test run scope. For the markers to work, you have to decorate the test with the appropriate _mark_ (see `test_blog.py`).
  * Single marker:
    * `-m=smoke`
  * Multiple markers:
    * `-m="smoke and regression"`

* You can create additional custom command-line arguments by adding them to the `pytest_addoption` hook in `conftest.py`.

* HTML reports are generated by default (defined in the `pytest.ini` file) once test run is finished.
  * This includes HTML report, Slack and Xray (Jira plugin) payloads.


## ⭐ Running tests

Arguments:

* You can **omit** optional arguments from the run command if you want to use the default values set in `conftest.py`.
* You can **omit** the scope argument `tests` when running all tests


Run all tests in a test file:

````
python3 -m pytest tests/blog/test_blog.py --browser=firefox --env=dev
````

Run all tests in a class:

````
python3 -m pytest tests/blog/test_blog.py::TestBlog --browser=firefox --env=dev
````

Run all tests in a directory:

````
python3 -m pytest tests/blog
````

Run a single test:

````
python3 -m pytest tests/blog/test_blog.py::TestBlog::test_navigate_to_blog_page_example_one
````

Run tests marked `smoke`:

````
python3 -m pytest -m=smoke
````

Run tests with multiple markers:

````
python3 -m pytest -m="smoke and regression"
````


## 🌟 Parallel run

The [pytest-xdist](https://pypi.org/project/pytest-xdist/) plugin is used to extend pytest with additional test execution modes.

`pytest-xdist` options for parallel test run:
* `-n 2`
  * Specifies the usage of two workers (browser windows).


### Running tests in parallel (2+ browser windows)

Run all tests on four Chrome browser windows:

````
python3 -m pytest --browser=chrome -n 4
````

Run all tests in the `test_blog.py` module on two Firefox browser windows:

````
python3 -m pytest --browser=firefox -n 2 tests/blog/test_blog.py
````

## Wiki

For additional information on the project, please check the [Wiki](https://github.com/infinum/qawa/wiki).


##
<p align="center">
  <img src="/img/infinum-logo.png" alt="infinum-logo.png" width="300">
</p>
