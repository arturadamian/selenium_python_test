from selenium.webdriver.common.by import By


class SignInModalLocators:
    """Holds locators for SignIn Modal Window."""
    USERNAME_INPUT = (By.NAME, "login")
    PASSWORD_INPUT = (By.NAME, "token")
    SIGNIN_MODAL_BUTTON = (By.CLASS_NAME, "js-sign-in-submit")
    MODAL_WINDOW = (By.ID, "sign-in-modal")
