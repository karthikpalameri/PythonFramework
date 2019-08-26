import inspect
import logging

import pytest

from pages.courses.register_courses_page import RegisterCoursesPages
from utilities import custom_logger as cl
from utilities.teststatus import TestStatus
from pages.home.login_page import LoginPage

@pytest.mark.usefixtures("oneTimeSetup", "setUp")
class TestRegisterCoursesTest():
    @pytest.fixture(autouse=True)
    def objectSetup(self):
        self.rc = RegisterCoursesPages(self.driver)
        self.lp=LoginPage(self.driver)
        self.ts = TestStatus(self.driver)


    @pytest.mark.run(order=1)
    def test_invalidEnrollment(self):
        self.driver.get(self.baseUrl)
        self.lp.login("test@email.com", "abcabc")
        result1 = self.lp.verifyLoginSuccessful()
        self.ts.mark(result1, " login verification", testName=inspect.stack()[0][3])

        self.rc.enrollCourse("Selenium WebDriver With Java", "6" * 16, "2345", "12345", "United States", "12345")
        result2=self.rc.verifyEnrollFailed("The card was declined.")
        self.ts.markFinal(result2, " Enrollment verification", testName=inspect.stack()[0][3])