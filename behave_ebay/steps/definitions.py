import shutil
import requests
import json
import re
import emoji
from PIL import Image
from time import sleep
from io import BytesIO
from pathlib import Path
from grappa import should
from behave import when
from behave import then
from behave import given
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import InvalidSwitchToTargetException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


# --- Set up environment


@given('Open eBay')
def open_ebay(context):
    context.driver.get(context.ENVIRONMENT)


# --- Search correction


@then('Verify rewritten search is {auto_correction}')
def find_notice(context, auto_correction):
    xpath_search_notice = \
        "//div[contains(@class, 'srp-river-answer--REWRITE_START')]" \
        "//span[@class = 'BOLD']"
    assert context.wait.until(EC.text_to_be_present_in_element(
        (By.XPATH, xpath_search_notice), auto_correction)), \
        f"The search auto correction does not match. Expected: {auto_correction}"


# --- Verify result of the specific search on given pages


@then('Verify titles contain {keywords} on the pages '
      'from {current_page:d} to {page_number:d}')
def verify_titles_on_given_pages(context, keywords, current_page, page_number):
    xpath_current_page = \
        f"//a[@class = 'pagination__item' and text() = '{current_page}']"
    description = f"Page number {page_number}"

    _click(context, xpath_current_page, description)

    counter = -1 if page_number - current_page < 0 else 1

    page_count = abs(current_page - page_number)
    while page_count >= 0:
        context.execute_steps(f"""
            When Collect listing titles
            Then Verify that titles contain exact words {keywords}
            """)
        current_page += counter
        page_count -= abs(counter)
        if page_count >= 0:
            xpath_page_number = \
                f"//a[@class = 'pagination__item' and " \
                f"text() = '{current_page}']"
            _click(context, xpath_page_number, description)


# --- Verify result of the specific search on all pages


@then('Open All refinements')
def all_refinements(context):
    xpath_see_all_refinements = \
        "//span[text() = 'see all']" \
        "[ancestor::li[@class = 'x-refine__main__list ' " \
        "and ./div/@aria-expanded = 'true']][1]"
    description = "First visible link to see all refinements"

    _click(context, xpath_see_all_refinements, description)
    sleep(.5)


@when('In all refinements choose "{category}" {options}')
def sort_by_category_and_option(context, category, options):

    xpath_all_refinements_category = \
        f"//div[contains(@class, 'x-overlay-aspect') " \
        f"and ./span[text() = '{category}']]"
    description = f"All refiniments category {category}"

    _click(context, xpath_all_refinements_category, description)
    if "[" in options:
        options = json.loads(options)
        options = sorted(options)
        description = \
            f"All refiniments category {category} with option {options}"
        xpath_all_refinements_options = \
            f"//form[@id = 'x-overlay__form']" \
            f"//span[contains(@class, 'x-refine__multi-select-cbx') and " \
            f"text() < '{options[-1]}' and  text() > '{options[0]}']"
        all_refinements_options = _collect(context, xpath_all_refinements_options, description)
        for item in all_refinements_options:
            size = item.text.split()[0]
            if float(size) in options:
                item.click()
            else:
                continue
    else:
        description = \
            f"All refiniments category {category} with option {options}"
        xpath_all_refinements_options = \
            f"//form[@id = 'x-overlay__form']" \
            f"//*[contains(@class, 'x-refine__multi-select-cbx') " \
            f"and text() = '{options}'][self::label or self::span]"
        _click(context, xpath_all_refinements_options, description)


@when('Press Apply Button')
def press_apply(context):
    xpath_apply_button = \
        f"//button[contains(@class, 'x-overlay-footer__apply-btn')]"
    description = "All refinements apply button"

    _click(context, xpath_apply_button, description)


@then('Collect pagination items')
def collect_pagination(context):
    xpath_pagination = "//a[@class = 'pagination__item']"

    try:
        context.pages = WebDriverWait(context.driver, 3).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, xpath_pagination)))
    except TimeoutException:
        context.pages = [1]


