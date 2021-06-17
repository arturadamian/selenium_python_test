class BasePage:
    """Base class.

    Args:
        driver (obj): WebDriver set in test setUp()

    """
    def __init__(self, driver):
        self.driver = driver
