import traceback

from base.selenium_driver import SeleniumDriver
from utilities.util import Util
from utilities.custom_logger import customLogger
import logging


class Basepage(SeleniumDriver):
    log = customLogger(logLevel=logging.DEBUG)

    def __init__(self, driver):
        """
        Base page inherites from the selenium driver which takes care of all the operations related to selenium driver
        So further we can just inherit this Base page into all our prages so we can have both the functionality
        :param driver:
        """
        super().__init__(driver)
        self.driver = driver
        self.util = Util()  # Creation of util object inorder to use utility functions anywhere in classes which is extending this class ex:any pages class

    def verifyPageTitle(self, textToVerify):
        """
        Verify the title of the webpage

        :param textToVerify:Title on the page that needs to be verified
        :return:boolean
        """
        try:
            actualTitle = self.getTitle()
            return self.util.verifyTextContains(actualTitle, textToVerify)
        except:
            self.log.error("Failed to get the page title")
            traceback.print_stack()
            return False
