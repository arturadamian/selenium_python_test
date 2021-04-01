from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options


BASE_URL = "https://www.ck12.org"
ARITHMETIC_ENDPOINT = "/c/arithmetic/"
BROWSE_ENDPOINT = "/browse"
INTERACTIVE_ALGEBRA_2 = "https://flexbooks.ck12.org/cbook/ck-12-interactive-algebra-2"
PROPERTIES_OF_POLYNOMIALS = "/section/1.1/primary/lesson/properties-of-polynomials"

def get_driver(browserName):
    if browserName == "chrome":
        options = Options()
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.set_window_position(0, 0)
    elif browserName == "firefox":
        driver = webdriver.Firefox(
            executable_path=GeckoDriverManager().install())
    elif browserName == "safari":
        driver = webdriver.Safari()
    else:
        raise Exception(f"driver {browserName} not found")
    driver.implicitly_wait(10)
    return driver
