from behave import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep


@given(u'Search environment')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.amazon.com")
    context.wait = WebDriverWait(context.driver, 10, 0.25)
    context.driver.implicitly_wait(10)


@when(u'Collect item\'s urls and prices on the main page')
def step_impl(context):
    x_items = "//div[contains(@id, 'desktop-')][.//h2/text() = 'Trending deals']//span[@class='a-list-item']"
    x_a_link = ".//a[@class='a-link-normal']"
    x_time_left = ".//span[contains(@class, 'dealAvailabilityMessage')]"
    x_min_price = ".//span[contains(@class, 'min-deal-price')]"
    x_max_price = ".//span[contains(@class, 'max-deal-price')]"
    x_next_slide = "//div[contains(@id, 'desktop-')][.//h2[text() = 'Trending deals']]//a[@aria-label='Carousel next slide']"
    sleep(1)
    items = context.wait.until(EC.presence_of_all_elements_located((By.XPATH, x_items)))
    context.items_data = []
    count = 0
    for item in items:
        count += 1
        print(count)
        sleep(.6)
        if count % 6 == 0:
            # sleep(333)
            next_slide = context.wait.until(EC.presence_of_element_located((By.XPATH, x_next_slide)))
            context.driver.execute_script("arguments[0].click();", next_slide)
            sleep(.6)
        # context.wait.until(EC.visibility_of(item))
        time_left = item.find_element_by_xpath(x_time_left)
        print(time_left.text)
        if time_left.text == "Deal has ended":
            continue
        context.wait.until(EC.visibility_of(item))
        url_link = item.find_element_by_xpath(x_a_link)
        url = url_link.get_attribute("href")
        print(url)
        context.wait.until(EC.visibility_of(item))
        min_price = item.find_element_by_xpath(x_min_price)
        print("price min found: ", min_price.text)
        min_price = min_price.text.strip("$")
        print(min_price)
        min_price = float(min_price)

        try:
            max_price = item.find_element_by_xpath(x_max_price)
        except NoSuchElementException:
            max_price = 0
        else:
            print("price max found: ", max_price)
            max_price = max_price.text.strip("$")
            print("price max found: ", max_price)
            # sleep(333)
            max_price = float(max_price)
        price = (min_price, max_price)
        context.items_data.append((url, price))
        print(context.items_data)
            # actions = ActionChains(context.driver)
            # actions.move_to_element(next_slide)
            # context.wait.until(EC.element_to_be_clickable((By.XPATH, x_next_slide)))
            # actions.click()
            # actions.perform()


@then(u'Verify that item prices are the same as on the main page')
def step_impl(context):
    mismatch = []
    for url, price in context.items_data:
        window_before = context.driver.current_window_handle
        context.driver.execute_script(f"window.open(\"{url}\");")
        context.wait.until(EC.number_of_windows_to_be(2))
        window_after = context.driver.window_handles[-1]
        context.driver.switch_to.window(window_after)
        collect_price(context)
        for mi, ma in price:
            if mi == 0 or ma == 0:
                continue
            if mi > context.price:
                mismatch.append(f"The min price advertised was: {mi}, but the actual price is {context.price}")
            elif ma > context.price:
                mismatch.append(f"The min price advertised was: {ma}, but the actual price is {context.price}")

        context.driver.close()
        context.driver.switch_to.window(window_before)

    if mismatch:
        raise ValueError(f"Some advertised prices are not correct:\n{mismatch}")


def collect_price(context):
    x_price = "//span[@id='priceblock_dealprice']"
    # x_options = "//li[@class='swatchAvailable']"

    context.price = context.wait.until(EC.presence_of_element_located((By.XPATH, x_price)))
