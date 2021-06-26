Feature: eBay Regression Testing

  Scenario Outline: Add the first searched item to cart
    Given Open eBay
    When Choose "<category>"
    And Type "<item>" in the search field
    And Press search button
    And Find first item with "Buy it now" option and add it to cart
    Then Add the item to cart and get the title
    Then Check if the item is in the cart

    Examples:
      | category | item   |
      | Antiques | Lamp   |
      | Books    | Python |

  Scenario Outline: Search with suggestion and watch filtered items on auction
    Given Open eBay
    When Type "<item>" in the search field
    And Press search button
    And Verify "<item>" search and sort listings by auctions
    And Filter items: "<price_max>", "<price_min>", "<ship_price_max>", "<bid_days_left>"
    Then Create/cleanup the directory for screenshots
    Then Save screenshots of selected items in a newly created directory

    Examples:
      | item        | price_max | price_min | ship_price_max | bid_days_left |
      | shoes women | 25        | 20        | 10             | 1             |
