Feature: eBay Regression Testing


  Scenario: Verify Hero carousel functionality
    Given Hero carousel slides are collected
    Then Autoplay and verify carousel correct slide appearance
    When Click carousel play/pause button and track slides
    Then Verify carousel correct slide appearance
    When Click carousel left button and track slides
    Then Verify carousel correct slide appearance
    When Click carousel right button and track slides
    Then Verify carousel correct slide appearance


  Scenario Outline: Add the first searched item to cart and verify that
    Given
    When Choose "<category>"
    And Type "<item>" in the search field
    And Press search button
    And Find first item with "Buy it now" option
    Then Add the item to cart and get the title
    Then Check if the item is in the cart


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


  Scenario: Verify image rendering
    Given Open eBay
    When Go to advanced search
    And Select options
    And Click submit
    Then Verify the correct search results
    When Open the first found item
    And Verify the images are downloading and rendering correctly
