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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


# --- Verify Hero carousel functionality


@given('Hero carousel slides are collected')
def collect_carousel_slides(context):
    context.xpath_hero_carousel_slides = \
        "//li[contains(@class, 'carousel__snap-point')]" \
        "[ancestor::div[contains(@class, 'carousel__autoplay')]]"
    carousel_slides = "carousel_slides"

    context.hero_carousel_slides = \
        _collect(context, context.xpath_hero_carousel_slides, carousel_slides)


@then('Autoplay and verify carousel correct slide appearance')
def autoplay_verify_carousel(context):
    context.count = 0
    context.total_count = len(context.hero_carousel_slides) - 1
    sleep(1)
    for slide in context.hero_carousel_slides:
        slide_apearence = slide.get_attribute("aria-hidden")
        assert slide_apearence is None
        if context.count != context.total_count:
            sleep(3.3)
        else:
            sleep(1)
            break
        context.count += 1


@when('Click carousel play/pause button and track slides')
def verify_carousel_play_pause(context):
    xpath_play_pause_button = \
        "//button[contains(@class, 'carousel__playback')]"
    xpath_play_pause_class = \
        "//*[name() = 'svg']" \
        "[parent::button/@class = 'carousel__playback']"
    play_pause = "play_pause"

    play_pause_button = \
        _click(context, xpath_play_pause_button)
    play_pause_class = \
        _presence(context, xpath_play_pause_class, play_pause)
    status_class = play_pause_class.get_attribute("class")
    play, pause = 0, 0
    if "icon--play" in status_class:
        play = 1
    elif "icon--pause" in status_class:
        pause = 1
    if context.count == context.total_count and play == 1:
        context.count = 0
    elif 0 <= context.count < context.total_count and play == 1:
        context.count += 1
    elif pause == 1:
        play_pause_button.click()
        sleep(1)
        return
    play_pause_button.click()


@then('Verify carousel correct slide appearance')
def verify_carousel_slide(context):
    carousel_slides = "carousel_slides"
    sleep(.2)

    context.hero_carousel_slides = \
        _collect(context, context.xpath_hero_carousel_slides, carousel_slides)
    slide = context.hero_carousel_slides[context.count]
    slide_apearence = slide.get_attribute("aria-hidden")
    assert slide_apearence is None


@when('Click carousel left button and track slides')
def click_carousel_left(context):
    xpath_left_arrow_button = \
        "//button[contains(@class, 'carousel__control')]" \
        "[ancestor::div[contains(@class, 'carousel__autoplay')]][1]"

    if context.count == 0:
        context.count = context.total_count
    elif 0 < context.count <= context.total_count:
        context.count -= 1
    _click(context, xpath_left_arrow_button)


@when('Click carousel right button and track slides')
def click_carousel_right(context):
    xpath_right_arrow_button = \
        "(//button[contains(@class, 'carousel__control')]" \
        "[ancestor::div[contains(@class, 'carousel__autoplay')]])[2]"

    if context.count == context.total_count:
        context.count = 0
    elif 0 <= context.count < context.total_count:
        context.count += 1
    _click(context, xpath_right_arrow_button)


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
    _click(context, context.xpath_search_button)


@when('Find first item to open in a new tab')
def open_first_item(context):
    xpath_first_item_with_buy_option = \
        "(//div[contains(@class, 's-item__info')]" \
        "[.//span/text() = 'Buy It Now']/a)[1]"
    context.xpath_el_new_tab = xpath_first_item_with_buy_option


@when('Open element in a new tab')
def open_element_in_new_tab(context):
    element = "element_to_open"
    if isinstance(context.xpath_el_new_tab, str):
        element = _presence(
            context, context.xpath_el_new_tab, element)
    else:
        element = context.xpath_el_new_tab
    sleep(.2)
    context.window_before = context.driver.window_handles[0]
    actions = ActionChains(context.driver)
    actions.move_to_element(
        element).key_down(
        Keys.COMMAND).click().key_up(
        Keys.COMMAND).perform()
    sleep(.2)
    WebDriverWait(context.driver, context.delay).until(
        EC.number_of_windows_to_be(2))
    window_after = context.driver.window_handles[1]
    context.driver.switch_to_window(window_after)


@then('Get the title of the item')
def get_title(context):
    title = "title"

    item_title = _presence(
        context, context.xpath_item_title, title)
    context.item_title = item_title.text


@then('Add the item to cart if there is an option')
def add_to_cart(context):
    xpath_add_to_cart_button = "//a[@id = 'atcRedesignId_btn']"
    xpath_item_added_modal = "//div[@class = 'vi-overlayTitleBar']"
    try:
        _click(context, xpath_add_to_cart_button)
        WebDriverWait(context.driver, context.delay).until(
            EC.visibility_of_element_located((By.XPATH, xpath_item_added_modal)))
        sleep(.2)
    except TimeoutException:
        context.scenario.skip(reason='This item has no "Add to cart" option')
    context.driver.close()
    context.driver.switch_to.window(context.window_before)


