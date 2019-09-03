import unittest
from tests.home.login_test import TestLoginTests
from tests.courses.register_courses_CSVData_test import TestRegisterCoursesCSVDataTest
from tests.courses.register_courses_test import TestRegisterCoursesTest

# Get all tests from the testclasses

tc1 = unittest.TestLoader.loadTestsFromTestCase(TestLoginTests)
tc2 = unittest.TestLoader.loadTestsFromTestCase(TestRegisterCoursesCSVDataTest)
tc3 = unittest.TestLoader.loadTestsFromTestCase(TestRegisterCoursesTest)

# Create a Test Suite Combining all the test classes

smokeTest = unittest.TestSuite([tc1, tc2, tc3])

unittest.TextTestRunner(verbosity=2).run(smokeTest)