@then('Verify all titles on all pages contain search {keywords}')
def verify_all_pages_title(context, keywords):
    while context.pages:
        context.execute_steps(f"""
            When Collect listing titles
            Then Verify that titles contain exact words {keywords}
            """)
        context.pages.pop(0)
        if context.pages:
            context.pages[0].click()


# --- Verify Advanced Search


@given('Data stored for Advanced Search')
def saved_data(context):
    context.xpath_input_field = "//input[@name = '_nkw']"
    context.xpath_search_button = "//button[@id = 'searchBtnLowerLnk']"
    context.xpath_titles = "//a[parent::h3[@class = 'lvtitle']]"


@when('In keywords options select {keyword_option}')
def select_keywords_options(context, keyword_option):
    xpath_keywords_options = "//select[@id = '_in_kw']"

    _select(context, xpath_keywords_options, keyword_option)


@when('In Price put from {min_price} to {max_price}')
def price_option(context, min_price, max_price):
    xpath_min_price = "//input[@name = '_udlo']"
    xpath_max_price = "//input[@name = '_udhi']"

    _type(context, xpath_min_price, min_price)
    _type(context, xpath_max_price, max_price)


@when('Check {option}')
def check_option(context, option):
    xpath_checkbox = \
        f"//input[starts-with(@id, 'LH')][@type = 'checkbox']" \
        f"[following-sibling::node()[normalize-space() = '{option}']]"
    description = f"Advanced: checkbox {option}"

    _click(context, xpath_checkbox, description)


@when('In Location select {max_miles} of {index}')
def price_option(context, max_miles, index):
    xpath_located_max_miles = "//select[@id = '_sadis']"
    xpath_located_index = "//input[@name = '_stpos']"

    _select(context, xpath_located_max_miles, max_miles)
    _type(context, xpath_located_index, index)


@when('In Sort by select {sort_by_option}')
def price_option(context, sort_by_option):
    xpath_sort_by = "//select[@id='LH_SORT_BY']"

    _select(context, xpath_sort_by, sort_by_option)


@when('In View results select {sort_by_option}')
def price_option(context, sort_by_option):
    xpath_sort_by = "//select[@id='LH_VIEW_RESULTS_AS']"

    _select(context, xpath_sort_by, sort_by_option)


@when('In Results per page select {number_of_results}')
def price_option(context, number_of_results):
    xpath_sort_by = "//select[@id = 'LH_IPP']"

    _select(context, xpath_sort_by, number_of_results)


@then('Verfiy number {number_results:d}')
def verify_number(context, number_results):
    xpath_listings = "//ul[@id='ListViewInner']/li"
    listings = "listings"

    context.listings = _collect(context, xpath_listings, listings)

    assert len(context.listings) <= number_results, \
        f"The number of listings on the page " \
        f"should be {number_results} but {len(context.listings)} instead"


@then('Verify Distance: nearest first, {index},'
      ' not farther than {max_miles:d}')
def verify_number(context, index, max_miles):
    xpath_distance = "//ul[contains(@class, 'lvdetails')]/li[1]"
    ship_distance = "ship_distance"
    mismatch_idx, dist = [], []

    ship_distance = _collect(context, xpath_distance, ship_distance)
    for item in ship_distance:
        text_split = item.text.split()
        if text_split[0] == "<":
            n = text_split[1].replace(",", "")
            dist.append(int(n))
        else:
            n = text_split[0].replace(",", "")
            dist.append(int(n))
        if text_split[-1] != index:
            mismatch_idx.append(text_split[-1])

    if mismatch_idx:
        raise AssertionError(
            f"Index of users location should be {index} "
            f"but {mismatch_idx} instead")
    assert max(dist) < max_miles, \
        f"The item is located {max(dist)} miles away " \
        f"which is more than {max_miles} by filter"
    assert all(dist[i] <= dist[i + 1] for i in range(len(dist) - 1)), \
        "The listings are not sorted by 'nearest first'"


