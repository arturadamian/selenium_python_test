from pages.base_page import BasePage
from locators.browse_page_locators import BrowsePageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep


class BrowsePage(BasePage):
    """Contains methods for login and close popups.

    Args:
        driver (obj): WebDriver set in test setUp()
        _wait (obj): explicit wait set for 10 seconds

    """

    def __init__(self, driver):
        super().__init__(driver)
        self._wait = WebDriverWait(self.driver, 20)

    def is_all_links_work(self, options=None):
        """Checks all the links redirections

        Args:
            options (:obj:, optional): webdriver chrome options

        Returns:
            bool: True if `not failed` links count == all

        """
        try:
            link_elements = self._wait.until(
                EC.presence_of_all_elements_located(
                    BrowsePageLocators.ALL_LINKS))
        except TimeoutException:
            print("decimals_links were not collected")
        url_pattern = "interactives"

        for count, link_el in enumerate(link_elements):
            if "Grade" in link_el.text:
                grade = link_el.text[6:7]
                if grade == "1" or grade == "K":
                    link_text = "Grade 1"
                else:
                    link_text = f"Middle School Math {grade}"
            else:
                link_text = self.__link_text_hard_fix(link_el.text, options)
            window_before = self.driver.window_handles[0]
            el = self.click(link_el)
            ActionChains(self.driver).move_to_element(
                el).key_down(
                    Keys.COMMAND).click().key_up(
                        Keys.COMMAND).perform()
            sleep(0.5)
            window_after = self.driver.window_handles[1]
            self.driver.switch_to.window(window_after)

            if url_pattern not in self.driver.current_url:
                pass
                try:
                    self._wait.until(
                        EC.title_contains(link_text))
                except TimeoutException:
                    return False
            elif self._wait.until(
                        EC.title_contains("Physics Simulations")):
                if not self._wait.until(
                        EC.text_to_be_present_in_element(
                            BrowsePageLocators.LINKS_BY_URL[url_pattern],
                            link_text)):
                    return False
            else:
                return False

            self.driver.close()
            self.driver.switch_to.window(window_before)
            print(count)
        return count + 1 == len(link_elements)

    def __link_text_hard_fix(self, link_text, options):
        """Replace link text with matching title value

        Args:
            link_text (str): link text value
            options (:obj:, optional): webdriver chrome options

        Returns:
            str: corrected title match

        """
        link_text_correction = {
            "Algebra I": "Algebra 1",
            "Algebra II": "Algebra 2",
            "Philosophy": "PHILOSOPHY",
            "The Universe": "the Universe",
            "PreCalculus": "Precalculus",
            "FlexLets™": "FlexLets",
            "Geography": "Geo",
            "Deutsche": "Deutsch"
        }
        return link_text_correction.get(link_text, link_text)
