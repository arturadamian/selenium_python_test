from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from behave import fixture, use_fixture


def before_all(context):
    try:
        options = Options()
        options.add_argument("--window-size=860,1080")
        context.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        context.browser.set_window_position(0, 0)
    except FileNotFoundError:
        print(f"Chromedriver not found")
    context.browser.implicitly_wait(10)
    return context.browser

