from selenium.webdriver.common.by import By


class ArithmeticPageLocators:
    """Holds locators for Arithmetic Page."""
    ARITHMETIC_LINK = (By.LINK_TEXT, "Arithmetic")
    MEASUREMENT_LINK = (By.LINK_TEXT, "Measurment")
    ALGEBRA_LINK = (By.LINK_TEXT, "Algebra")
    GEOMETRY_LINK = (By.LINK_TEXT, "Geometry")
    PROBABILITY_LINK = (By.LINK_TEXT, "Probability")
    STATISTIC_LINK = (By.LINK_TEXT, "Statistics")
    TRIGONOMETRY_LINK = (By.LINK_TEXT, "Trigonometry")
    ANALYSIS_LINK = (By.LINK_TEXT, "Analysis")
    CALCULUS_LINK = (By.LINK_TEXT, "Calculus")

    ARITHMETIC_HEADER = (By.CLASS_NAME, "browseheader")
    DECIMALS_ACCORDION = (
        By.XPATH,
        "//*[@id='concept-list-container']/div[5]/a")
    ACCORDIONS_HEADERS = (By.XPATH, "//a[contains(@class, 'level-1-concept')]")
    ACCORDIONS_LINKS = (By.XPATH, "//a[contains(@href, '/c/arithmetic/')]")
    ACCORDIONS_CLICKED_LINKS = (By.ID, "artifact_title")
    EXPAND_ALL_BUTTON = (By.ID, "expand-all-concepts")
