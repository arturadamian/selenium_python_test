from behave import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from locators.xpath import SearchPage as X
from locators.xpath import ItemPage as XI
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from custom.element_chaged_css import element_chaged_css_class
from hamcrest import assert_that
from hamcrest import equal_to


@given('Navigate to eBay')
def open_ebay(context):
    """Opens the page"""
    context.browser = webdriver.Chrome()
    context.browser.get("https://www.ebay.com/")
    context.wait = WebDriverWait(context.browser, 10)


@when('Choose "{category}"')
def choose_category(context, category):
    """Selects the option"""
    try:
        select = Select(context.browser.find_element_by_xpath(
            X.SELECT_CATEGORY))
        select.select_by_visible_text(category)
    except TimeoutException:
        print("Cannot choose the category")


@when('Search "{item}"')
def search_item(context, item):
    """Sends the keys"""
    search_input = context.browser.find_element(By.XPATH, X.SEARCH_FIELD)
    search_input.send_keys(item)
    context.browser.find_element(By.XPATH, X.SEARCH_BUTTON).click()


@when('Add first found item to cart')
def add_to_cart(context):
    """Adds the item in a separate tab"""
    first = 1
    first_item = X.SEARCH_RESULTS + f"[{first}]" + X.RESULTS_IMAGE
    element = context.wait.until(EC.element_to_be_clickable(
        (By.XPATH, first_item)))
    window_before = context.browser.window_handles[0]
    ActionChains(context.browser).move_to_element(
        element).key_down(
        Keys.COMMAND).click().key_up(
        Keys.COMMAND).perform()
    window_after = context.browser.window_handles[1]
    context.browser.switch_to_window(window_after)
    context.title = context.browser.find_element_by_xpath(XI.TITLE).text
    add_to = context.wait.until(EC.element_to_be_clickable(
        (By.XPATH, XI.ADD_TO_CART)))
    add_to.click()
    context.browser.close()
    context.browser.switch_to.window(window_before)


@then('Check the cart')
def check_cart(context):
    """Checks if the mini cart contains added item"""
    element = context.wait.until(EC.element_to_be_clickable(
        (By.XPATH, X.CART)))
    ActionChains(context.browser).move_to_element(element).perform()
    context.wait.until(element_chaged_css_class(element, "gh-flyout-active"))
    ActionChains(context.browser).move_to_element(element).perform()
    mini_title = context.browser.find_element_by_xpath(
        X.MINICART_ITEM_TITLE).text
    assert_that(mini_title, equal_to(context.title))
