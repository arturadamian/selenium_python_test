from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from pathlib import Path
import shutil
import re


def before_all(context):
    context.ENVIRONMENT = "https://www.ebay.com/"
    context.delay = 10


def before_scenario(context, scenario):
    context.driver = webdriver.Chrome()
    context.driver.implicitly_wait(10)
    context.wait = WebDriverWait(context.driver, context.delay)


def after_step(context, step):
    failure_dir = "failure_screenshots"
    step_name = step.name.replace(' ', '_').lower()
    regex = re.compile('[^a-zA-Z0-9_]')
    step_name = regex.sub('', step_name).lower()
    screenshot_name = step_name + ".png"
    if Path(f"./{failure_dir}").is_dir():
        shutil.rmtree(f"./{failure_dir}")
    Path(f"./{failure_dir}").mkdir(parents=True, exist_ok=True)
    if step.status == 'failed':
        context.driver.save_screenshot(f"{screenshot_name}")


def after_scenario(context, scenario):
    context.driver.close()
    context.driver.quit()
