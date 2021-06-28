import shutil
import requests
from PIL import Image
from time import sleep
from io import BytesIO
from pathlib import Path
from grappa import should
from behave import when
from behave import then
from behave import given
from urllib.request import urlretrieve
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


################################################################
# # # # # # # # # # # #  SCENARIO  # # # # # # # # # # # # # # #

# Verify Hero carousel functionality

################################################################


@given('Hero carousel slides are collected')
def collect_carousel_slides(context):
    context.xpath_hero_carousel_slides = \
        "//li[contains(@class, 'carousel__snap-point')" \
        " and (ancestor::div[contains(@class, 'carousel__autoplay')])]"

    context.hero_carousel_slides = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, context.xpath_hero_carousel_slides)))


@then('Autoplay and verify carousel correct slide appearance')
def autoplay_verify_carousel(context):
    context.count = 0
    for slide in context.hero_carousel_slides:
        slide_apearence = slide.get_attribute("aria-hidden")
        slide_apearence | should.be.equal.to(None)
        if context.count != 2:
            sleep(3.43)  # the timing may vary
        else:
            sleep(1)
            break
        context.count += 1


@when('Click carousel play/pause button and track slides')
def verify_carousel_play_pause(context):
    xpath_hero_carousel_play_pause_button = \
        "//button[contains(@class, 'carousel__playback')]"
    xpath_play_pause_class = \
        "//*[name() = 'svg' and (contains(@class, 'icon--play') " \
        "or contains(@class, 'icon-pause'))]"

    hero_carousel_play_pause_button = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_hero_carousel_play_pause_button)))
    hero_carousel_play_pause_button.click()
    sleep(1)
    play_pause_class = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath_play_pause_class)))
    status_class = play_pause_class.get_attribute("class")
    play, pause = 0, 0
    if "icon--play" in status_class:
        play = 1
    elif "icon--pause" in status_class:
        pause = 1
    if context.count == 2 and play == 1:
        context.count = 0
    elif 0 <= context.count < 2 and play == 1:
        context.count += 1
    elif pause == 1:
        hero_carousel_play_pause_button.click()
        sleep(1)
        return
    hero_carousel_play_pause_button.click()


@then('Verify carousel correct slide appearance')
def verify_carousel_left(context):
    sleep(1)
    context.hero_carousel_slides = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, context.xpath_hero_carousel_slides)))
    slide = context.hero_carousel_slides[context.count]
    slide_apearence = slide.get_attribute("aria-hidden")

    slide_apearence | should.be.equal.to(None)


@when('Click carousel left button and track slides')
def verify_carousel_left(context):
    xpath_hero_carousel_left_arrow_button = \
        "(//button[contains(@class, 'carousel__control') " \
        "and (ancestor::div[contains(@class, 'carousel__autoplay')])])[1]"

    if context.count == 0:
        context.count = 2
    elif 0 < context.count <= 2:
        context.count -= 1
    hero_carousel_left_arrow_button = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_hero_carousel_left_arrow_button)))
    hero_carousel_left_arrow_button.click()


@when('Click carousel right button and track slides')
def verify_carousel_right(context):
    xpath_hero_carousel_right_arrow_button = \
        "(//button[contains(@class, 'carousel__control')" \
        " and (ancestor::div[contains(@class, 'carousel__autoplay')])])[2]"

    if context.count == 2:
        context.count = 0
    elif 0 <= context.count < 2:
        context.count += 1
    hero_carousel_right_arrow_button = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_hero_carousel_right_arrow_button)))
    hero_carousel_right_arrow_button.click()


######################################################
# # # # # # # # # # #  SCENARIO  # # # # # # # # # # #

# Add the first searched item to cart and verify that
# with it's title in mini cart

#######################################################


@given('Xpath saved in context')
def save_xpath_context(context):
    context.xpath_select_category = "//select[@id = 'gh-cat']"
    context.xpath_search_field = "//input[@id = 'gh-ac']"
    context.xpath_search_button = "//input[@id = 'gh-btn']"
    context.xpath_item_title = '//h1[@id = "itemTitle"]'


