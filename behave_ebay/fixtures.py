from behave import fixture
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options


@fixture
def browser_firefox(context):
    try:
        driver = webdriver.Firefox()
        print(driver)
        context.driver = driver
        context.driver.set_window_position(0, 0)
        yield context.driver
    except WebDriverException("Cannot start Firefox driver"):
        raise
    finally:
        context.driver.quit()


@fixture
def browser_chrome(context):
    try:
        options = Options()
        options.add_argument("--window-size=1920,1080")
        context.driver = webdriver.Chrome(options=options)
        context.driver.set_window_position(0, 0)
        yield context.driver
    except WebDriverException("Cannot start Chrome driver"):
        raise
    finally:
        context.driver.quit()

