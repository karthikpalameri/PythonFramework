import utilities.custom_logger as cl
import logging
from  base.basepage import Basepage

class RegisterCoursesPages(Basepage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver) #calling Basepageclass constructor with the help of self() to initilize driver for parent class
        self.driver = driver


        #Locators

        _search_box=""