@when('Select "{category}"')
def choose_category(context, category):
    element = ''

    try:
        element = WebDriverWait(
            context.driver, context.delay).until(
            EC.presence_of_element_located(
                (By.XPATH, context.xpath_select_category)))
    except TimeoutException:
        print(f"Cannot select {category} category")
    finally:
        select = Select(element)
        select.select_by_visible_text(category)


@when('Type "{item}" in the search field')
def search_item(context, item):

    search_input = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_element_located(
            (By.XPATH, context.xpath_search_field)))
    search_input.send_keys(item)
    WebDriverWait(context.driver, context.delay).until(
        lambda browser: search_input.get_attribute('value') == item)


@when('Press search button')
def press_search_button(context):

    element = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, context.xpath_search_button)))
    element.click()


@when('Find first item to open in a new tab')
def add_to_cart(context):
    xpath_first_item_with_buy_option = \
        "(//div[contains(@class, 's-item__info')" \
        " and .//span/text() = 'Buy It Now']/a)[1]"

    context.xpath_el_new_tab = xpath_first_item_with_buy_option


@when('Open element in a new tab')
def open_element_in_new_tab(context):
    if isinstance(context.xpath_el_new_tab, str):
        element = WebDriverWait(
            context.driver, context.delay).until(
            EC.element_to_be_clickable(
                (By.XPATH, context.xpath_el_new_tab)))
    else:
        element = context.xpath_el_new_tab
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


@then('Get the title of the item')
def add_to_cart(context):
    context.item_title = WebDriverWait(
        context.driver, context.delay).until(
        EC.presence_of_element_located(
            (By.XPATH, context.xpath_item_title))
    ).text


@then('Add the item to cart if there is an option')
def add_to_cart(context):
    xpath_add_to_cart_button = "//a[@id = 'atcRedesignId_btn']"

    try:
        add_to_button = WebDriverWait(
            context.driver, context.delay
        ).until(EC.element_to_be_clickable(
            (By.XPATH, xpath_add_to_cart_button)))
        add_to_button.click()
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


############################################################
# # # # # # # # # # #  SCENARIO  # # # # # # # # # # # # # #

# Search specific items on auction and save pictures of them
# in a created directory

############################################################


@given('Save directory to create, "{item}"')
def save_data(context, item):
    context.xpath_search_field = "//input[@id = 'gh-ac']"
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


@when('Sort listings by central left "{option}"')
def sort_listings_by_left_option(context, option):
    xpath_sort_listings_option = \
        f"//span[text() = '{option}' and " \
        f"ancestor::ul[@class='fake-tabs__items']]"

    try:
        element = WebDriverWait(
            context.driver, context.delay).until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath_sort_listings_option)))
        element.click()
    except TimeoutException:
        print(f"Cannot sort Listings by {option}")


@when('Filter items: {price_max}, {price_min}, '
      '{ship_price_max}, {bidding_min_days_left}')
def filter_items(context, price_max, price_min,
                 ship_price_max, bidding_min_days_left):
    xpath_links_for_filtered_items = \
        f"//div[contains(@class, 's-item__details') and " \
        f"(translate(.//span/text(), '$', '') > {price_min} and " \
        f"translate(.//span/text(), '$', '') < {price_max}) and " \
        f"(.//span[(contains(text(),'Free shipping')) " \
        f"or translate(substring-before(., ' shipping'), '+$', '')" \
        f" <= {ship_price_max}]) and (.//span[@class='s-item__time-left'" \
        f" and substring-before(., 'd') > {bidding_min_days_left}])]" \
        f"/ancestor::div/a"

    try:
        context.watch_links = WebDriverWait(
            context.driver, context.delay).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, xpath_links_for_filtered_items)))
    except TimeoutException:
        print("Cannot collect filtered items")


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


