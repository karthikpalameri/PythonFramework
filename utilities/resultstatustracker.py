"""
teststatus to keep track of each validation and proceed further if it fails in the process


"""
import inspect

from base.selenium_driver import SeleniumDriver
import logging
from utilities.custom_logger import customLogger as cl


class ResultStatusTracker(SeleniumDriver):
    log = cl(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.resultList = []

    def setResult(self, result, resultMessage, testName):
        """
        appending the result status/assert status  to the list
        so it can be verified at the end

        :param result:
        :param resultMessage:
        :return: None
        """

        try:
            if result is not None:
                if result:  # we are not writing is True , the result value will be always True or False
                    self.resultList.append("PASS")
                    self.log.info("### VERIFICATION SUCCESSFUL :: {}".format(resultMessage))
                else:
                    self.resultList.append("FAIL")
                    self.log.error("### VERIFICATION FAILED :: {}".format(resultMessage))
                    self.saveScreenShot(testName, resultMessage)

            else:
                self.resultList.append("FAIL")
                self.log.error("### VERIFICATION FAILED :: {}".format(resultMessage))
                self.saveScreenShot(testName, resultMessage)

        except:
            self.resultList.append("FAIL")
            self.log.error("### Exception Occured!!!")
            self.saveScreenShot(testName, resultMessage)

    def mark(self, result, resultMessage, testName):
        """
        Mark the result of the verification point in a test case
        :param testName:
        :param result:
        :param resultMessage:
        :return:
        """
        self.setResult(result, resultMessage, testName)

    def markFinal(self, result, resultMessage, testName):
        """
        Mark the result of the verification point in a test case
        This needs to be called at least once in a test case
        This should be the final test status of the test case
        :param testName:
        :param result:
        :param resultMessage:
        :return: None
        """
        self.setResult(result, resultMessage, testName)

        if "FAIL" in self.resultList:
            self.log.error(testName + "<---### TEST FAILED")
            self.resultList.clear()
            assert True == False

        else:
            self.log.error(testName + "<---### TEST PASSED")
            self.resultList.clear()
            assert True == True
