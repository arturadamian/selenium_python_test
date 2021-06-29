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
    Given Save directory to create, "<item>"
      """
      screenshots
      """
    When Type "<item>" in the search field
    And Press search button
    Then Verify correct search
    When Sort listings by central left "<option>"
    And Filter and collect items: "<price_max>", "<price_min>", "<ship_price_max>", "<bidding_min_days_left>"
    When Cleanup/create a directory for saving files in project root
    Then Open items in a new tab and save screenshots in the directory

    Examples:
      | item        | price_max | price_min | ship_price_max | bidding_min_days_left | option  |
      | shoes men   | 19        | 0         | 5              | 2                     | Auction |
      | shoes women | 30        | 17        | 50             | 1                     | Auction |

  Scenario Outline: Verify Recent searches in suggested search menu
    Given Set up Xpath in context
    When Type "<full_item>" in the search field
    And Press search button
    And Go back
    When Type "<partial_item>" in the search field
    And Find the first Recent searches element in suggested search
    Then Verify that first "Recent searches" element == "<full_item>"

    Examples:
      | partial_item | full_item   |
      | shoe         | shoes women |
      | shoe         | shoes men   |

  Scenario Outline: Verify image rendering, HTTP response, appearance on the page
    Given A directory to create, "<keywords>"
      | directory |
      | images    |
    When Open Advanced search
    And Select "<keyword_options>"
    And Type "<keywords>" in the search field
    And Press search button
    Then Verify correct search
    When Sort by central right "<option>"
    When Open the first found item
    Then Collect the images of the item
    Then Verify the images are getting 200 HTTP response
#    When Cleanup/create a directory for saving files in project root
    Then Verify that downloaded images size > 0
    When Open image gallery
    When Collect gallery images
    Then Verify the images are rendered and displayed
    Then Verify the left arrow button of the gallery

    Examples:
      | keyword_options        | keywords                    | option               |
      | Exact words, any order | 1969 Mercedes-Benz SL-Class | Price: highest first |