@then('Verify the price of the listing on the page'
      ' is from {min_price:d} to {max_price:d}')
def verify_price(context, min_price, max_price):
    xpath_items_price = "//span[parent::li[contains(@class, 'lvprice')]]"
    prices = "prices"
    mismatch_from_to_price, mismatch_price = [], []

    prices = _collect(context, xpath_items_price, prices)
    for price in prices:
        price = price.text.replace("$", "")
        if "to" in price:
            price_from, price_to = price.split("to")
            if min_price >= int(float(price_from)) >= max_price or \
                    min_price >= int(float(price_to)) >= max_price:
                mismatch_from_to_price.append(price)
        else:
            if min_price >= int(float(price)) >= max_price:
                mismatch_price.append(price)
    if mismatch_from_to_price:
        raise AssertionError(
            f"The price {mismatch_from_to_price} is out of range")
    if mismatch_price:
        raise AssertionError(f"The price {mismatch_price} is out of range")


@then('Verify that titles contain exact words {words}')
def verify_keywords_in_titles(context, words):
    mismatch = []
    for title in context.titles:
        text = title.text.lower().split()
        keywords = words.split()
        if set(keywords) & set(text) is False:
            mismatch.append(title.text)
    if mismatch:
        raise AssertionError(f"Some titles do not contain exact words")


@then('Verify Free shipping and Sale')
def verify_sale(context):
    xpath_sale = "//div[@class = 'cmpat']/span"
    xpath_ship = "//span[@class = 'bfsp']" \
                 "[ancestor::span[@class = 'ship']]"
    sale_text = "Was"
    ship_text = "Free shipping"
    mismatch_sale, mismatch_ship = [], []

    for count, listing in enumerate(context.listings):
        element = listing.find_element_by_xpath(xpath_sale)
        if sale_text in element.text is False:
            mismatch_sale.append(element.text)
        element = listing.find_element_by_xpath(xpath_ship)
        if ship_text in element.text is False:
            mismatch_ship.append(element.text)

    if mismatch_sale:
        raise AssertionError(f"Some listings are not on sale: {mismatch_sale}")
    if mismatch_ship:
        raise AssertionError(
            f"Some listings have no Free shipping: {mismatch_ship}")


# --- Verify Hero Carousel functionality


@given('Hero carousel slides are collected')
def collect_carousel_slides(context):
    xpath_carousel_slide_titles = \
        "//li[contains(@class, 'carousel__snap-point')]" \
        "[ancestor::div[contains(@class, 'carousel__autoplay')]]//h2"
    description = "Hero carousel slides"

    context.hero_carousel_slides = \
        _collect(context, xpath_carousel_slide_titles, description)


@then('Verify carousel autoplay')
def verify_autoplay(context):
    mismatch_slide_visibility = []
    for slide in context.hero_carousel_slides:
        header_is_visible = context.wait.until(EC.visibility_of(slide))
        if not header_is_visible:
            mismatch_slide_visibility.append(slide.text)
        context.slide = slide
    if mismatch_slide_visibility:
        raise AssertionError(
            f"Carousel slide: {mismatch_slide_visibility} is not visible ")
    context.slide_index = \
        context.hero_carousel_slides.index(context.slide)


@when('Carousel {action}')
def carousel_action(context, action):
    xpath_play_pause_button = \
        "//button[contains(@class, 'carousel__playback')]"
    xpath_right_arrow_button = \
        "//button[contains(@class, 'carousel__control')]" \
        "[ancestor::div[contains(@class, 'carousel__autoplay')]][2]"
    xpath_left_arrow_button = \
        "//button[contains(@class, 'carousel__control')]" \
        "[ancestor::div[contains(@class, 'carousel__autoplay')]][1]"
    description = "Carousel " + action + " button"

    if action == "pause":
        _click(context, xpath_play_pause_button, description)
        return
    elif action == "play":
        _click(context, xpath_play_pause_button, description)
    elif action == "right":
        _click(context, xpath_right_arrow_button, description)
    elif action == "left":
        _click(context, xpath_left_arrow_button, description)
    context.slide = expected_slide(context, action)


