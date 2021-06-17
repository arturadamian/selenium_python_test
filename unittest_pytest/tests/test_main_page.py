#!/usr/bin/env python3
import unittest
from unittest import skip
from config.config import *
from users.users import User
from pages.main_page import MainPage
from pages.modal_signin import ModalSignIn


# @skip
class MainPageTest(unittest.TestCase):
    """Containes tests for the Main page"""

    def setUp(self):
        """Sets up the environment for each session.

        Opens Chrome Browser with the Main page and signs in.
        """
        self.driver = get_driver("chrome")
        self.driver.get(BASE_URL)
        self.user = User.TEACHER
        self.modal_signin = ModalSignIn(self.driver, self.user)
        self.main_page = MainPage(self.driver)

    # @skip
    def test_main_page_title(self):
        """Checks the title of the Main page."""
        assert self.main_page.is_title_matched(), \
            "Main page title does not match"

    # @skip
    def test_modal_open(self):
        """Checks the visibility of the modal window."""
        self.modal_signin.open_modal()
        assert self.main_page.is_signin_modal_show(), \
            "signin modal is not shown"

    # @skip
    def test_user_signed_in(self):
        """Checks that user is logged in."""
        self.modal_signin.login()
        assert self.main_page.is_logged_in(self.user), \
            "user is not logged in"

    # @skip
    def test_change_language(self):
        """Checks language change element in footer"""
        langs = ['Zulu', 'Chinese', 'Hebrew', 'Burmese']
        assert all([self.main_page.switch_language(lang) for lang in langs])

    def tearDown(self):
        """Quits the driver"""
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
