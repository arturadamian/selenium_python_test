from time import sleep
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from locators.main_page_locators import MainPageLocators as ML
from locators.signin_modal_locators import SignInModalLocators as SL
from custom.element_has_css_style import element_has_css_style


class ModalSignIn(BasePage):
    """Contains methods for login and close popups.

    Args:
        driver (obj): [description]

    """

    def __init__(self, driver):
        super().__init__(driver)
        self._wait = WebDriverWait(self.driver, 10)

    def popup_close(self):
        """Closes popup window."""
        if self._wait.until(
            element_has_css_style(
                ML.POPUP_WINDOW,
                'visibility: visible;')):
            ActionChains(self.driver).send_keys(
                Keys.TAB).send_keys(Keys.RETURN).perform()
        else:
            return

    def open_modal(self):
        """Opens modal window with the signin form"""
        try:
            # unmute the line below if you get the popup window
            # self.popup_close()
            self._wait.until(
                EC.element_to_be_clickable(
                    ML.SIGNIN_BUTTON)
            ).click()
            sleep(0.4)
        except TimeoutException:
            print('Cannot Open Modal')

    def login(self, username, password):
        """logs in the user

        Args:
            username (str): user's username
            password (str): user's password

        """
        try:
            # self.open_modal()  # Skip this if use tests in order
            self._wait.until(
                EC.presence_of_element_located(
                    SL.USERNAME_INPUT)
            ).send_keys(username)
            self._wait.until(
                EC.presence_of_element_located(
                    SL.PASSWORD_INPUT)
            ).send_keys(password)
            sleep(0.5)
            self._wait.until(
                EC.element_to_be_clickable(
                    SL.SIGNIN_MODAL_BUTTON)
            ).click()
            sleep(0.3)
        except TimeoutException:
            print('Cannot login')
