import inspect

from selenium.webdriver import ActionChains

import utilities.custom_logger as cl
import logging
from base.basepage import Basepage
from utilities.prototype import Prototype as pt


class LoginPage(Basepage):
    log = cl.customLogger(logLevel=logging.DEBUG)

    def __init__(self, driver):
        super().__init__(
            driver)  # calling Basepageclass constructor with help of self() to initialize driver there first
        self.driver = driver
        self.ptobject = pt(driver)

    # Locators
    _login_link = "Login"
    _email_field = "user_email"
    _password_field = "user_password"
    _login_button_xpath = "//input[@name='commit']"

    def clickLoginLink(self):
        print()
        # below code will generate the cropped image of the element passed in as parameter
        # self.ptobject.cropElement(self.__class__.__name__, "_login_link", self._login_link, "linktext")
        self.elementClick(self._login_link, "linktext")

    def enterEmail(self, username):
        self.sendKeys(locator=self._email_field, dataToEnter=username)

    def enterPassword(self, password):
        self.sendKeys(locator=self._password_field, dataToEnter=password)

    def clickLoginButton(self):
        self.elementClick(self._login_button_xpath, "xpath")

    def login(self, username="", password=""):
        print()
        # Below code will utilize the prototype module and fetch the element
        # ele = self.ptobject.getElementFromProtoType(page_name="practice", image_name="_login_link.png")
        # self.elementClick(element=ele)
        self.clickLoginLink()
        self.enterEmail(username)
        self.enterPassword(password)
        self.clickLoginButton()

    def verifyLoginSuccessful(self):
        result = self.isElementPresent("//*[@id='navbar']/div/div/div/ul/li[4]/a/span", locatorType="xpath")
        return result

    def verifyLoginFailed(self):
        result = self.isElementPresent("//div[contains(text(),'Invalid email or password.')]", locatorType="xpath")
        return result

    def getTitle(self):
        return self.driver.title

    def verifyLoginTitle(self):
        return self.verifyPageTitle("Google")

    def logout(self):
        return self.driver.execute_script("$x('//*[@id='navbar']/div/div/div/ul/li[4]/ul/li[5]/a')[0].click()")