@then('Verify {pressed} button')
def verify_pause(context, pressed):
    xpath_play_pause_class = \
        "//*[name() = 'svg']" \
        "[parent::button/@class = 'carousel__playback']"
    description = "Play/pause carousel button"

    play_pause_class = _present(context, xpath_play_pause_class, description)
    status_class = play_pause_class.get_attribute("class")
    if pressed == "pause":
        assert "icon--play" in status_class, \
            f"Carousel button status is incorrect after pressing {pressed}"
    elif pressed == "play":
        assert "icon--pause" in status_class, \
            f"Carousel button status is incorrect after pressing {pressed}"


def expected_slide(context, action):
    max_index = len(context.hero_carousel_slides) - 1
    if action == "left":
        if context.slide_index > 0:
            context.slide_index -= 1
            slide = context.hero_carousel_slides[context.slide_index]
        else:
            context.slide_index = max_index
            slide = context.hero_carousel_slides[context.slide_index]
    elif action == "right" or action == "play":
        if context.slide_index < max_index:
            context.slide_index += 1
            slide = context.hero_carousel_slides[context.slide_index]
        else:
            context.slide_index = 0
            slide = context.hero_carousel_slides[context.slide_index]
    else:
        return
    return slide


@then('Verify correct slide appearance')
def verify_slide(context):
    xpath_visible_carousel_slide_header = \
        "//li[contains(@class, 'carousel__snap-point')]" \
        "[ancestor::div[contains(@class, 'carousel__autoplay')]]" \
        "[not(@aria-hidden = 'true')]//h2"

    sleep(1)
    visible_slide = context.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, xpath_visible_carousel_slide_header)))
    assert context.slide == visible_slide, \
        "The current slide is not the one that should be visible"


# --- Add the first searched item to cart and verify that
# --- with it's title in mini cart


@given('Saved data')
def save_data(context):
    context.xpath_select_category = "//select[@id = 'gh-cat']"
    context.xpath_input_field = "//input[@id = 'gh-ac']"
    context.xpath_search_button = "//input[@id = 'gh-btn']"
    context.xpath_item_title = '//h1[@id = "itemTitle"]'


@when('select {category}')
def select_category(context, category):
    _select(context, context.xpath_select_category, category)


@when('Type {item} in the search field')
def type_item(context, item):
    if not hasattr(context, 'item'):
        context.item = item.lower()
    _type(context, context.xpath_input_field, item)


@when('Press search button')
def press_search_button(context):
    description = "Search button"

    _click(context, context.xpath_search_button, description)


@when('Find first item to open in a new tab')
def find_first_item(context):
    xpath_first_item_with_buy_option = \
        "(//div[contains(@class, 's-item__info')]" \
        "[.//span/text() = 'Buy It Now']/a)[1]"
    description = "First item with Buy It Now option"

    context.xpath_el_new_tab = \
        _present(
            context, xpath_first_item_with_buy_option, description)
    if context.xpath_el_new_tab is None:
        context.skip_scenario(
            reason='There is no item with Buy It Now option on the page')


@when('Open element in a new tab')
def open_element_in_new_tab(context):
    description = "Element opening in a new tab"
    err_msg_move = f"Cannot move to {description}"
    err_msg_no_window = "The second tab was not opened"
    err_msg_switch = "Driver cannot switch to the second tab"

    if isinstance(context.xpath_el_new_tab, str):
        element = _present(
            context, context.xpath_el_new_tab, description)
    else:
        element = context.xpath_el_new_tab
    sleep(.2)
    context.window_before = context.driver.window_handles[0]
    try:
        actions = ActionChains(context.driver)
        actions.move_to_element(
            element).key_down(
            Keys.COMMAND).click().key_up(
            Keys.COMMAND).perform()
        sleep(.2)
    except MoveTargetOutOfBoundsException(err_msg_move):
        raise
    try:
        context.wait.until(
            EC.number_of_windows_to_be(2))
        window_after = context.driver.window_handles[1]
        context.driver.switch_to_window(window_after)
    except TimeoutException as e:
        raise NoSuchWindowException(err_msg_no_window) from e
    except InvalidSwitchToTargetException(err_msg_switch):
        raise


