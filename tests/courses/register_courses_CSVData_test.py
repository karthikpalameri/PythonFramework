import inspect
import logging

import pytest

from pages.courses.register_courses_page import RegisterCoursesPages
from utilities import custom_logger as cl
from utilities.resultstatustracker import ResultStatusTracker
from pages.home.login_page import LoginPage
from ddt import ddt, data, unpack  # Step1:Need these decorator to implement data driven test-cases
import unittest
from utilities.read_write_data import getCsvData


@ddt  # Step2: @ddt decorator should be put before
@pytest.mark.usefixtures("oneTimeSetup", "setUp")
class TestRegisterCoursesCSVDataTest(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def objectSetup(self):
        self.rc = RegisterCoursesPages(self.driver)
        self.lp = LoginPage(self.driver)
        self.ts = ResultStatusTracker(self.driver)

    # @pytest.mark.run(order=1)
    # @data(*getCsvData(filename="/Users/karthikp/PycharmProjects/PythonFramework/resources/testdata.csv"))  # Step 3: @data decorator should be used to pass the data
    # @unpack  # Step 4: If the above is list , tuple then use @unpack decorator to unpack them to below variables which are passed as parameter for function
    # def test_invalidEnrollment(self, course_name, card_number, card_exp_date, card_cvc, card_country, card_postal_code):
    #     self.driver.get(self.baseUrl)
    #     self.lp.login("test@email.com", "abcabc")
    #     result1 = self.lp.verifyLoginSuccessful()
    #     self.ts.mark(result1, " login verification", testName=inspect.stack()[0][3])
    #
    #     self.rc.enrollCourse(course_name, card_number, card_exp_date, card_cvc, card_country,
    #                          card_postal_code)
    #     result2 = self.rc.verifyEnrollFailed("The card was declined.")
    #     self.ts.markFinal(result2, " Enrollment verification", testName=inspect.stack()[0][3])

    @pytest.mark.run(order=1)
    @data(*getCsvData(filename="/Users/karthikp/PycharmProjects/PythonFramework/resources/login_testdata.csv"))
    @unpack
    def test_invalidEnrollment(self, username, password):
        self.driver.get(self.baseUrl)
        self.lp.login(username, password)
        self.lp.logout()
