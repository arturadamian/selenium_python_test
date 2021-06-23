from locators.main_page_locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


class language_button:
    """Selets language with the button located in footer.

    Args:
        lang (str): Language to select

    """
    def __init__(self, lang):
        self.lang = lang

    def __call__(self, driver):
        """Changes the language with the element in iframe.

        Returns:
            bool: True if succesful otherwise runs out of time

        """
        wait = WebDriverWait(driver, 10)
        # print(self.lang)
        wait.until(
            EC.element_to_be_clickable(
                MainPageLocators.LANGUAGE_BUTTON)
        ).click()
        wait.until(
            EC.frame_to_be_available_and_switch_to_it(
                MainPageLocators.LANGUAGE_IFRAME))
        driver.find_element_by_xpath(
            f"//span[contains(., '{self.lang}')]"
        ).click()
        driver.switch_to.default_content()
        sleep(1)
        return True