######################################################################
# # # # # # # # # # # #  THIRD SCENARIO  # # # # # # # # # # # # # # #
######################################################################


@given('Set up Xpath in context')
def save_data(context):
    context.xpath_search_field = "//input[@id = 'gh-ac']"
    context.xpath_search_button = "//input[@id = 'gh-btn']"


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


@then('Verify that first "Recent searches" element == "{item_full_name}"')
def verify_suggested_recent(context, item_full_name):
    suggested_one_aria_label = \
        context.suggested_one.get_attribute("aria-label")

    suggested_one_aria_label | should.have.contain("Recent searches")
    suggested_one_aria_label | should.have.contain(item_full_name)


################################################################
# # # # # # # # # # # # #   SCENARIO   # # # # # # # # # # # # #

# Verify image rendering, HTTP response, appearance on the page

################################################################


@given('A directory to create, "{item}"')
def save_data(context, item):
    context.dir = context.table[0]['directory']
    context.xpath_select_category = "//select[@id = '_in_kw']"
    context.xpath_search_field = "//input[@id = '_nkw']"
    context.xpath_search_button = \
        "//button[.='Search' and following-sibling::span/@id = " \
        "'searchBtnUpperNoScript']"
    context.xpath_header_one = "//h1[@class = 'rsHdr']"
    context.xpath_beautiful_thing_images = \
        "//img[ancestor::div[@id = 'vi_main_img_fs']]"
    context.img_urls = []
    context.image_bytes = []
    context.item = "\" \"".join(tuple(item.split()))


@when('Open advanced search')
def open_advanced(context):
    xpath_advanced_search = "//a[@id = 'gh-as-a']"
    element = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_advanced_search)))
    element.click()


@when('Sort by central right "{option}"')
def sort_by_option(context, option):
    xpath_central_right_first_dropdown = \
        "(//a[contains(@class, 'dropdown-toggle')])[1]"
    xpath_central_right_first_dropdown_option = \
        f"//a[text() = '{option}' and " \
        f"ancestor::ul/@id = 'SortMenu']"

    central_right_first_dropdown = WebDriverWait(
        context.driver, context.delay
    ).until(EC.element_to_be_clickable(
        (By.XPATH, xpath_central_right_first_dropdown)))
    actions = ActionChains(context.driver)
    actions.move_to_element(central_right_first_dropdown).perform()
    central_right_first_dropdown_option = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_central_right_first_dropdown_option)))
    central_right_first_dropdown_option.click()


@when('Open the first found item')
def open_first_item(context):
    xpath_very_beautiful_item = "(//img[@class = 'img'])[1]"

    extremely_beautiful_thing = WebDriverWait(
        context.driver, context.delay).until(
        EC.element_to_be_clickable(
            (By.XPATH, xpath_very_beautiful_item)))
    extremely_beautiful_thing.click()


@then('Collect the images of the item')
def collect_images(context):
    try:
        context.gorgeous_images = WebDriverWait(
            context.driver, context.delay).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, context.xpath_beautiful_thing_images)))
    except TimeoutException:
        print("Cannot collect gorgeous images")


@then('Verify the images are getting 200 HTTP response')
def collect_images(context):
    for gorgeous_image in context.gorgeous_images:
        img_link = gorgeous_image.get_attribute("src")
        context.img_urls.append(img_link)
        response = requests.get(img_link)
        context.image_bytes.append(BytesIO(response.content))

        response.status_code | should.be.equal.to(200), \
            f"{img_link} delivered response code of {response.status_code}"


@then('Download images to a new directory and verify the size > 0')
def verify_images_size(context):
    for count, byte in enumerate(context.image_bytes):
        img_name = f"gorgeous_image_{count}.png"
        img_path = f"./{context.dir}/{img_name}"
        img = Image.open(byte)
        img.save(img_path)

        img.size | should.do_not.contain(0), f"Oops - {img_name} is broken"
