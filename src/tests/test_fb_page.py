#!/usr/bin/env python3
import unittest
from unittest import skip
from config.config import *
from users.users import User
from pages.modal_signin import ModalSignIn


# @skip
class FacePageTest(unittest.TestCase):
    """Containes tests for the Main page"""

    def setUp(self):
        """Sets up the environment for each session.

        Opens Chrome Browser with the Main page and signs in.
        """
        self.driver = get_driver("chrome")
        self.driver.get("https://www.ck12.org/fbbrowse/")
        self.user = User.STUDENT
        self.modal_signin = ModalSignIn(self.driver, self.user)

    # @skip
    # def test_aa(self):
    #     """Checks the title of the Main page."""
        # x = self.el_select("//select[@name='Language']", "English")
        # y = self.el_select("//select[@name='Subject']", "Language Arts")
        # z = self.el_select("//select[@name='Grade']", "Elementary School")
        # print(x, y, z)

    def tearDown(self):
        """Quits the driver"""
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()
