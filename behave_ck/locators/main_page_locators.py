from selenium.webdriver.common.by import By


class MainPageLocators:
    """Holds locators for Main Page."""
    SIGNIN_BUTTON = (By.ID, "top_nav_signin")
    SUBJECTS_BUTTON = (By.XPATH, "//a[@href='/browse']")
    USER_HEADER = (By.ID, "header_user_dropdown")
    POPUP_WINDOW = (By.ID, "welcomePopup")
    LANGUAGE_BUTTON = (By.CLASS_NAME, "goog-te-gadget-simple")
    LANGUAGE_IFRAME = (By.XPATH, "//body/iframe[1]")
