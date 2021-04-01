class element_has_css_style:
    """An expectation for checking that an element has a particular css style.

    Args:
        locator (tuple): used to find the element
        css_style (string): css style of the element

    """

    def __init__(self, locator, css_style):
        self.locator = locator
        self.css_style = css_style

    def __call__(self, driver):
        """Checks that css style contains needed information.

        Returns:
            the WebElement once it has the particular css style
            or False

        """
        element = driver.find_element(*self.locator)
        if self.css_style in element.get_attribute("style"):
            return element
        else:
            return False
