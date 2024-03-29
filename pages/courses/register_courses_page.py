import logging

import utilities.custom_logger as cl
from base.basepage import Basepage
from utilities.resultstatustracker import ResultStatusTracker


class RegisterCoursesPages(Basepage):
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(
            driver)  # calling Basepageclass constructor with the help of self() to initilize driver for parent class
        self.ts = ResultStatusTracker(driver)
        self.driver = driver

    # Locators
    _search_box_xpath = "//*[@id='search-courses']"
    _search_button_xpath = "// *[ @ id = 'search-course-button']"
    _selenium_webdriver_with_java_course_xpath = "//div[contains(text(),'Selenium WebDriver With Java')]"
    _enroll_in_course_button_top_css = "[id='enroll-button-top']"
    _card_number_text_xpath = "//*[text()='Card Number']"
    _card_number_text_field_iframe_xpath = "//*[@aria-label='Credit or debit card number']"
    _common_frame_for_payment_input_fields_xpath = "//iframe[@name='{}']"
    _payment_info_frame = "//*[text()='Payment Information']"
    _card_expiration_date_text_field_xpath = "//*[@placeholder='MM / YY']"
    _card_cvv_text_field_xpath = "//*[@aria-label='Credit or debit card CVC/CVV']"
    _card_country_select_box_id = "country_code_credit_card-cc"
    _card_postal_code_text_field_xpath = "//*[@id='root']/form/span[2]/span/input[@name='postal']"
    _card_i_agree_radio_button_xpath = "//input[@id='agreed_to_terms_checkbox']"
    _enroll_in_course_button_bottom_id = "confirm-purchase"
    _card_error_messagexpath = "//*[@class='payment-error-box']/i[@class='fa fa-exclamation-circle']/following-sibling::span[text()='The card was declined.']"

    # Methods to perform actions on the above elements
    def enterCourseName(self, course_name):
        self.sendKeys(course_name, self._search_box_xpath, "xpath")

    def clickOnSearchButton(self):
        self.elementClick(self._search_button_xpath, "xpath")

    def selectCourseToEnroll(self, full_course_name):
        ele = self.waitForElement(self._selenium_webdriver_with_java_course_xpath, "xpath")
        if str(self.getText(element=ele)).lower() == full_course_name.lower():
            self.elementClick(element=ele)
            self.log.info("Selection Done::Clicked on the {}".format(full_course_name))
        else:
            self.log.error("Course {} not found to click on it".format(full_course_name))

    def clickTopEnrollInCourse(self):
        self.elementClick(self._enroll_in_course_button_top_css, "cssselector")

    def scrollTillBottomEnrollInCourses(self):
        self.webScroll(self._enroll_in_course_button_bottom_id)

    def enterCardNumber(self, card_number):
        self.webScroll(self._card_number_text_xpath, "xpath")
        self.switchToFrame(self._common_frame_for_payment_input_fields_xpath.format("__privateStripeFrame8"), "xpath",
                           info="insideCardNumberFrame")
        self.sendKeys(card_number, self._card_number_text_field_iframe_xpath, "xpath")
        self.switchBackToParentFrame()

    def enterExpDate(self, card_date):
        self.switchToFrame(self._common_frame_for_payment_input_fields_xpath.format("__privateStripeFrame9"), "xpath",
                           info="expDateFieldFrame")
        self.sendKeys(card_date, self._card_expiration_date_text_field_xpath, "xpath")
        self.switchBackToParentFrame()

    def enterCvcCode(self, card_cvc):
        self.switchToFrame(self._common_frame_for_payment_input_fields_xpath.format("__privateStripeFrame10"), "xpath",
                           info="expDateFieldFrame")
        ele = self.getElement(self._card_cvv_text_field_xpath, "xpath")
        self.sendKeys(card_cvc, element=ele)
        self.switchBackToParentFrame()

    def selectCountry(self, card_country):
        ele = self.getElement(self._card_country_select_box_id)
        self.moveMouseTo(element=ele)
        self.select(self._card_country_select_box_id, toSelect=card_country)

    def enterPostalCode(self, card_postal_code):
        self.switchToFrame("(//iframe)[4]", "xpath",
                           info="expDateFieldFrame")
        self.sendKeys(card_postal_code, self._card_postal_code_text_field_xpath, "xpath")
        self.switchBackToParentFrame()

    def selectIAgreeToTerms(self, select=True):
        ele = self.getElement(self._card_i_agree_radio_button_xpath,"xpath")
        self.moveMouseTo(element=ele)
        state = self.checkSelected(element=ele)
        if state is False:
            self.elementClick(element=ele)

    def clickBottomEnrollInCourse(self):
        self.elementClick(self._enroll_in_course_button_bottom_id)

    def checkErrorMessageAfterForInvalidPayment(self, error_message_to_verify) -> bool:
        error_msg = self.getText(self._card_error_messagexpath, "xpath")
        if error_msg == error_message_to_verify:
            return True
        else:
            return False

    def enterCreditCardInformation(self, card_number, card_exp_date, card_cvc, card_country,
                                   card_postal_code):
        self.scrollTillBottomEnrollInCourses()
        self.enterCardNumber(card_number)
        self.enterExpDate(card_exp_date)
        self.enterCvcCode(card_cvc)
        self.selectCountry(card_country)
        self.enterPostalCode(card_postal_code)
        self.selectIAgreeToTerms(select=True)

    def enrollCourse(self, course_name, card_number, card_exp_date, card_cvc, card_country,
                     card_postal_code):
        self.enterCourseName(course_name)
        self.clickOnSearchButton()
        self.selectCourseToEnroll(course_name)
        self.clickTopEnrollInCourse()
        self.enterCreditCardInformation(card_number, card_exp_date, card_cvc, card_country,
                                        card_postal_code)
        self.clickBottomEnrollInCourse()

    def verifyEnrollFailed(self, error_message_to_verify):
        result1 = self.checkErrorMessageAfterForInvalidPayment(error_message_to_verify)
        return result1
