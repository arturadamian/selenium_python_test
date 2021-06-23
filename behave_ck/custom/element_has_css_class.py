class element_has_css_class:
    """An expectation for checking that an element has a particular css class.

    Args:
        locator (tuple): used to find the element
        css_class (string): css class of the element

    """

    def __init__(self, locator, css_class):
        self.locator = locator
        self.css_class = css_class

    def __call__(self, driver):
        """Checks that css class fully or partially matches.

        Returns:
            the WebElement once it has the particular css class
            or False

        """
        element = driver.find_element(*self.locator)
        if self.css_class in element.get_attribute("class"):
            return element
        else:
            return False