@then('Get the title of the item')
def get_title(context):
    description = "Title on the item's page"

    sleep(.1)
    item_title = _present(
        context, context.xpath_item_title, description)
    context.item_title = item_title.text


@then('Add the item to cart if there is an option')
def add_to_cart(context):
    xpath_add_to_cart_button = "//a[@id = 'atcRedesignId_btn']"
    xpath_item_added_modal = "//div[@class = 'vi-overlayTitleBar']"
    description = "Add to cart button"

    _click(context, xpath_add_to_cart_button, description)
    context.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, xpath_item_added_modal)))
    sleep(.2)
    context.driver.close()
    context.driver.switch_to.window(context.window_before)


@when('Hover over cart')
def hover_over_cart(context):
    xpath_cart = "//li[@id = 'gh-minicart-hover']"
    description = "Cart icon"

    _move(context, xpath_cart, description)


@then('Verify the title of the item in mini cart')
def verify_item_in_cart(context):
    xpath_title_in_minicart = \
        "//span[parent::div/@class = 'gh-info__title']"

    title_in_mini_cart = context.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, xpath_title_in_minicart)))

    assert title_in_mini_cart.text == context.item_title, \
        "Item's title found in mini cart does not match the original title"


# --- Search specific items on auction and save pictures of them
# --- in a created directory


@given('Save directory to create, {item}')
def save_data(context, item):
    context.xpath_input_field = "//input[@id = 'gh-ac']"
    context.xpath_search_button = "//input[@id = 'gh-btn']"
    context.xpath_header_one = "//h1[@class = 'srp-controls__count-heading']"
    context.item = item
    context.dir = context.text


@then('Verify correct search')
def verify_searched_item(context):
    assert context.wait.until(EC.text_to_be_present_in_element(
        (By.XPATH, context.xpath_header_one), context.item)), \
        "Header one does not contain correct search"


@when('Sort listings by central left {option}')
def sort_listings_by_central_left_option(context, option):
    xpath_sort_listings_option = \
        f"//span[text() = '{option}']" \
        f"[ancestor::ul[@class='fake-tabs__items']]"
    description = f"Sort listings by {option} button"

    _click(context, xpath_sort_listings_option, description)


@when('Filter and collect items: {price_max}, {price_min}, '
      '{ship_price_max}, {bidding_min_days_left}')
def collect_filter_items(context, price_max, price_min,
                         ship_price_max, bidding_min_days_left):
    xpath_links_for_filtered_items = \
        f"//div[contains(@class, 's-item__details')]" \
        f"[translate(.//span/text(), '$', '') > {price_min} and " \
        f"translate(.//span/text(), '$', '') < {price_max}]" \
        f"[.//span[contains(text(),'Free shipping') or " \
        f"translate(substring-before(., ' shipping'), '+$', '') <= " \
        f"{ship_price_max}]][.//span[@class = 's-item__time-left' and " \
        f"substring-before(., 'd') > {bidding_min_days_left}]]" \
        f"/preceding-sibling::a"
    description = f"Filtered {context.item} collection"

    context.watch_links = _collect(
        context, xpath_links_for_filtered_items, description)


@when('Cleanup/create a directory for saving files in project root')
def create_dir(context):
    if Path(f"./{context.dir}").is_dir():
        shutil.rmtree(f"./{context.dir}")
    Path(f"./{context.dir}").mkdir(parents=True, exist_ok=True)


@then('Open items in a new tab and save screenshots in the directory')
def save_screenshots(context):
    for count, watch_link in enumerate(context.watch_links):
        context.xpath_el_new_tab = watch_link
        open_element_in_new_tab(context)
        context.driver.save_screenshot(
            f"./{context.dir}/selected_item_picture_{count}.png")
        context.driver.close()
        context.driver.switch_to.window(context.window_before)


