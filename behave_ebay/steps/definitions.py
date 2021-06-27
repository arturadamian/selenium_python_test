import shutil
from time import time
from time import sleep
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
    """Open element in a new tab and switch to it.

    Args:
        context (obj): Behave object.
        xpath_or_element (str or obj): xpath locator or WebDriver element.

    """
    if isinstance(xpath_or_element, str):
        element = WebDriverWait(
            context.driver, context.delay).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath_or_element)))
    else:
        element = xpath_or_element
    context.window_before = context.driver.window_handles[0]
    actions = ActionChains(context.driver)
    actions.move_to_element(
        element).key_down(
        Keys.COMMAND).click().key_up(
        Keys.COMMAND).perform()
    WebDriverWait(context.driver, context.delay).until(
        EC.number_of_windows_to_be(2))
    window_after = context.driver.window_handles[1]
    context.driver.switch_to_window(window_after)


def test_carousel_left(context, left):

    if context.count == 0:
        context.count = 2
    else:
        context.count -= 1
    left.click()
    sleep(1)
    slide = context.hero_carousel_slides[context.count]
    slide_apearence = slide.get_attribute("aria-hidden")

    slide_apearence | should.be.equal.to(None)


def test_carousel_right(context, right):
    if context.count == 2:
        context.count = 0
    else:
        context.count += 1
    right.click()
    sleep(1)
    slide = context.hero_carousel_slides[context.count]
    slide_apearence = slide.get_attribute("aria-hidden")

    slide_apearence | should.be.equal.to(None)


def test_carousel_play_pause(context, play_pause):
    context.xpath_play_pause_class = \
        "//*[name() = 'svg' and (contains(@class, 'icon--play') " \
        "or contains(@class, 'icon-pause'))]"

    play_pause_class = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_element_located(
            (By.XPATH, context.xpath_play_pause_class)))
    status_class = play_pause_class.get_attribute("class")
    play, pause = 0, 0
    if "icon--play" in status_class:
        play = 1
    elif "icon--pause" in status_class:
        pause = 1
    if context.count == 2 and play == 1:
        context.count = 0
    elif play == 1:
        context.count += 1
    elif pause == 1:
        play_pause.click()
        sleep(1)
        return
    play_pause.click()
    sleep(1)
    slide = context.hero_carousel_slides[context.count]
    slide_apearence = slide.get_attribute("aria-hidden")

    slide_apearence | should.be.equal.to(None)


@given('Open eBay')
def open_ebay(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.ebay.com/")
    context.delay = 5


@then('Quit browser')
def quit_browser(context):
    context.driver.close()
    context.driver.quit()


@when('Choose "{category}"')
def choose_category(context, category):
    xpath_select_category = "//select[@id = 'gh-cat']"
    element = ''

    try:
        element = WebDriverWait(
            context.driver, context.delay).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath_select_category)))
    except TimeoutException:
        print("Cannot choose the category")
    finally:
        select = Select(element)
        select.select_by_visible_text(category)


@when('Type "{item}" in the search field')
def search_item(context, item):
    xpath_search_field = "//input[@id = 'gh-ac']"

    search_input = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath_search_field)))
    search_input.send_keys(item)
    WebDriverWait(context.driver, context.delay).until(
        lambda browser: search_input.get_attribute('value') == item)


@when('Press search button')
def press_search_button(context):
    xpath_search_button = "//input[@id = 'gh-btn']"

    element = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_search_button)))
    element.click()


@when('Find first item with "Buy it now" option')
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

    context.item_title = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath_item_title))
    ).text
    add_to = WebDriverWait(
        context.driver, context.delay
    ).until(EC.element_to_be_clickable(
        (By.XPATH, xpath_add_to_cart_button)))
    add_to.click()
    context.driver.close()
    context.driver.switch_to.window(context.window_before)


@then('Check if the item is in the cart')
def check_cart(context):
    xpath_title_in_minicart = "//span[parent::div/@class = 'gh-info__title']"
    xpath_cart = "//li[@id = 'gh-minicart-hover']"

    mini_cart = WebDriverWait(
        context.driver, context.delay
    ).until(EC.element_to_be_clickable(
        (By.XPATH, xpath_cart)))
    actions = ActionChains(context.driver)
    actions.move_to_element(mini_cart).perform()
    title_in_mini_cart = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_title_in_minicart)))

    title_in_mini_cart.text | should.be.equal(context.item_title)


######################################################################
# # # # # # # # # # # # SECOND SCENARIO  # # # # # # # # # # # # # # #
######################################################################

@then('Verify "{item}" search')
def verify_searched_item(context, item):
    xpath_header_one = "//h1[@class = 'srp-controls__count-heading']"

    check = WebDriverWait(context.driver, context.delay).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, xpath_header_one), item))

    check | should.be.equal.to(True)


