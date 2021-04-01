class element_changed_css_class:
    """An expectation for checking that an element changed
    a particular css class.

    Args:
        locator (tuple): used to find the element

    """

    def __init__(self, element, css_class):
        self.element = element
        self.css_class = css_class

    def __call__(self, driver):
        """Checks that css has been changed on a particular element.

        Returns:
            the WebElement once it has the particular css class
            or False

        """
        if self.css_class in self.element.get_attribute("class"):
            return self.element
        else:
            return False
