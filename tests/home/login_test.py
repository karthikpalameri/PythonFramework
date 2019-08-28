import inspect
import logging

import pytest

from pages.home.login_page import LoginPage
from utilities import custom_logger as cl
from utilities.resultstatustracker import ResultStatusTracker


@pytest.mark.usefixtures("oneTimeSetup", "setUp")
class TestLoginTests():
    log = cl.customLogger(logLevel=logging.DEBUG)

    @pytest.fixture(autouse=True)
    def classSetup(self, oneTimeSetup):
        """
        classSetup is a custom fixture written here and not is conftest
        onTimeSetup and setUp fixtures will not be called first as none of them are passed as arguments for classSetup function
        it is just a fixture which will act as a constructor and initializes the class whichever we want and makes it available to all the functions
        :return:
        """
        print("inside classsetuppp")
        self.lp = LoginPage(self.driver)
        self.ts = ResultStatusTracker(self.driver)

    @pytest.mark.run(order=1)
    def test_validLogin(self):
        self.log.debug("test_invalidLogin scenario executing..")
        self.driver.get(self.baseUrl)
        self.lp.login("test@email.com", "abcabc")
        result = self.lp.verifyLoginSuccessful()
        self.ts.markFinal(result, "valid login verification", testName=inspect.stack()[0][3])

    @pytest.mark.karthik
    @pytest.mark.run(order=2)
    def test_invalidLogin(self):
        self.log.debug("test_validLogin scenario executing..")
        self.lp.login("test@email.com", "abcabcxyz")
        result1 = self.lp.verifyLoginTitle()
        self.ts.mark(result1, "Title verification ",testName=inspect.stack()[0][3])
        result2 = self.lp.verifyLoginFailed()
        self.ts.markFinal(result2, "InValid login verification", testName=inspect.stack()[0][3])