@when('Hover over cart')
def hover_over_cart(context):
    xpath_cart = "//li[@id = 'gh-minicart-hover']"

    mini_cart = WebDriverWait(
        context.driver, context.delay
    ).until(EC.element_to_be_clickable(
        (By.XPATH, xpath_cart)))
    actions = ActionChains(context.driver)
    actions.move_to_element(mini_cart).perform()


@then('Verify the title of the item in mini cart')
def verify_item_in_cart(context):
    xpath_title_in_minicart = "//span[parent::div/@class = 'gh-info__title']"

    title_in_mini_cart = WebDriverWait(
        context.driver, context.delay).until(
        EC.visibility_of_element_located(
            (By.XPATH, xpath_title_in_minicart)))

    title_in_mini_cart.text | should.be.equal(context.item_title)


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
    check = WebDriverWait(context.driver, context.delay).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, context.xpath_header_one), context.item))

    check | should.be.equal.to(True)


@when('Sort listings by central left {option}')
def sort_listings_by_central_left_option(context, option):
    xpath_sort_listings_option = \
        f"//span[text() = '{option}']" \
        f"[ancestor::ul[@class='fake-tabs__items']]"

    try:
        _click(context, xpath_sort_listings_option)
    except TimeoutException:
        print(f"Cannot sort Listings by {option}")


@when('Filter and collect items: {price_max}, {price_min}, '
      '{ship_price_max}, {bidding_min_days_left}')
def collect_filter_items(context, price_max, price_min,
                         ship_price_max, bidding_min_days_left):
    xpath_links_for_filtered_items = \
        f"//div[contains(@class, 's-item__details')][translate(.//span/text(), '$', '')" \
        f" > {price_min} and translate(.//span/text(), '$', '') < {price_max}]" \
        f"[.//span[contains(text(),'Free shipping') or " \
        f"translate(substring-before(., ' shipping'), '+$', '') " \
        f"<= {ship_price_max}]][.//span[@class = 's-item__time-left' " \
        f"and substring-before(., 'd') > {bidding_min_days_left}]]/preceding-sibling::a"

    filtered_items = ''

    context.watch_links = _collect(
        context, xpath_links_for_filtered_items, filtered_items)
    if context.watch_links is None:
        context.scenario.skip(reason='No items found by with these filteres')


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


@given('Set up necessary data')
def save_data(context):
    context.xpath_input_field = "//input[@id = 'gh-ac']"
    context.xpath_search_button = "//input[@id = 'gh-btn']"


@when('Go back')
def go_back(context):
    context.driver.back()
    sleep(.2)


@when('Find the first Recent searches element in suggested search')
def find_suggested_one(context):
    xpath_suggested_one = "//li[contains(@class, 'ui-menu-item')]/a[1]"
    suggested_one = "suggested_one"

    sleep(.2)
    context.suggested_one = _presence(
        context, xpath_suggested_one, suggested_one)


@then('Verify that first "Recent searches" element == {item_full_name}')
def verify_suggested_recent(context, item_full_name):
    suggested_one_aria_label = \
        context.suggested_one.get_attribute("aria-label")

    suggested_one_aria_label | should.have.contain("Recent searches")
    context.suggested_one.text | should.have.contain(context.item.split())


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

    _click(context, xpath_advanced_search)


@when('Sort by central right {option}')
def sort_by_central_right_option(context, option):
    xpath_central_right_first_dropdown = \
        "//a[contains(@class, 'dropdown-toggle')][1]"
    xpath_central_right_first_dropdown_option = \
        f"//a[text() = '{option}' and " \
        f"ancestor::ul/@id = 'SortMenu']"

    central_right_first_dropdown = WebDriverWait(
        context.driver, context.delay
    ).until(EC.element_to_be_clickable(
        (By.XPATH, xpath_central_right_first_dropdown)))
    actions = ActionChains(context.driver)
    actions.move_to_element(central_right_first_dropdown).perform()
    _click(context, xpath_central_right_first_dropdown_option)


@when('Open the first found item')
def open_first_item(context):
    xpath_very_beautiful_item = "//img[@class = 'img'][1]"

    _click(context, xpath_very_beautiful_item)


@then('Collect the images of the item')
def collect_images(context):
    all_item_images = 'all_item_images'

    context.gorgeous_images = _collect(
        context, context.xpath_beautiful_thing_images, all_item_images)