# --- Verify Recent searches in suggested search menu


@given('Main search field')
def save_data(context):
    context.xpath_input_field = "//input[@id = 'gh-ac']"
    context.xpath_search_button = "//input[@id = 'gh-btn']"
    context.xpath_header_one = "//h1[@class = 'srp-controls__count-heading']"
    context.xpath_titles = "//h3[@class = 's-item__title']" \
                           "[ancestor::div/@id = 'mainContent']"


@when('Go back')
def go_back(context):
    context.driver.back()
    sleep(.2)


@when('Find the first Recent searches element in suggested search')
def find_suggested_one(context):
    xpath_suggested_one = "//li[contains(@class, 'ui-menu-item')]/a[1]"
    description = "First element in suggested search"

    sleep(.2)
    context.suggested_one = _present(
        context, xpath_suggested_one, description)


@then('Verify that first "Recent searches" element == {item_full_name}')
def verify_suggested_recent(context, item_full_name):
    suggested_one_aria_label = \
        context.suggested_one.get_attribute("aria-label")

    suggested_one_aria_label | should.have.contain("Recent searches"), \
        "Recent searches are not displayed at the top of the suggested list"
    context.suggested_one.text | should.have.contain(context.item.split()), \
        "Recent searches doesn't suggest the earliest recent search at the top"


# --- Verify image rendering, HTTP response, appearance on the page


@given('A directory to create, {item}')
def save_data(context, item):
    context.dir = context.table[0]['directory']
    context.xpath_select_category = "//select[@id = '_in_kw']"
    context.xpath_input_field = "//input[@id = '_nkw']"
    context.xpath_search_button = \
        "//button[.='Search']" \
        "[following-sibling::span/@id = 'searchBtnUpperNoScript']"
    context.xpath_header_one = "//h1[@class = 'rsHdr']"
    context.xpath_beautiful_thing_images = \
        "//img[ancestor::div[@id = 'vi_main_img_fs']]"
    context.image_bytes = []
    context.item = "\" \"".join(tuple(item.split()))


@when('Open advanced search')
def open_advanced(context):
    xpath_advanced_search = "//a[@id = 'gh-as-a']"
    description = "Advanced search link"

    _click(context, xpath_advanced_search, description)


@when('Sort by central right {option}')
def sort_by_central_right_option(context, option):
    xpath_central_right_first_dropdown = \
        "//a[contains(@class, 'dropdown-toggle')][1]"
    xpath_central_right_first_dropdown_option = \
        f"//a[text() = '{option}' and " \
        f"ancestor::ul/@id = 'SortMenu']"
    description = f"Central right sort dropdown"

    _move(context, xpath_central_right_first_dropdown, description)
    _click(context,xpath_central_right_first_dropdown_option,
           description + f": {option}")


@when('Open the first found item')
def open_first_item(context):
    xpath_very_beautiful_item = "//img[@class = 'img'][1]"
    description = "First found item's image"

    _click(context, xpath_very_beautiful_item, description)


@then('Collect the images of the item')
def collect_images(context):
    description = "Item's all images"

    context.gorgeous_images = _collect(
        context, context.xpath_beautiful_thing_images, description)


@then('Verify the images are getting 200 HTTP response')
def verify_images_response(context):
    mismatch_status_code = []
    for gorgeous_image in context.gorgeous_images:
        img_link = gorgeous_image.get_attribute("src")
        response = requests.get(img_link)
        context.image_bytes.append(BytesIO(response.content))
        if response.status_code != 200:
            mismatch_status_code.append(response.status_code)

    if mismatch_status_code:
        raise AssertionError(
            f"Some images delivered response code of {mismatch_status_code} ")


