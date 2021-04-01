from selenium.webdriver.common.by import By


class BrowsePageLocators:
    """Holds locators for Browse Page."""
    HEADER = (By.CLASS_NAME, "sc-ckVGcZ")
    ARITHMETIC_LINK = (By.LINK_TEXT, "Arithmetic")
    TITLE = (By.XPATH, "/html[1]/head[1]/title[1]")
    ALL_LINKS = (By.XPATH, "//div[contains(@class, 'sc-eNQAEJ')]//a")
    LINKS_BY_URL = {
        "interactives": (By.ID, "languageDropDownBtn")
    }
