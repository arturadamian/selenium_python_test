#!/usr/bin/env python3
import unittest
from unittest import skip
from config.config import *
from users.users import User
from pages.browse_page import BrowsePage
from pages.modal_signin import ModalSignIn


# @skip
class BrowsePageTest(unittest.TestCase):
    """Containes tests for the Browse page"""

    def setUp(self):
        """Sets up the environment for each session.

        Opens Chrome Browser with the Browse page.

        """
        self.driver = get_driver("chrome")
        self.driver.get(BASE_URL + BROWSE_ENDPOINT)
        self.browse_page = BrowsePage(self.driver)

    # @skip
    def test_title(self):
        """Checks that the Browse's page title is correct."""
        self.assertEqual(self.driver.title,
                         "K-12 FlexBooks® & Concepts | CK-12 Foundation")

    # @skip
    def test_links(self):
        """Check every link correct redirection"""
        assert self.browse_page.is_all_links_work()

    def tearDown(self):
        """Quits the driver"""
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
