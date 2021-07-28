from behave.fixture import use_fixture
from fixtures import browser_firefox
from fixtures import browser_chrome
from fixtures import browser_safari
from pathlib import Path
import shutil
import re


def before_tag(context, tag):
    if tag == "fixture.browser.firefox":
        return use_fixture(browser_firefox, context)
    elif tag == "fixture.browser.chrome":
        return use_fixture(browser_chrome, context)
    elif tag == "fixture.browser.safari":
        return use_fixture(browser_safari, context)


def before_all(context):
    context.ENVIRONMENT = "https://www.ebay.com"


def before_feature(context, feature):
    context.feature.records = {}
    failure_dir = "failure_screenshots"

    if Path(f"./{failure_dir}").is_dir():
        shutil.rmtree(f"./{failure_dir}")


def after_step(context, step):
    failure_dir = "failure_screenshots"
    step_name = step.name.replace(' ', '_').lower()
    regex = re.compile('[^a-zA-Z0-9_]')
    step_name = regex.sub('', step_name).lower()
    screenshot_name = step_name + ".png"
    if step.status == 'failed':
        Path(f"./{failure_dir}").mkdir(parents=True, exist_ok=True)
        context.driver.save_screenshot(f"./{failure_dir}/{screenshot_name}")


def after_scenario(context, scenario):
    context.driver.quit()