@when('Sort listings by left "{option}"')
def sort_listings_by_left_option(context, option):
    xpath_sort_listings_option = f"//span[text() = '{option}'" \
                                  f" and ancestor::ul[" \
                                  f"@class='fake-tabs__items']]"

    try:
        element = WebDriverWait(
            context.driver, context.delay).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath_sort_listings_option)))
        element.click()
    except TimeoutException:
        print(f"Cannot sort Listings by {option}")


@when('Filter items: {price_max}, {price_min}, '
      '{ship_price_max}, {bid_days_left}')
def filter_items(context, price_max, price_min,
                 ship_price_max, bid_days_left):
    xpath_links_for_filtered_items = \
        "//div[contains(@class, 's-item__details') and " \
        "(translate(.//span/text(), '$', '') > 10 and " \
        "translate(.//span/text(), '$', '') < 30 ) and " \
        "(.//span[(contains(text(),'Free shipping')) or " \
        "translate(substring-before(., ' shipping'), '+$', '') <= 20]) and " \
        "(.//span[@class='s-item__time-left' and " \
        "substring-before(., 'd') > 1])]/ancestor::div/a"

    try:
        context.watch_links = WebDriverWait(
            context.driver, context.delay).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, xpath_links_for_filtered_items)))
    except TimeoutException:
        print("Cannot collect filtered items")


@then('Create/cleanup the directory for screenshots')
def create_dir(context):
    shutil.rmtree('./screenshots')
    Path("./screenshots").mkdir(parents=True, exist_ok=True)


@then('Save screenshots of selected items in the directory')
def save_screenshots(context):
    for count, watch_link in enumerate(context.watch_links):
        open_element_in_new_tab(context, watch_link)
        context.driver.save_screenshot(f"./screenshots/selected_item_picture_"
                                       + str(count) + ".png")
        context.driver.close()
        context.driver.switch_to.window(context.window_before)


######################################################################
# # # # # # # # # # # #  THIRD SCENARIO  # # # # # # # # # # # # # # #
######################################################################

@when('Go back')
def go_back(context):
    context.driver.back()


@when('Find the first Recent searches element in suggested search')
def find_suggested_one(context):
    xpath_suggested_one = "(//li[contains(@class, 'ui-menu-item')]/a)[1]"

    context.suggested_one = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath_suggested_one)))


@then('verify first Recent searches element == "{full_item}"')
def verify_suggested_recent(context, full_item):
    suggested_one_aria_label = \
        context.suggested_one.get_attribute("aria-label")

    suggested_one_aria_label | should.have.contain("Recent searches")
    suggested_one_aria_label | should.have.contain(full_item)


#####################################################################
# # # # # # # # # # # #  FOURTH SCENARIO  # # # # # # # # # # # # # #
#####################################################################

@then('Verify carousel autoplay')
def find_carousel_elements(context):
    xpath_hero_carousel_slides = \
        "//li[contains(@class, 'carousel__snap-point')" \
        " and (ancestor::div[contains(@class, 'carousel__autoplay')])]"
    xpath_hero_carousel_play_pause_button = \
        "//button[contains(@class, 'carousel__playback')]"

    context.hero_carousel_slides = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, xpath_hero_carousel_slides)))

    context.count = 0
    for slide in context.hero_carousel_slides:
        slide_apearence = slide.get_attribute("aria-hidden")
        slide_apearence | should.be.equal.to(None)
        if context.count != 2:
            sleep(3.3)
        else:
            hero_carousel_play_pause_button = WebDriverWait(
                context.driver, context.delay).until(
                EC.element_to_be_clickable(
                    (By.XPATH, xpath_hero_carousel_play_pause_button)))
            hero_carousel_play_pause_button.click()
            break
        context.count += 1
    hero_carousel_play_pause_button = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_hero_carousel_play_pause_button)))
    test_carousel_play_pause(context, hero_carousel_play_pause_button)


@then('Verify carousel controls - left, right, play/pause buttons')
def verify_carousel_conrtols(context):
    xpath_hero_carousel_left_arrow_button = \
        "(//button[contains(@class, 'carousel__control') " \
        "and (ancestor::div[contains(@class, 'carousel__autoplay')])])[1]"
    xpath_hero_carousel_right_arrow_button = \
        "(//button[contains(@class, 'carousel__control')" \
        " and (ancestor::div[contains(@class, 'carousel__autoplay')])])[2]"

    hero_carousel_left_arrow_button = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_hero_carousel_left_arrow_button)))
    test_carousel_left(context, hero_carousel_left_arrow_button)

    hero_carousel_right_arrow_button = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_hero_carousel_right_arrow_button)))
    test_carousel_right(context, hero_carousel_right_arrow_button)