@then('Verify the images are getting 200 HTTP response')
def verify_images_response(context):
    for gorgeous_image in context.gorgeous_images:
        img_link = gorgeous_image.get_attribute("src")
        response = requests.get(img_link)
        context.image_bytes.append(BytesIO(response.content))

        response.status_code | should.be.equal.to(200), \
            f"{img_link} delivered response code of {response.status_code}"


@then('Verify that downloaded images size > 0')
def verify_images_size(context):
    for count, byte in enumerate(context.image_bytes):
        img_name = f"gorgeous_image_{count}.png"
        img = Image.open(byte)

        img.size | should.do_not.contain(0), f"Oops - {img_name} is broken"


@when('Open image gallery')
def open_image_gallery(context):
    xpath_image_area = "//img[@id='icImg']"

    _click(context, xpath_image_area)


@when('Collect gallery images')
def collect_gallery_images(context):
    xpath_gallery_images = \
        "//button[starts-with(@id, 'viEnlargeImgLayer_layer_fs_thImg')]"
    gallery_images = 'gallery_images'

    context.gorgeous_gallery_images = \
        _collect(context, xpath_gallery_images, gallery_images)


@then('Verify the images are rendered and displayed')
def verify_images_displayed(context):
    xpath_gallery_right_arrow = "//a[@title = 'To Next Image']"
    xpath_gallery_central_image = "// img[@id = 'viEnlargeImgLayer_img_ctr']"

    for image in range(len(context.gorgeous_gallery_images) - 1):
        gallery_central_image = "gallery_central_image"

        gallery_central_image = _presence(
            context, xpath_gallery_central_image, gallery_central_image)
        styles = gallery_central_image.get_attribute("style").split()
        width, height = styles[1].replace("px;", ""), styles[3].replace("px;", "")

        assert int(float(width)) > 500 and int(float(height)) > 500, \
            f"The size (width: {width}, height: {height}) of the image #{image} in the gallery is incorrect"

        _click(context, xpath_gallery_right_arrow)


@then('Verify the left arrow button of the gallery')
def verify_left_arrow(context):
    xpath_gallery_left_arrow = "//a[@title='To Previous Image']"

    for image in range(len(context.gorgeous_gallery_images) - 1):
        _click(context, xpath_gallery_left_arrow)


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
    try:
        _click(context, xpath_link)
    except TimeoutException:
        print(f"Cannot open navigation link {link_name}")


@then('Verify correct redirection with title')
def verify_title(context):
    assert context.driver.title == context.dict[context.key], \
        f"Title of the page directed from {context.key} is not verified"


# --- Verify navigation links redirection

@given('Data for navigation')
def save_data(context):
    context.xpath_input_field = "//input[@id = 'gh-ac']"
    context.xpath_search_button = "//input[@id = 'gh-btn']"
    context.xpath_header_one = "//h1[@class = 'srp-controls__count-heading']"
    context.xpath_titles = "//h3[@class = 's-item__title']" \
                           "[ancestor::div/@id = 'mainContent']"


@when('Collect listing titles')
def collect_titles(context):
    titles = "titles"
    context.titles = _collect(context, context.xpath_titles, titles)


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

    assert match > int(min_match_score)
    assert full_title_match > int(min_full_title_match_score)


# ----- Search for a specific item with details and verfify results


@given('Some data stored')
def some_data(context):
    context.xpath_input_field = "//input[@id = 'gh-ac']"
    context.xpath_search_button = "//input[@id = 'gh-btn']"
    context.xpath_header_one = "//h1[@class = 'srp-controls__count-heading']"
    context.xpath_titles = \
        "//span[parent::h1[@class = 'srp-controls__count-heading']][2]"


@then('Verify all listing titles contain the '
      '{main_search} with important {main_details}')
def verify_main_search(context, main_search, main_details):
    main_search = main_search.lower() + ' ' + main_details.lower()
    for title in context.titles:
        remove_special_chars = \
            title.text.translate(
                {ord(c): " " for c in emoji.UNICODE_EMOJI['en'].keys()
                 if len(c) == 1})
        title_tokens = re.split(r"\s+|/|\(|\)|\+|\*|-",
                                remove_special_chars.lower())
        match_tokens = re.split(r"\s+", main_search)

        assert set(title_tokens) & set(match_tokens), \
            "Some titles don't match the main search"


# --- Verify Advanced Search


@given('Data stored for Advanced Search')
def saved_data(context):
    context.xpath_input_field = "//input[@name = '_nkw']"
    context.xpath_search_button = "//button[@id = 'searchBtnLowerLnk']"
    context.xpath_titles = "//a[parent::h3[@class = 'lvtitle']]"


@when('In keywords options select {keyword_option}')
def select_keywords_options(context, keyword_option):
    xpath_keywords_options = "//select[@id = '_in_kw']"
    print(keyword_option)
    _select(context, xpath_keywords_options, keyword_option)


