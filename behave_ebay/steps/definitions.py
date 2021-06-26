import shutil
from pathlib import Path
from grappa import should
from selenium import webdriver
from behave import when, then, given
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def open_element_in_new_tab(context, xpath_or_element):
    if isinstance(xpath_or_element, str):
        element = context.wait.until(EC.element_to_be_clickable(
            (By.XPATH, xpath_or_element)))
    else:
        element = xpath_or_element
    context.window_before = context.driver.window_handles[0]
    actions = ActionChains(context.driver)
    actions.move_to_element(
        element).key_down(
        Keys.COMMAND).click().key_up(
        Keys.COMMAND).perform()
    window_after = context.driver.window_handles[1]
    context.driver.switch_to_window(window_after)


@given('Open eBay')
def open_ebay(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.ebay.com/")
    context.wait = WebDriverWait(context.driver, 10)
    context.driver.implicitly_wait(5)


@when('Choose "{category}"')
def choose_category(context, category):
    xpath_select_category = "//select[@id = 'gh-cat']"
    element = ''

    try:
        element = context.wait.until(EC.presence_of_element_located(
            (By.XPATH, xpath_select_category)))
    except TimeoutException:
        print("Cannot choose the category")
    finally:
        select = Select(element)
        select.select_by_visible_text(category)


@when('Type "{item}" in the search field')
def search_item(context, item):
    xpath_search_field = "//input[@id = 'gh-ac']"

    search_input = context.wait.until(
        EC.presence_of_element_located((By.XPATH, xpath_search_field)))
    search_input.send_keys(item)
    context.wait.until(
        lambda browser: search_input.get_attribute('value') == item)


@when('Press search button')
def press_search_button(context):
    xpath_search_button = "//input[@id = 'gh-btn']"
    context.driver.find_element(By.XPATH, xpath_search_button).click()


@when('Find first item with "Buy it now" option and add it to cart')
def add_to_cart(context):
    xpath_first_item_with_buy_option = \
        "(//div[contains(@class, 's-item__info')" \
        " and .//span/text() = 'Buy It Now']/a)[1]"

    open_element_in_new_tab(
        context, xpath_first_item_with_buy_option)


@then('Add the item to cart and get the title')
def add_to_cart(context):
    xpath_item_title = '//h1[@id = "itemTitle"]'
    xpath_add_to_cart_button = "//a[@id = 'atcRedesignId_btn']"

    context.item_title = context.wait.until(
        EC.presence_of_element_located(
            (By.XPATH, xpath_item_title))
    ).text
    add_to = context.wait.until(EC.element_to_be_clickable(
        (By.XPATH, xpath_add_to_cart_button)))
    add_to.click()
    context.driver.close()
    context.driver.switch_to.window(context.window_before)


@then('Check if the item is in the cart')
def check_cart(context):
    xpath_title_in_minicart = "//span[parent::div/@class = 'gh-info__title']"
    xpath_cart = "//li[@id = 'gh-minicart-hover']"

    mini_cart = context.wait.until(EC.element_to_be_clickable(
        (By.XPATH, xpath_cart)))
    actions = ActionChains(context.driver)
    actions.move_to_element(mini_cart).perform()
    title_in_mini_cart = context.wait.until(EC.element_to_be_clickable(
        (By.XPATH, xpath_title_in_minicart)))

    title_in_mini_cart.text | should.be.equal(context.item_title)


######################################################################
# # # # # # # # # # # # SECOND SCENARIO  # # # # # # # # # # # # # # #
######################################################################

@when('Verify "{item}" search and sort listings by auctions')
def verify_and_sort(context, item):
    xpath_header_one = "//h1[@class = 'srp-controls__count-heading']"
    xpath_sort_listings_auction = "//span[text() = 'Auction' and ancestor::ul[@class='fake-tabs__items']]"

    check = context.wait.until(EC.text_to_be_present_in_element(
        (By.XPATH, xpath_header_one), item))
    check | should.be.equal.to(True)

    try:
        element = context.wait.until(EC.element_to_be_clickable(
            (By.XPATH, xpath_sort_listings_auction)))
        element.click()
    except TimeoutException:
        print("Cannot sort Listings by Action")


@when('Filter items: {price_max}, {price_min}, {ship_price_max}, {bid_days_left}')
def filter_items(context, price_max, price_min, ship_price_max, bid_days_left):
    xpath_links_for_filtered_items = "//div[contains(@class, 's-item__details')" \
                                          " and (translate(.//span/text(), '$', '') > 20" \
                                          " and translate(.//span/text(), '$', '') < 26 )" \
                                          " and (.//span[(contains(text(),'Free shipping'))" \
                                          " or translate(substring-before(., ' shipping'" \
                                          "), '+$', '') <= 20]) and (.//span[@class='s-item__time-left'" \
                                          " and substring-before(., 'd') > 1])]/ancestor::div/a"

    try:
        context.watch_links = context.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, xpath_links_for_filtered_items)))
    except TimeoutException:
        print("Cannot gather filtered elements")


@then('Create/cleanup the directory for screenshots')
def create_dir(context):
    shutil.rmtree('./screenshots')
    Path("./screenshots").mkdir(parents=True, exist_ok=True)


@then('Save screenshots of selected items in a newly created directory')
def save_screenshots(context):

    for count, watch_link in enumerate(context.watch_links):
        open_element_in_new_tab(context, watch_link)
        context.driver.save_screenshot(f"./screenshots/selected_item_picture_" + str(count) + ".png")
        context.driver.close()
        context.driver.switch_to.window(context.window_before)


######################################################################
# # # # # # # # # # # #  THIRD SCENARIO  # # # # # # # # # # # # # # #
######################################################################
