from time import sleep
from pages.base_page import BasePage
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from custom.element_has_css_class import element_has_css_class
from custom.element_changed_css_class import element_changed_css_class
from locators.arithmetic_page_locators import ArithmeticPageLocators as AL


class ArithmeticPage(BasePage):
    """Contains methods for Arithmetic page.

    Args:
        driver (obj): WebDriver set in test setUp()
        _wait (obj): explicit wait set for 10 seconds

    """

    def __init__(self, driver):
        super().__init__(driver)
        self._wait = WebDriverWait(self.driver, 10)

    def expand_all(self):
        try:
            self._wait.until(
                EC.element_to_be_clickable(
                    AL.EXPAND_ALL_BUTTON)
            ).click()
            sleep(0.2)
        except TimeoutException:
            print("decimals_links were not collected")

    def open_every_accordion(self):
        try:
            accordion_header_elements = self._wait.until(
                EC.presence_of_all_elements_located(
                    AL.ACCORDIONS_HEADERS)
            )
        except TimeoutException:
            print("accordion header elements were not collected")
        for accordion_header in accordion_header_elements:
            try:
                sleep(0.3)
                accordion_header.click()
                self._wait.until(
                    element_changed_css_class(
                        accordion_header,
                        "level-1-concept show-child-concepts clicked"))
            except TimeoutException:
                print("Cannot open accordion")

    def is_all_links_work(self):
        self.expand_all()
        link_elements = self._wait.until(
            EC.presence_of_all_elements_located(
                AL.ACCORDIONS_LINKS))
        for count, link_el in enumerate(link_elements):
            link_text = link_el.text
            window_before = self.driver.window_handles[0]
            sleep(0.3)
            ActionChains(self.driver).move_to_element(
                link_el).key_down(
                    Keys.COMMAND).click().key_up(
                        Keys.COMMAND).perform()
            sleep(0.3)
            window_after = self.driver.window_handles[1]
            self.driver.switch_to.window(window_after)
            # print(count)
            if not self._wait.until(
                EC.text_to_be_present_in_element(
                    AL.ACCORDIONS_CLICKED_LINKS,
                    link_text)):
                return False
            else:
                self.driver.close()
            self.driver.switch_to.window(window_before)
        return count == len(link_elements)

    def is_header_matched(self):
        return self._wait.until(
            EC.text_to_be_present_in_element(
                AL.ARITHMETIC_HEADER,
                "Arithmetic"))

    def is_every_accordion_open(self):
        self.open_every_accordion()
        return self._wait.until(
            element_has_css_class(
                AL.DECIMALS_ACCORDION,
                "show-child-concepts clicked"))
