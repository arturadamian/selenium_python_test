from selenium import webdriver


def before_scenario(context, scenario):
    context.driver = webdriver.Chrome()
    context.driver.get("https://www.ebay.com/")
    context.driver.implicitly_wait(5)
    context.delay = 5


def after_scenario(context, scenario):
    context.driver.quit()
