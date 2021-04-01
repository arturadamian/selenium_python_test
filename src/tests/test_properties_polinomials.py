#!/usr/bin/env python3
import unittest
from unittest import skip
from config.config import *
from users.users import User
from pages.modal_signin import ModalSignIn
from pages.interactive_algebra_2.properties_polinomials_page \
    import PropertiesPolinomialsPage

# @skip
class PropertiesPolinomialsTest(unittest.TestCase):
    """Containes tests for the Main page"""

    def setUp(self):
        """Sets up the environment for each session.

        Opens Chrome Browser with the Main page and signs in.
        """
        self.driver = get_driver("chrome")
        self.driver.get(INTERACTIVE_ALGEBRA_2 + PROPERTIES_OF_POLYNOMIALS)
        self.user = User.STUDENT
        self.modal_signin = ModalSignIn(self.driver, self.user)
        self.property_page = PropertiesPolinomialsPage(self.driver)

    # @skip
    def test_pp(self):
        """Checks the title of the Main page."""
        assert self.property_page.is_header_matched(), \
            "Main page title does not match"

    def tearDown(self):
        """Quits the driver"""
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
