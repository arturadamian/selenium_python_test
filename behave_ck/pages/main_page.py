from time import sleep
from pages.base_page import BasePage
from pages.modal_signin import ModalSignIn
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from locators.signin_modal_locators import SignInModalLocators as SL
from locators.main_page_locators import MainPageLocators as ML
from custom.element_has_css_style import element_has_css_style
from elements.language_button import language_button


class MainPage(BasePage):
    """Contains methods for login and close popups.

    Args:
        driver (obj): WebDriver set in test setUp()
        _wait (obj): explicit wait set for 10 seconds

    """

    def __init__(self, driver):
        super().__init__(driver)
        self._wait = WebDriverWait(self.driver, 10)

    def go_browse_page(self):
        try:
            self._wait.until(
                EC.element_to_be_clickable(
                    ML.SUBJECTS_BUTTON)
            ).click()
        except TimeoutException:
            print("Browse Page is not opening")

    def switch_language(self, lang):
        return self._wait.until(language_button(lang))

    def is_title_matched(self):
        return "Free Online Textbooks" in self.driver.title

    def is_signin_modal_shown(self):
        return self._wait.until(
            element_has_css_style(
                SL.MODAL_WINDOW,
                "visibility: visible;"))

    def is_logged_in(self, name):
        return self._wait.until(
            EC.text_to_be_present_in_element(
                ML.USER_HEADER,
                name.upper()))
