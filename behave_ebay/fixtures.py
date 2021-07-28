from behave import fixture
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.wait import WebDriverWait


@fixture
def browser_chrome(context):
    try:
        options = Options()
        options.add_argument("--window-size=1200,1080")
        context.driver = webdriver.Chrome(options=options)
        context.driver.set_window_position(0, 0)
        context.delay = 10
        context.driver.implicitly_wait(10)
        context.wait = WebDriverWait(context.driver, context.delay)
        yield context.driver
    except WebDriverException("Cannot start Chrome driver"):
        raise
    finally:
        context.driver.quit()


# Firefox: When use move_to() if the element is not in the viewport, you would have to manually scroll the page,
# executing javascript ( context.execute_script( window.scrollTo(...) ) ),
# otherwise you get MoveTargetOutOfBoundsException
# Chrome: It just works
@fixture
def browser_firefox(context):
    try:
        binary = FirefoxBinary()
        caps = DesiredCapabilities().FIREFOX
        caps["marionette"] = True
        context.driver = webdriver.Firefox(capabilities=caps, firefox_binary=binary)
        context.driver.set_window_position(0, 0)
        context.delay = 10
        context.driver.implicitly_wait(10)
        context.wait = WebDriverWait(context.driver, context.delay)
        yield context.driver
    except WebDriverException(f"Cannot start Firefox driver"):
        raise
    finally:
        context.driver.quit()


# Safari driver version is not supported with 2.46.
# Try downgrading Selenium Version:
# pip install -Iv selenium==2.45 or pip install selenium==2.45
@fixture
def browser_safari(context):
    try:
        context.driver = webdriver.Safari()
        context.driver.set_window_position(0, 0)
        context.delay = 10
        context.driver.implicitly_wait(10)
        context.wait = WebDriverWait(context.driver, context.delay)
        yield context.driver
    except WebDriverException(f"Cannot start Safari driver"):
        raise
    finally:
        context.driver.quit()
