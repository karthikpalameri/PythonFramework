from selenium import webdriver
from pages.home.login_page import LoginPage
import pytest


@pytest.mark.usefixtures("oneTimeSetup", "setUp")
class TestLoginTests():

    @pytest.fixture(autouse=True)
    def classSetup(self):
        """
        classSetup is a custom fixture written here and not is conftest
        onTimeSetup and setUp fixtures will not be called first as none of them are passed as arguments for classSetup function
        it is just a fixture which will act as a constructor and initializes the class whichever we want and makes it available to all the 
        :return:
        """
        lp = LoginPage(self.driver)

    @pytest.mark.run(order=2)
    def test_invalidLogin(self):
        self.driver.get(self.baseUrl)
        self.lp.login("test@email.com", "abcabc")
        result = self.lp.verifyLoginSuccessful()
        assert result == True
        self.driver.quit()

    @pytest.mark.run(order=1)
    def test_validLogin(self):
        self.driver.get(self.baseUrl)
        self.lp.login("test@email.com", "abcabcxyz")
        result = self.lp.verifyLoginFailed()
        assert result == True
