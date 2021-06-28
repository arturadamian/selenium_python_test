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


  Scenario Outline: Add the first searched item to cart and verify that with it's title in mini cart
    Given Xpath saved in context
    When Select "<category>"
    And Type "<item>" in the search field
    And Press search button
    And Find first item to open in a new tab
    When Open element in a new tab
    Then Get the title of the item
    Then Add the item to cart if there is an option
    When Hover over cart
    Then Verify the title of the item in mini cart

    Examples:
      | category | item   |
      | Antiques | Lamp   |
      | Books    | Python |

  Scenario Outline: Search specific items on auction and save pictures of them in a created directory
    Given Directory to create
      """
      screenshots
      """
    When Type "<item>" in the search field
    And Press search button
    Then Verify "<item>" search
    When Sort listings by central left "<option>"
    And Filter items: "<price_max>", "<price_min>", "<ship_price_max>", "<bidding_min_days_left>"
    Then Create/cleanup the directory for screenshots
    Then Open items in a new tab and save screenshots in the directory


    Examples:
      | item        | price_max | price_min | ship_price_max | bidding_min_days_left | option  |
      | shoes women | 25        | 20        | 10             | 1                     | Auction |

  Scenario Outline: Verify Recent searches in suggested search menu
    Given
    When Type "<full_item>" in the search field
    And Press search button
    And Go back
    When Type "<partial_item>" in the search field
    And Find the first Recent searches element in suggested search
    Then Verify first Recent searches element == "<full_item>"

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