@then('Verify that downloaded images size > 0')
def verify_images_size(context):
    mismatch_img_byte = []
    img, img_name = '', ''

    for count, byte in enumerate(context.image_bytes):
        img_name = f"gorgeous_image_{count}.png"
        img = Image.open(byte)
        if not img:
            mismatch_img_byte.append({img_name: img})

    if mismatch_img_byte:
        raise ValueError(
            f"Some images stored in bytes are not opening: {mismatch_img_byte}")

    assert 0 not in img.size, f"Oops - {img_name} size is zero"


@when('Open image gallery')
def open_image_gallery(context):
    xpath_image_area = "//img[@id='icImg']"
    description = "Image clickable area"

    _click(context, xpath_image_area, description)


@when('Collect gallery images')
def collect_gallery_images(context):
    xpath_gallery_images = \
        "//button[starts-with(@id, 'viEnlargeImgLayer_layer_fs_thImg')]"
    description = 'Gallery images'

    context.gorgeous_gallery_images = \
        _collect(context, xpath_gallery_images, description)


@then('Verify the images are rendered and displayed')
def verify_images_displayed(context):
    xpath_gallery_right_arrow = "//a[@title = 'To Next Image']"
    xpath_gallery_central_image = "// img[@id = 'viEnlargeImgLayer_img_ctr']"
    description_click = "Image gallery right arrow button"
    description_present = "Gallery central image"
    mismatch_img_size = []

    for image in range(len(context.gorgeous_gallery_images) - 1):
        gallery_central_image = _present(
            context, xpath_gallery_central_image, description_present)
        styles = gallery_central_image.get_attribute("style").split()
        width, height = \
            styles[1].replace("px;", ""), styles[3].replace("px;", "")

        if int(float(width)) < 500 and int(float(height)) < 500:
            mismatch_img_size.append({image: [width, height]})

        _click(context, xpath_gallery_right_arrow, description_click)
    if mismatch_img_size:
        raise AssertionError(
            f"The size of some image in the gallery is incorrect: "
            f"{mismatch_img_size}")


@then('Verify the left arrow button of the gallery')
def verify_left_arrow(context):
    xpath_gallery_left_arrow = "//a[@title='To Previous Image']"
    description = "Image gallery left arrow button"

    for image in range(len(context.gorgeous_gallery_images) - 1):
        _click(context, xpath_gallery_left_arrow, description)


# --- Verify navigation links redirection


@given('Links -> Titles to verify')
def save_data(context):
    context.dict = json.loads(context.text)


@when('Open navigation link {link_name}')
def open_link(context, link_name):
    context.key = link_name
    xpath_link = \
        f"//a[parent::li/@class = 'hl-cat-nav__js-tab']" \
        f"[text() = '{link_name}']"
    description = f"Navigation link {link_name}"

    _click(context, xpath_link, description)


@then('Verify correct redirection with title')
def verify_title(context):
    assert context.driver.title == context.dict[context.key], \
        f"Title of the page directed from {context.key} is not verified"


# --- Verify navigation links redirection


@when('Collect listing titles')
def collect_titles(context):
    description = "Listing titles"

    context.titles = _collect(context, context.xpath_titles, description)


@then('Calculate result match')
def calculate_result_match(context):
    context.keywords = context.item.split()
    context.titles_match, context.total_match, match = 0, 0, 0

    for title in context.titles:
        for word in context.keywords:
            if word.lower() in title.text.lower():
                match += 1
        if match == 3:
            context.titles_match += 1
        context.total_match += match
        match = 0


@then('Verify match score > {min_match_score} and '
      'full title match score > {min_full_title_match_score}')
def test_verify_match(context, min_match_score, min_full_title_match_score):
    match_max = len(context.titles) * len(context.keywords)
    titles_match_max = len(context.titles)

    match = context.total_match / match_max * 100
    full_title_match = context.titles_match / titles_match_max * 100

    assert match > int(min_match_score), \
        "This search does not satisfy min match score parameter"
    assert full_title_match > int(min_full_title_match_score), \
        "This search does not satisfy min full title match score parameter"


