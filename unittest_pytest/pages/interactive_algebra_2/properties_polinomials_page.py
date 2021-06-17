from time import sleep
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from locators.interactive_algebra_2.properties_polinomials_locators \
    import PropertiesPolinomialsLocators as PP

class PropertiesPolinomialsPage(BasePage):
    """Contains methods for PropertiesPolinomials page.

    Args:
        driver (obj): WebDriver set in test setUp()
        _wait (obj): explicit wait set for 10 seconds

    """

    def __init__(self, driver):
        super().__init__(driver)
        self._wait = WebDriverWait(self.driver, 10)


    def is_header_matched(self):
        return self._wait.until(
            EC.text_to_be_present_in_element(
                PP.HEADER,
                "Properties of Polynomials"))

