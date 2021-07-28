from behave import *
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


@given(u'Main Search data')
def step_impl(context):
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.amazon.com")
    context.wait = WebDriverWait(context.driver, 10, 0.25)


@when(u'Collect the list of category urls')
def step_impl(context):
    x_categories = "//div[contains(@class, 'first-carousel')]//a[@class = 'a-link-normal']"

    context.categories = context.wait.until(EC.presence_of_all_elements_located((By.XPATH, x_categories)))
    context.urls_and_titles = []
    for item in context.categories:
        url = item.get_attribute("href")
        img = item.find_element_by_xpath("./img")
        title = img.get_attribute("alt")
        tuple_url_title = (url, title)
        context.urls_and_titles.append(tuple_url_title)


@then(u'Verify homework categories titles')
def step_impl(context):
    mismatch = []
    count = 0
    for url, title in context.urls_and_titles:
        window_before = context.driver.current_window_handle
        context.driver.execute_script(f"window.open(\"{url}\");")
        context.wait.until(EC.number_of_windows_to_be(2))
        window_after = context.driver.window_handles[-1]
        context.driver.switch_to.window(window_after)
        page_title = context.driver.title
        if title.lower() not in page_title.lower():
            mismatch.append(f"Title {title} is not the same on the category page")

        context.driver.close()
        context.driver.switch_to.window(window_before)
        count += 1
    if count != len(context.urls_and_titles):
        raise ValueError(f"We did not check all the items:\nEspected: {len(context.urls_and_titles)}\nActual: {count}")
    if mismatch:
        raise ValueError(f"Some titles don't match:\n{mismatch}")
