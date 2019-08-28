import os
import traceback
from pathlib import Path
from time import strftime, localtime

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote import webelement
import utilities.custom_logger as cl
import logging


class SeleniumDriver():
    log = cl.customLogger(logLevel=logging.DEBUG)

    def __init__(self, driver):
        """
        :param driver:set driver for this class
        """
        self.driver = driver

    def getByType(self, locatorType):
        """
        Takes in locator type as userfriendly string type and finds the appropriate By type and returns it
        :param locatorType: linktext,partiallinktext,tagname,name,classname,cssselector,xpath,id
        :return:
        """
        try:
            locatorType = locatorType.lower()
            if locatorType == "id":
                return By.ID
            elif locatorType == "xpath":
                return By.XPATH
            elif locatorType == "cssselector":
                return By.CSS_SELECTOR
            elif locatorType == "name":
                return By.NAME
            elif locatorType == "classname":
                return By.CLASS_NAME
            elif locatorType == "linktext":
                return By.LINK_TEXT
            elif locatorType == "partiallinktext":
                return By.PARTIAL_LINK_TEXT
            elif locatorType == "tagname":
                return By.TAG_NAME

            else:
                self.log.info("Locator Type:{} not correct/supported".format(locatorType))
            return False
        except:
            self.log.debug("Exception! in getByType-> Locator Type:{} NOT CORRECT/NOT SUPPORTED".format(locatorType))
            traceback.print_stack()

    def getElement(self, locator, locatorType="id") -> webelement:
        """
        Returns a single element if present
        :param locator:
        :param locatorType:linktext,partiallinktext,tagname,name,classname,cssselector,xpath,id
        :return:
        """
        try:
            element = None
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found with locator: {} and locatorType: {}".format(locator, locatorType))
            return element
        except:
            self.log.error(
                "Exception! in getElement. Element NOT Found with locator: {} and locatorType: {}".format(locator,
                                                                                                          locatorType))
            traceback.print_stack()

    def getElements(self, locator, locatorType="id"):
        """
        Returns a multiple element if present
        :param locator:
        :param locatorType:
        :return:
        """
        try:
            elements = None
            byType = self.getByType(locatorType)
            elements = self.driver.find_elements(byType, locator)
            self.log.info("Elements Found with locator: {} and locatorType: {}".format(locator, locatorType))
            return elements
        except:
            self.log.error(
                "Exception! in getElements Elements NOT Found with locator: {} and locatorType: {}".format(locator,
                                                                                                           locatorType))
            traceback.print_stack()

    def isElementPresent(self, locator="", locatorType="id", element=None):
        """
        will return true if the element is present or else it will return false
        :param locator:
        :param locatorType:
        :return:
        """
        element = None
        try:
            if locator:  # This means the locator is not empty
                element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element Found with locator: {} and locatorType: {}".format(locator, locatorType))
                return True
            else:
                self.log.info("Element NOT Found with locator: {} and locatorType: {}".format(locator, locatorType))
                return False
        except:
            self.log.error("Element Not Found!")
            return False

    def isElementPresenceCheck(self, locator, locatorType, elements=None):
        """
        will return True or False ,will check if the element is present or not in the page , it does not care for the isDisplayed, if it is present and in the page it will return as true
        :param locator:
        :param locatorType:
        :return:
        """
        elements = None
        try:
            if locator:  # This means the locator is not empty
                elements = self.getElements(locator, locatorType)
            if len(elements) > 0:
                self.log.info("Element Found with locator: {} and locatorType: {}".format(locator, locatorType))
                return True
            else:
                self.log.info("Element NOT Found with locator: {} and locatorType: {}".format(locator, locatorType))
                return False
        except:
            self.log.error("Element NOT Found with locator: {} and locatorType: {}".format(locator, locatorType))
            return False

    def waitForElement(self, locator, locatorType, timeout=10, poll_frequency=0.5, waitType="visible"):
        """

        :param locator:
        :param locatorType:
        :param timeout:
        :param poll_frequency:
        :param waitType: clickable,ispresent,default=visibility_of_element_located
        :return:
        """
        element = None
        waitType = waitType.lower()
        byType = self.getByType(locatorType)
        try:
            self.log.info("Waiting for the element")
            if waitType == "clickable":
                element = WebDriverWait(self.driver, timeout, poll_frequency).until(
                    expected_conditions.element_to_be_clickable((byType, locator)))
                self.log.info(
                    "Wait complete for locator: {} and locatorType: {}, Returning the element which is clickable".format(
                        locator, locatorType))
                return element
            elif waitType == "ispresent":
                element = WebDriverWait(self.driver, timeout, poll_frequency).until(
                    expected_conditions.presence_of_element_located((byType, locator)))
                self.log.info(
                    "Wait complete for locator: {} and locatorType: {}, Returning the element which isPresent".format(
                        locator, locatorType))
            else:
                element = WebDriverWait(self.driver, timeout, poll_frequency).until(
                    expected_conditions.visibility_of_element_located((byType, locator)))
                self.log.info(
                    "Wait complete for locator: {} and locatorType: {}, Returning the element which isVisible".format(
                        locator, locatorType))
            return element
        except:
            self.log.error(
                "Waiting Done for locator: {} and locatorType: {}. Element Not Present!!!".format(locator, locatorType))
            traceback.print_stack()

    def saveScreenShot(self, test_name, result_message):
        try:
            # dir_location = os.getcwd() + "/Screenshots/" + test_name + "/"
            dir_location = Path(__file__).parent.parent / 'Screenshots' / test_name
            # Path.mkdir(dir_location, exist_ok=True)
            os.makedirs(dir_location, exist_ok=True)
            file_name = result_message.strip() + strftime("%d-%m-%y_%H:%M:%S", localtime()) + ".png"

            # file_path = os.path.join(dir_location, file_name)
            file_path = dir_location / file_name
            self.log.info("Taking Screenshot to-> {}".format(file_path))
            self.driver.save_screenshot(str(file_path))
            self.log.info("Screenshot taken in-> {}".format(file_path))
        except:
            self.log.error("Something went wrong while taking a Screenshot!!!")
            traceback.print_stack()



    def elementClick(self, locator="", locatorType="id", element=None):
        """
        Click on element
        Either provide element or a combination of both locator and locator type
        :param locator:
        :param locatorType:
        :param element:
        :return: None
        """
        try:
            if locator:  # This means if the locator is not empty
                element = self.getElement(locator, locatorType)
            element.click()
            self.log.info("Clicked on element with locator: {} and locatorType: {}".format(locator, locatorType))
        except:
            self.log.error("Click FAILED on element with locator: {} and locatorType: {}".format(locator, locatorType))
            self.log.error("self.log.infoing Stack Trace->")
            traceback.print_stack()

    def sendKeys(self, dataToEnter, locator="", locatorType="id", element=None):
        """
        Send keys to an element
        Either provide element or a combination of both locator and locator type
        :param locator:
        :param dataToEnter:
        :param locatorType:
        :param element:
        :return:
        """
        try:
            if locator:  # This means the locator is not empty
                element = self.getElement(locator, locatorType)
            element.send_keys(dataToEnter)
            self.log.info(
                "Entering Data: {} SUCCESSFULL to the locator: {} and locatorType{}".format(dataToEnter, locator,
                                                                                            locatorType))
        except Exception as e:
            self.log.error(
                "Entering the Data: {} FAILED to the locator: {}  and locatorType: {} ".format(dataToEnter, locator,
                                                                                               locatorType))
            self.log.error("Exception Message->{}".format(e))
            traceback.print_stack()

    def getText(self, locator="", locatorType="", element=None, info=""):
        """
        Get text of an element
        Either provide element or a combination of both locator and locator type
        :param locator:
        :param locatorType:
        :param element:
        :return: str
        """
        try:
            if locator:
                self.log.debug("In locator contdition")
                element = self.getElement(locator, locatorType)
            self.log.debug("Before finding the text")
            text = element.text
            self.log.debug("After finding the text, size is : " + str(len(text)))
            if len(text) == 0:
                text = element.get_attribute('innerText')
            if len(text) != 0:
                self.log.info("Getting the text of the element :: {}".format(info))
                self.log.info("The text is :: '{}'".format(text))
                text = text.strip()
                return text
        except:
            self.log.error("FAILED to get text on element {}".format(info))
            traceback.print_stack()
            text = None

    def isElementDisplayed(self, locator="", locatorType="id", element=None):

        try:
            isDisplayed = False
            if locator:
                element = self.getElement(locator, locatorType)
                isDisplayed = element.is_displayed()
                self.log.info("Element is displayed with locator: {} , locatorType: {}".format(locator, locatorType))
            else:
                self.log.info(
                    "Element is NOT displayed with locator: {} , locatorType: {}".format(locator, locatorType))
                return isDisplayed
        except:
            self.log.error("!Exception: Element NOT Found")
            return False

    def webScroll(self, locator="", locatorType="id", direction="up", element=None):
        """
        Scrolls the page till the element
        :param locator:
        :param locatorType:
        :param direction:
        :param element:
        :return:
        """

        try:
            if locator:
                element = self.getElement(locator, locatorType)
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                self.log.info(
                    "Scrolling Successful until the Element with locator : {} ,locatorType {} ".format(locator,
                                                                                                       locatorType))
                # element.location_once_scrolled_into_view
            elif direction == "up":
                self.driver.execute_script("window.scrollBy(0,-1000)")
                self.log.info("Scrolling page UP by -1000")
            elif direction == "down":
                self.driver.execute_script("window.scrollBy(0,1000)")
                self.log.info("Scrolling page DOWN by 1000")
        except:
            self.log.error("!Exception: FAILED to Scroll")

    def select(self, locator="", locatorType="id", element=None, toSelect=""):
        """
        Selcts option from the select box
        :param locator:
        :param locatorType:
        :param element:
        :param toSelect: visibleText to be selected
        :return: None
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            select = Select(element)
            select.select_by_visible_text(toSelect)
            self.log.info("Selecting option ->{} from Select box locator:{}, locatorType:{}".format(toSelect, locator,
                                                                                                    locatorType))
        except:
            self.log.error(
                "Exception!:Selecting Option ->{} FAILED from Select box locator:{}, locatorType:{}".format(toSelect,
                                                                                                            locator,
                                                                                                            locatorType))

    def checkSelected(self, locator="", locatorType="id", element=None) -> bool:
        """
        Checks if the  element is selected or not
        :param locator:
        :param locatorType:
        :param element:
        :return: boolean
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            state = element.is_selected
            if state:
                self.log.info("Element with locator:{}, locatorType:{} is Enabled")
            else:
                self.log.info("Element with locator:{}, locatorType:{} is Disabled")
            return state
        except:
            self.log.error("Exception!:Failed to check if the element is selected or not")

    def moveMouseTo(self, locator="", locatorType="id", element=None):
        """
        Moves the cursor to the locatoror element
        :param locator:
        :param locatorType:
        :param element:
        :return:
        """
        try:
            if locator:
                element = self.getElement(locator, locatorType)
            ActionChains(self.driver).move_to_element(element).perform()
            self.log.info("Moving Mouse to Element with locator: {} ,locatorType:{}".format(locator, locatorType))
        except:
            self.log.error(
                "Moving Mouse FAILED to Element with locator: {} ,locatorType:{}".format(locator, locatorType))

    def getTitle(self):
        return self.driver.title
