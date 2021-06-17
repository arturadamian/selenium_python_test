# from selenium.webdriver.support import expected_conditions as EC


# class element_to_be_clickable:
#     """An expectation for checking that an element is ready for a click."

#     Args:
#         element_or_locator (tuple || object): used to find the element


#     """

#     def __init__(self, element_or_locator):
#         self.target = element_or_locator

#     def __call__(self, driver):
#         """Checks that css style contains needed information.

#         Returns:
#             the WebElement once it is ready
#             or False

#         """
#         if type(self.target) is tuple:
#             element = EC.visibility_of_element_located(self.target)(driver)
#         else:
#             element = EC.visibility_of(self.target)
#         if element and element.is_enabled():
#             return element
#         else:
#             return False