# --- Search for a specific item with details and verfify results


@then('Verify all listing titles contain the '
      '{main_search} with important {main_details}')
def verify_main_search(context, main_search, main_details):
    main_search = main_search.lower() + ' ' + main_details.lower()
    context.title_tokens, mismatch_titles = [], []

    for title in context.titles:
        remove_special_chars = \
            title.text.translate(
                {ord(c): " " for c in emoji.UNICODE_EMOJI['en'].keys()
                 if len(c) == 1})
        title_tokens = re.split(r"\s+|/|\(|\)|\+|\*|-",
                                remove_special_chars.lower())
        context.title_tokens.append(title_tokens)
        match_tokens = re.split(r"\s+", main_search)

        if set(title_tokens) & set(match_tokens) is False:
            mismatch_titles.append(title)
    if mismatch_titles:
        raise AssertionError(
            f"Some titles don't match the main search: {mismatch_titles}")


@then('Verify all items contain some of "{other_details}"')
def verify_main_search(context, other_details):
    details = other_details.lower()
    mismatch = []

    for count, tokens in enumerate(context.title_tokens):
        match_tokens = re.split(r"\s+", details)
        if any(word in tokens for word in match_tokens) is False:
            mismatch.append(tokens)

    if mismatch:
        raise AssertionError(f"Some titles doesn't match the other details")


# Helper Functions


def _click(context, xpath, description):
    """Opens WebDriver element.

    Args:
        context (obj): Behave object
        xpath (str): locator of the element
        description (str): description of the element

    """
    try:
        element = context.wait.until(
            EC.element_to_be_clickable((By.XPATH, xpath)))
    except TimeoutException as e:
        err_msg = f"{description} element is not clickable"
        raise NoSuchElementException(err_msg) from e
    else:
        err_msg = f"Cannot click on the element {description}"
        try:
            element.click()
            sleep(.2)
        except ElementClickInterceptedException(err_msg):
            raise
    return element


def _collect(context, xpath, description):
    """Collects WebDriver elements.

    Args:
        context (obj): Behave object
        xpath (str): locator of the elements
        description (str): description of the element

    """
    try:
        element = context.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))
        sleep(.2)
    except TimeoutException as e:
        err_msg = f"{description} element is not present on the page"
        raise NoSuchElementException(err_msg) from e
    else:
        return element


def _type(context, xpath, text):
    """Types text into input.

    Args:
        context (obj): Behave object
        xpath (str): locator of the input field
        text (str): text to type

    """
    description = "Search input field"

    search_input = _present(context, xpath, description)
    sleep(.2)
    search_input.clear()
    search_input.send_keys(text)
    context.wait.until(
        lambda browser: search_input.get_attribute('value') == text)


def _select(context, xpath, option):
    """Selects an option.

    Args:
        context (obj): Behave object
        xpath (str): locator of the select element
        option (str): option to choose

    """
    description = f"Select element with {option} option"
    element = _present(context, xpath, description)
    try:
        select = Select(element)
        select.select_by_visible_text(option)
        sleep(.2)
    except NoSuchElementException:
        err_msg = f"Cannot _select {option}"
        raise ElementNotSelectableException(err_msg)


def _present(context, xpath, description):
    """Checks the presence of the WebDriver element.

    Args:
        context (obj): Behave object
        xpath (str): locator of the element
        description (str): description of the element

    """
    try:
        element = context.wait.until(
            EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException as e:
        err_msg = f"{description} element is not _present on the page"
        raise NoSuchElementException(err_msg) from e
    else:
        return element


def _move(context, xpath, description):
    """Checks the presence of the WebDriver element.

    Args:
        context (obj): Behave object
        xpath (str): locator of the element
        description (str): description of the element

    """
    element = _present(context, xpath, description)
    try:
        actions = ActionChains(context.driver)
        actions.move_to_element(element)
        actions.perform()
    except MoveTargetOutOfBoundsException(
            f"Cannot move to element {description}"):
        raise
