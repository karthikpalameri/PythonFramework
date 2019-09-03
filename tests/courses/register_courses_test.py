import inspect
import logging

import pytest

from pages.courses.register_courses_page import RegisterCoursesPages
from utilities import custom_logger as cl
from utilities.resultstatustracker import ResultStatusTracker
from pages.home.login_page import LoginPage
from ddt import ddt, data, unpack  # Step1:Need these decorator to implement data driven test-cases
import unittest

@ddt  # Step2: @ddt decorator should be put before
@pytest.mark.usefixtures("oneTimeSetup", "setUp")

class TestRegisterCoursesTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def objectSetup(self):
        self.rc = RegisterCoursesPages(self.driver)
        self.lp = LoginPage(self.driver)
        self.ts = ResultStatusTracker(self.driver)

    @pytest.mark.run(order=1)
    @data(("Selenium WebDriver With Java", "3434 343434 34343", "2345", "12345", "United States","12345"),("Selenium WebDriver With Java", "5555 343434 34343", "2345", "99999", "India","88888"))  # Step 3: @data decorator should be used to pass the data
    @unpack  # Step 4: If the above is list , tuple then use @unpack decorator to unpack them to below variables which are passed as parameter for function

    def test_invalidEnrollment(self, course_name, card_number, card_exp_date, card_cvc, card_country,card_postal_code):
        self.driver.get(self.baseUrl)
        self.lp.login("test@email.com", "abcabc")
        result1 = self.lp.verifyLoginSuccessful()
        self.ts.mark(result1, " login verification", testName=inspect.stack()[0][3])

        self.rc.enrollCourse(course_name, card_number, card_exp_date, card_cvc, card_country,
                             card_postal_code)
        result2 = self.rc.verifyEnrollFailed("The card was declined.")
        self.ts.markFinal(result2, " Enrollment verification", testName=inspect.stack()[0][3])

    # @pytest.mark.run(order=1)
    # def test_invalidEnrollment(self):
    #     self.driver.get(self.baseUrl)
    #     self.lp.login("test@email.com", "Zabcabc")