@when('In Price put from {min_price} to {max_price}')
def price_option(context, min_price, max_price):
    xpath_min_price = "//input[@name = '_udlo']"
    xpath_max_price = "//input[@name = '_udhi']"

    _type(context, xpath_min_price, min_price)
    _type(context, xpath_max_price, max_price)


@when('Check {option}')
def check_option(context, option):
    xpath_checkbox = f"//input[starts-with(@id, 'LH')][@type = 'checkbox']" \
                     f"[following-sibling::node()[normalize-space() = '{option}']]"

    _click(context, xpath_checkbox)


@when('In Location select {max_miles} miles of {index}')
def price_option(context, max_miles, index):
    xpath_located_max_miles = "//select[@id = '_sadis']"
    xpath_located_index = "//input[@name = '_stpos']"
    context.index = index

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


@then('Verfiy number of results is <= {number_results:d}')
def verify_number(context, number_results):
    xpath_listings = "//ul[@id='ListViewInner']/li"
    listings = "listings"

    listings = _collect(context, xpath_listings, listings)

    assert len(listings) <= number_results, \
        f"The number of listings on the page " \
        f"should be {number_results} but {len(listings)} instead"


@then('Verify listings sorted by Distance: nearest first and the index is correct')
def verify_number(context):
    xpath_distance = "//ul[contains(@class, 'lvdetails')]/li[1]"
    ship_distance = "ship_distance"
    dist = []

    ship_distance = _collect(context, xpath_distance, ship_distance)
    for item in ship_distance:
        text_split = item.text.split()
        if text_split[0] == "<":
            n = text_split[1].replace(",", "")
            dist.append(int(n))
        else:
            n = text_split[0].replace(",", "")
            dist.append(int(n))
        assert text_split[-1] == context.index, \
            f"Index of users location should be {context.index} but {text_split[-1]} instead"

    assert all(dist[i] <= dist[i + 1] for i in range(len(dist) - 1)), \
        "The listings are not sorted by 'nearest first'"


@then('Verify the price of the listing on the page is from 50 to 500')
def verify_price(context):
    xpath_items_price = "//span[parent::li[contains(@class, 'lvprice')]]"
    prices = "prices"

    prices = _collect(context, xpath_items_price, prices)
    print(prices)
    for price in prices:
        price = price.text.replace("$", "")
        if "to" in price:
            price_from, price_to = price.split("to")
            assert 50 < int(float(price_from)) < 500 or \
                   50 < int(float(price_to)) < 500, \
                   f"The price {price} is out of range"
        else:
            assert 50 < int(float(price)) < 500, \
                f"The price {price} is out of range"


@then('Verify that titles contain exact words grill and portable')
def verify_words(context):
    for title in context.titles:
        text = title.text.lower().split()
        words = ["grill", "portable"]
        assert set(words) & set(text), \
            f"Title {title} does not contain exact words"


# Helper Functions


def _click(context, xpath):
    """Opens WebDriver element.

    Args:
        context (obj): Behave object
        xpath (str): locator of the element

    """
    element = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath)))
    element.click()
    sleep(.2)
    return element


def _collect(context, xpath, name):
    """Collects WebDriver elements.

    Args:
        context (obj): Behave object
        xpath (str): locator of the elements
        name (str): name of the collection

    """
    try:
        name = WebDriverWait(
            context.driver, context.delay).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, xpath)))
        sleep(.2)
    except TimeoutException:
        print(f"Cannot collect {name}")
    else:
        return name


def _type(context, xpath, text):
    """Types text into input.

    Args:
        context (obj): Behave object
        xpath (str): locator of the input field
        text (str): text to type

    """
    search_input = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath)))
    sleep(.2)
    search_input.clear()
    search_input.send_keys(text)
    WebDriverWait(context.driver, context.delay).until(
        lambda browser: search_input.get_attribute('value') == text)


def _select(context, xpath, option):
    """Selects an option.

    Args:
        context (obj): Behave object
        xpath (str): locator of the select element
        option (str): optio0n to choose

    """
    element = ''

    try:
        element = WebDriverWait(
            context.driver, context.delay).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))
    except TimeoutException:
        print(f"Cannot select {option} category")
    finally:
        select = Select(element)
        select.select_by_visible_text(option)
    sleep(.2)


def _presence(context, xpath, name):
    """Checks the presence of the WebDriver element.

    Args:
        context (obj): Behave object
        xpath (str): locator of the element
        name (str): name to give

    """
    try:
        name = WebDriverWait(
            context.driver, context.delay).until(
            EC.presence_of_element_located(
                (By.XPATH, xpath)))
    except TimeoutException:
        print(f"{name} element is not present on the page")
    else:
        return name
