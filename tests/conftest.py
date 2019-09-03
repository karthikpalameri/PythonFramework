import pytest
import argparse

from selenium import webdriver
from base.webdriverfactory import WebDriverFactory

"""
conftest.py file is used to write the common setup and tear down code 
you can specifiy scope like package module fuction class
"""


# def star(fun):
#     def inner(*args, **kwargs):
#         print("*" * 90)
#         fun(*args, **kwargs)
#         print("*" * 90)
#     return inner



@pytest.yield_fixture()
# @star
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
def oneTimeSetup(request, command_line_browser, base_url) -> webdriver:
    """
    passing fixture name inside another fixture is possible, so that they get executed first
    we are calling another fixture 'command_line_browser' before executing oneTimeSetup to get the browsertype
    same goes for the base_url
    """
    print()
    print("*" * 60)
    print("Running conftest oneTimeSetup before every CLASS as specified")
    wdf = WebDriverFactory(command_line_browser, base_url)
    driver = wdf.getWebDriverFactoryInstance()
    if request.cls is not None:
        request.cls.driver = driver
        request.cls.baseUrl = base_url
    print("*" * 60)

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
    parser.addoption("--os", help="input operating system name")
    print("=" * 60)


@pytest.fixture(scope="session")
def command_line_browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def command_line_os(request):
    return request.config.getoption("--os")


@pytest.fixture(scope="session")
def base_url():
    base_url = 'https://learn.letskodeit.com/p/practice'
    return base_url
