"""
@package base

WebDriverFactory class implementaion
It create a webdriver instance based on the command_line_browser configurations

Examples:
    wdf=WebDriverFactory(command_line_browser)
    wdf.getWebDriverFactoryInstance()
"""

from selenium import webdriver


class WebDriverFactory():

    def __init__(self, command_line_browser, base_url):
        """
        Inits webdriver factory class

        Returns:
            None
        :param command_line_browser:
                base_url:
        """
        self.browser = command_line_browser
        self.base_url = base_url

    def getWebDriverFactoryInstance(self):
        if self.browser == 'firefox':
            print("%" * 60)
            print("Running tests in Firefox as it is passed as command line argument..")
            driver = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
            print("%" * 60)
        elif self.browser == 'iexplorer':
            print("%" * 60)
            print("Running tests in Internet Explorer as it is passed as command line argument..")
            driver = webdriver.Ie(executable_path='/usr/local/bin/msedgedriver.exe')
            print("%" * 60)
        else:
            print("%" * 60)
            print("Running tests in Chrome as it is passed as command line argument..")
            driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
            print("%" * 60)

        # driver.maximize_window()
        driver.set_window_size(1366,768)

        driver.get(self.base_url)
        driver.implicitly_wait(10)
        return driver
