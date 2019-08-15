import pytest
import argparse

from selenium import webdriver

"""
conftest.py file is used to write the common setup and tear down code 
you can specifiy scope like package module fuction class
"""


@pytest.yield_fixture()
def setUp():
    print()
    print("-" * 60)
    print("Running conftest setup before every METHOD specified ")
    print("-" * 60)
    yield
    print()
    print("-" * 60)
    print("Running conftest tearDown before every METHOD specified")
    print("-" * 60)


# scope can be function , module , package , session
@pytest.yield_fixture(scope="class")
def oneTimeSetup(request, command_line_browser):
    """
    passing fixture name inside another fixture is possible
    we are calling another function 'command_line_browser' before executing oneTimeSetup
    """
    print()
    print("*" * 60)
    print("Running conftest oneTimeSetup before every CLASS as specified")
    if command_line_browser == 'firefox':
        print("%" * 60)
        print("Running tests in Firefox as it is passed as command line argument..")
        baseUrl = 'https://learn.letskodeit.com/p/practice'
        driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
        driver.maximize_window()
        driver.implicitly_wait(10)
        print("%" * 60)
    else:
        print("%" * 60)
        print("Running tests in Chrome as it is passed as command line argument..")
        baseUrl = 'https://learn.letskodeit.com/p/practice'
        driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
        driver.maximize_window()
        driver.implicitly_wait(10)
        print("%" * 60)
    print("*" * 60)
    if request.cls is not None:
        request.cls.value = driver

    yield driver
    print("*" * 60)
    print("Running conftest oneTimeTearDown before every CLASS as specified")
    driver.quit()
    print("*" * 60)


@pytest.yield_fixture(scope="class")
def privateOneTimeSetup():
    print()
    print("!" * 60)
    print("Running conftest privateOneTimeSetup..")
    print("!" * 60)
    print()
    yield
    print()
    print("!" * 60)
    print("Running conftest privateOneTimeTearDown..")
    print("!" * 60)
    print()


def pytest_addoption(parser):
    print()
    print("=" * 60)
    parser.addoption("--browser", help="input browser name")
    print("=" * 60)


@pytest.fixture(scope="session")
def command_line_browser(request):
    return request.config.getoption("--browser")
