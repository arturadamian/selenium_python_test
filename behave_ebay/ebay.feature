Feature: eBay Buy

  Scenario Outline: Add the first searched item to cart
    Given Navigate to eBay
    When Choose "<Category>"
    And Search "<Item>"
    And Add first found item to cart
    Then Check the cart

    Examples:
      | Category | Item   |
      | Books    | Python |
      | Antiques | lamp   |

  Scenario: Select three best match items with average price
    Given Navigate to eBay
    When Choose "<Category>"
    And Search "<Item>"
    And