![Github-QAWA](https://github.com/infinum/qawa/assets/68659776/0a7742e2-9f14-433a-9e5a-d79d9d8a3f1a)

# ☕ QAWA

`QAWA` stands for `Quality Assurance Web Automation.`

It is a test automation framework based on [pytest](https://docs.pytest.org/en/7.2.x/) and [Selenium](https://www.selenium.dev/). With QAWA you can quickly start writing maintainable UI tests for your web projects.

## 📔 Contents

- [Setup](#-setup)
  - [Virtual environment](#virtual-environment)
  - [Dependencies](#dependencies)
  - [Pre-commit hook](#pre-commit-hook)
  - [Drivers](#drivers)
- [Project structure](#-project-structure)
- [Minimum setup for running tests](#-minimum-setup-for-running-tests)
- [Test setup](#-test-setup)
- [Command-line arguments](#-command-line-arguments)
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

Install pip-tools:

````
python -m pip install pip-tools
````

Generate the `requirements.txt` containing the dependencies specified in the `pyproject.toml` file:

````
pip-compile pyproject.toml
````

Install the dependencies:

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

The following browsers are supported: Chrome, Firefox, Safari, Edge

Documentation and download links:

* [ChromeDriver](https://chromedriver.chromium.org/) (or `brew install chromedriver`)
* [geckodriver](https://github.com/mozilla/geckodriver/releases) (or `brew install geckodriver`)
* [safaridriver](https://developer.apple.com/documentation/webkit/testing_with_webdriver_in_safari) (you have to enable `Allow Remote Automation` in Safari's settings)
* [Microsoft Edge WebDriver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) (extract the `msedgedriver` executable to `/usr/local/bin`)


## 🧱 Project structure

The project is structured using the `page object pattern`.


### Root

* `pre-commit-config.yaml`
  * Contains pre-commit configuration.


* `pyproject.toml`
  * Contains project details and requirements used to build the package.
  * Contains pytest configuration that allows you to change default behavior (e.g., the log level and report configurations), applied to entire test run.
  * Markers used on tests should be defined in `pyproject.toml`. If registered, they are listed when the `pytest --markers` command is run.

* `src/qawa`
  * Contains the source code.

### src/qawa

* `conftest.py`
  * Used to define configuration fixtures and hooks available throughout the entire project.
  * For more info on `conftest.py` and `fixtures` check the [pytest documentation](https://docs.pytest.org/en/7.2.x/how-to/fixtures.html).

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

* `reports`
  * Contains generated reports and screenshots.

* `utilities`
    * Should be used for test data, helper methods, etc.


## 🪛 Minimum setup for running tests

1. Update the following info in `core/constants.py` to match your project and your needs:
   * `Environment`, `EnvironmentUrl` and `EnvironmentApiUrl` class.
   * Timeouts in the `Timeout` class.
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
* All test classes within `test_*.py` files must be prefixed with `Test` (example: `TestBlog`).

### Extra

You should pass the `extra` argument to a test function if you want to take screenshots within a test.
* The `extras` fixture uses `extra` to append data to the report object.
* It has to be passed as an argument to a test method so that it can be then used as an argument in the `save_screenshot`.

Example:
```python
def test_go_to_blog_page(self, extra):
    self.home_page.blog_navigation_button.click()
    self.blog_page.save_screenshot(extra)
```

For more details on `extras` check the [pytest-html](https://pytest-html.readthedocs.io/en/latest/user_guide.html) documentation.


## 💻 Command-line arguments

You can use the command-line to specify which tests to run and which browser to use.
By default, the tests are run in Chrome (headful mode) on development environment, as set in `conftest.py`.

You can create custom command-line arguments by adding them to the `pytest_addoption` hook in `conftest.py`.

When running the tests:
* You can **omit** the arguments from the run command if you want to use the default values.
* You can **omit** the argument `tests` when running all tests.


### Browser

Use the `--browser` argument to specify the browser:
  * `--browser=chrome` (default)
  * `--browser=chrome-headless`
  * `--browser=firefox`
  * `--browser=firefox-headless`
  * `--browser=safari`
  * `--browser=edge`

### Environment

Use the `--env` argument to specify the environment:
  * `--env=dev`
  * `--env=prod` (default)

### Scope

Use the `-m` argument to specify the test run scope. Decorate the test with the appropriate _mark_ to include it in the scope (see `test_blog.py`).
  * Single marker:
    * `-m=smoke`
  * Multiple markers:
    * `-m="smoke and regression"`


## 🏃 Running tests

Make sure you are positioned in the `src/qawa` directory.

Run all tests in a directory:

````
python3 -m pytest tests/blog
````

Run all tests in a test file:

````
python3 -m pytest tests/blog/test_blog.py --browser=firefox --env=dev
````

Run all tests in a class:

````
python3 -m pytest tests/blog/test_blog.py::TestBlog --browser=firefox --env=dev
````

Run a single test:

````
python3 -m pytest tests/blog/test_blog.py::TestBlog::test_navigate_to_blog_page_example_one
````

Run all tests marked `smoke` (single marker):

````
python3 -m pytest -m=smoke
````

Run all tests marked `smoke` and `regression` (multiple markers):

````
python3 -m pytest -m="smoke and regression"
````


## 🏃🏃 Parallel run

The [pytest-xdist](https://pypi.org/project/pytest-xdist/) plugin is used to extend pytest with additional test execution modes.

Use the `-n` argument to specify number of workers for parallel execution:
* `-n 2`


### Running tests in parallel (2+ browser windows)

Run all tests on four Chrome browser windows:

````
python3 -m pytest -n 4 --browser=chrome
````

Run all tests in specific module on two Firefox browser windows:

````
python3 -m pytest -n 2 --browser=firefox tests/blog/test_blog.py
````

## 📈 Test report

HTML report is generated by default once test run is finished.
Slack and Xray (Jira plugin) payloads are also generated.

The files are stored in the `src/qawa/reports` directory.


## 📚 Wiki

For additional information on the project, please check the [Wiki](https://github.com/infinum/qawa/wiki).


##
<p align="center">
  <img src="https://github.com/infinum/qawa/assets/68659776/704652a8-fc95-489d-ae5a-2940f62716d4" alt="infinum-logo.png" width="300">
</p>
