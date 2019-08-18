from selenium.webdriver.common.by import By
from selenium import webdriver
from base.selenium_driver import SeleniumDriver
import utilities.custom_logger as cl
import logging
from base.basepage import Basepage


class LoginPage(Basepage):
    log = cl.customLogger(logLevel=logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)  # calling baseclass constructor with help of self() to initialize driver there first
        self.driver = driver

    # Locators
    _login_link = "Login"
    _email_field = "user_email"
    _password_field = "user_password"
    _login_button_xpath = "//input[@name='commit']"

    def clickLoginLink(self):
        self.elementClick(self._login_link, "linktext")

    def enterEmail(self, username):
        self.sendKeys(self._email_field, username)

    def enterPassword(self, password):
        self.sendKeys(self._password_field, password)

    def clickLoginButton(self):
        self.elementClick(self._login_button_xpath, "xpath")

    def login(self, username="", password=""):
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
