#!/usr/bin/env python3
import unittest
from unittest import skip
from config.config import *
from users.users import User
from pages.modal_signin import ModalSignIn
from pages.arithmetic_page import ArithmeticPage


# @skip
class ArithmeticPageTest(unittest.TestCase):
    """Containes tests for the Arithmetic page"""

    def setUp(self):
        """Sets up the environment for each session.

        Opens Chrome Browser with the Main page and signs in.
        """
        self.driver = get_driver("chrome")
        self.driver.get(BASE_URL + ARITHMETIC_ENDPOINT)
        self.arithmetic_page = ArithmeticPage(self.driver)

    # @skip
    def test_page_header(self):
        """Checks the Arithmetic page's header"""
        assert self.arithmetic_page.is_header_matched(), \
            "Arithmetic page header does not match"

    # @skip
    def test_accordion_open(self):
        """Checks the Arithmetic page's accordion opening"""
        assert self.arithmetic_page.is_every_accordion_open(), \
            "arithmetic page accordion is not open"

    @skip
    def test_accordion_links(self):
        """Checks that all links on the page redirect properly"""
        assert self.arithmetic_page.is_all_links_work()

    def tearDown(self):
        """Quits the driver"""
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
