from behave import *
from pages.arithmetic_page import ArithmeticPage
from hamcrest import assert_that
from hamcrest import equal_to


@given('User opens arithmetic page')
def open_browse(context):
    context.browser.get("https://www.ck12.org/c/arithmetic/")


@then('Check arithmetic page header')
def check_arithmetic_header(context):
    """Checks the Arithmetic page's header"""
    arithmetic_page = ArithmeticPage(context.browser)
    assert_that(arithmetic_page.is_header_matched() is True)


@then('Check arithmetic page accordion opening')
def test_accordion_open(context):
    """Checks the Arithmetic page's accordion opening"""
    arithmetic_page = ArithmeticPage(context.browser)
    assert_that(arithmetic_page.is_every_accordion_open() is True)


@then('Click accordion links and check redirection')
def check_accordion_links(context):
    """Checks that all links on the page redirect properly"""
    arithmetic_page = ArithmeticPage(context.browser)
    assert_that(arithmetic_page.is_all_links_work() is True)
