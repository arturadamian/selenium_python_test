from behave import *
from pages.modal_signin import ModalSignIn
from pages.main_page import MainPage


@given('User opens home page')
def open_main(context):
    context.browser.get("https://www.ck12.org")


@then('Check home title')
def check_home_title(context):
    """Checks the title of the Main page."""
    main_page = MainPage(context.browser)
    assert main_page.is_title_matched(), \
        "Main page title does not match"


@when('Click sign in button')
def click_signin(context):
    modal_signin = ModalSignIn(context.browser)
    modal_signin.open_modal()


@then('Modal window is open')
def check_modal(context):
    main_page = MainPage(context.browser)
    assert main_page.is_signin_modal_shown()


@when('Enters "{username}" and "{password}" and click submit button')
def login(context, username, password):
    print("I am here")
    modal_signin = ModalSignIn(context.browser)
    modal_signin.login(username, password)


@then('User "{name}" successfully logged in')
def check_login(context, name):
    main_page = MainPage(context.browser)
    assert main_page.is_logged_in(name), \
        "user is not logged in"


@then('Choose another lang')
def test_change_language(context):
    """Checks language change element in footer"""
    langs = ['Zulu', 'Chinese', 'Hebrew', 'Burmese']
    main_page = MainPage(context.browser)
    assert all([main_page.switch_language(lang) for lang in langs])
