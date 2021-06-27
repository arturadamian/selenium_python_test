Feature: eBay Regression Testing

  Scenario Outline: Add the first searched item to cart and verify that
    Given Open eBay
    When Choose "<category>"
    And Type "<item>" in the search field
    And Press search button
    And Find first item with "Buy it now" option
    Then Add the item to cart and get the title
    Then Check if the item is in the cart
    And Quit browser

    Examples:
      | category | item   |
      | Antiques | Lamp   |
      | Books    | Python |

  Scenario Outline: Search specific items on auction and save pictures of them
    Given Open eBay
    When Type "<item>" in the search field
    And Press search button
    Then Verify "<item>" search
    When Sort listings by left "<option>"
    And Filter items: "<price_max>", "<price_min>", "<ship_price_max>", "<bid_days_left>"
    Then Create/cleanup the directory for screenshots
    Then Save screenshots of selected items in the directory
    And Quit browser

    Examples:
      | item        | price_max | price_min | ship_price_max | bid_days_left | option  |
      | shoes women | 25        | 20        | 10             | 1             | Auction |

  Scenario Outline: Verify Recent searches in suggested search menu
    Given Open eBay
    When Type "<full_item>" in the search field
    And Press search button
    And Go back
    When Type "<partial_item>" in the search field
    And Find the first Recent searches element in suggested search
    Then Verify first Recent searches element == "<full_item>"
    And Quit browser

    Examples:
      | partial_item | full_item   |
      | shoe         | shoes women |


  Scenario: Verify Hero carousel functionality
    Given Open eBay
    Then Verify carousel autoplay
    Then Verify carousel controls - left, right, play/pause buttons
    And Quit browser

  Scenario: Verify image rendering
    Given Open eBay
    When Go to advanced search
    And Select options
    And Click submit
    Then Verify the correct search results
    When Open the first found item
    And Verify the images are downloading and rendering correctly
