Feature: eBay Regression Testing


  Background: Set up environment
    Given Open eBay


  @fixture.browser.chrome
  Scenario: Verify filteres in description of the item
    Given And Main
    When In the search field we type shoes woman
    And Click search_button
    And Click more_filters
    And Choose filter "US Shoe Size" "8"
    And Choose filter "Brand" "Nike"
    And Choose filter "Upper Material" "Cotton"
    When Click apply_button
    Then Collect item links
    Then Verify item's description contains "filter" and "option"


  @fixture.browser.chrome
  Scenario Outline: Duplicates within search with different sessions
    Given Main search field
    When Type <keywords> in the search field
    And Press search button
    Then Store records from the page
    Then Verify records are identical from exact same search

    Examples:
      | keywords                  |
      | christian louboutin black |
      | christian louboutin black |


  @fixture.browser.chrome
  Scenario: Verify search auto correction
    Given Main search field
    When Type por%able spea*er in the search field
    And Press search button
    Then Verify correct search
    Then Verify rewritten search is portable speaker


  @fixture.browser.chrome
  Scenario: Verify average rating correlates with rating stars in listings
    Given Main search field
    When Type portable speaker in the search field
    And Press search button
    When Find items with rating >= "4" stars and discount >= "40"%
    Then Verify the average rating >= "4" and discount >= "40"%


  @fixture.browser.chrome
  Scenario Outline: Verify result of the specific search on given pages
    Given Main search field
    When Type <keywords> in the search field
    And Press search button
    Then Verify correct search
    Then Verify titles contain <keywords> on the pages from <current_page> to <page_number>

    Examples:
      | keywords  | page_number | current_page |
      | Nike Zoom | 9           | 6            |
      | Nike Zoom | 4           | 6            |


  @fixture.browser.chrome
  Scenario Outline: Verify result of the specific search on all pages
    Given Main search field
    When Type <keywords> in the search field
    And Press search button
    Then Verify correct search
    Then Open All refinements
    When In all refinements choose "Buying Format" <buying_format>
    When In all refinements choose "Item Location" <item_location>
    When In all refinements choose "Local Pickup" <local_pickup>
    When In all refinements choose "US Shoe Size" <shoe_size>
    And Press Apply Button
    Then Collect pagination items
    Then Verify all titles on all pages contain search <keywords>

    Examples:
      | keywords  | buying_format | item_location | local_pickup      | shoe_size                  |
      | Nike Zoom | Auction       | US Only       | Free Local Pickup | [10, 7, 12, 9, 6, 11.5, 8] |


  @fixture.browser.chrome
  Scenario Outline: Verify Advanced Search options
    Given Data stored for Advanced Search
    When Open Advanced search
    And Type <keywords> in the search field
    And In keywords options select Exact words, any order
    And Check Title and description
    And In Price put from <min_price> to <max_price>
    And Check Buy It Now
    And Check Auction
    And Check New
    And Check Sale items
    And Check Free shipping
    And In Location select <miles_away> of <index>
    And In Sort by select <sorted_by>
    And In View results select All items
    And In Results per page select <results_per_page>
    And Press search button
    Then Verfiy number <results_per_page>
    Then Verify Distance: nearest first, <index>, not farther than <miles_away>
    Then Verify the price of the listing on the page is from <min_price> to <max_price>
    When Collect listing titles
    Then Verify that titles contain exact words <keywords>
    Then Verify Free shipping and Sale

    Examples:
      | min_price | max_price | miles_away | index | sorted_by               | results_per_page | keywords       |
      | 50        | 500       | 1000       | 94607 | Distance: nearest first | 25               | grill portable |


  @fixture.browser.chrome
  Scenario: Verify Hero carousel functionality
    Given Hero carousel slides are collected
    Then Verify carousel autoplay
    When Carousel pause
    Then Verify pause button
    Then Verify correct slide appearance
    When Carousel play
    Then Verify play button
    Then Verify correct slide appearance
    When Carousel right
    Then Verify correct slide appearance
    When Carousel left
    Then Verify correct slide appearance


  @fixture.browser.chrome
  Scenario Outline: Add the first searched item to cart and verify that with it's title in mini cart
    Given Saved data
    When Select <category>
    And Type <item> in the search field
    And Press search button
    And Find first item to open in a new tab
    When Open element in a new tab
    Then Get the title of the item
    Then Add the item to cart if there is an option
    Then Close the second tab
    When Hover over cart
    Then Verify the title of the item in mini cart

    Examples:
      | category | item   |
      | Antiques | Lamp   |
      | Books    | Python |


  @fixture.browser.chrome
  Scenario Outline: Search specific items on auction and save pictures of them in a created directory
    Given Save directory to create, <item>
      """
      screenshots
      """
    When Type <item> in the search field
    And Press search button
    Then Verify correct search
    When Sort listings by central left <option>
    When Filter and collect items: <price_max>, <price_min>, <ship_price_max>, <bidding_min_days_left>
    When Cleanup/create a directory for saving files in project root
    Then Open items in a new tab and save screenshots in the directory

    Examples:
      | item        | price_max | price_min | ship_price_max | bidding_min_days_left | option  |
      | shoes men   | 9         | 0         | 5              | 2                     | Auction |
      | shoes women | 30        | 17        | 50             | 1                     | Auction |


  @fixture.browser.chrome
  Scenario Outline: Verify Recent searches in suggested search menu
    Given Main search field
    When Type <full_item> in the search field
    And Press search button
    And Go back
    When Type <partial_item> in the search field
    And Find the first Recent searches element in suggested search
    Then Verify that first "Recent searches" element == <full_item>

    Examples:
      | partial_item | full_item   |
      | shoe         | shoes women |
      | shoe         | shoes men   |

  @fixture.browser.chrome
  Scenario Outline: Verify image rendering, HTTP response, appearance on the page
    Given A directory to create, <keywords>
      | directory |
      | images    |
    When Open Advanced search
    And Select <keyword_options>
    And Type <keywords> in the search field
    And Press search button
    Then Verify correct search
    When Sort by central right <option>
    When Open the first found item
    Then Collect the images of the item
    Then Verify the images are getting 200 HTTP response
    Then Verify that downloaded images size > 0
    When Open image gallery
    When Collect gallery images
    Then Verify the images are rendered and displayed
    Then Verify the left arrow button of the gallery

    Examples:
      | keyword_options        | keywords                    | option               |
      | Exact words, any order | 1969 Mercedes-Benz SL-Class | Price: highest first |

  @fixture.browser.chrome
  Scenario: Verify navigation links redirection
    Given Links -> Titles to verify
      """
      {
        "Motors": "eBay Motors: Auto Parts and Vehicles | eBay",
        "Fashion": "Fashion products for sale | eBay",
        "Electronics": "Electronics products for sale | eBay",
        "Collectibles & Art": "Collectibles & Art products for sale | eBay",
        "Home & Garden": "Home & Garden products for sale | eBay",
        "Sporting Goods": "Sporting Goods for sale | eBay",
        "Toys": "Toys & Hobbies products for sale | eBay",
        "Business & Industrial": "Business & Industrial products for sale | eBay",
        "Music": "Music products for sale | eBay",
        "Deals": "Daily Deals on eBay | Best deals and Free Shipping"
      }
      """
    When Open navigation link Deals
    Then Verify correct redirection with title

  @fixture.browser.chrome
  Scenario Outline: Search for a very specific item and verfify results
    Given Main search field
    When Type <keywords> in the search field
    When Press search button
    Then Verify correct search
    When Collect listing titles
    Then Calculate result match
    Then Verify match score > <min_match_score> and full title match score > <min_full_title_match_score>

    Examples:
      | keywords                   | min_match_score | min_full_title_match_score |
      | green inflatable crocodile | 50              | 20                         |


  @fixture.browser.chrome
  Scenario Outline: Search for a specific item with details and verify results
    Given Main search field
    When Type <main_search> <main_details> <other_details> in the search field
    When Press search button
    Then Verify correct search
    When Collect listing titles
    Then Verify all listing titles contain the <main_search> with important <main_details>
    Then Verify all items contain some of "<other_details>"

    Examples:
      | main_search   | main_details | other_details               |
      | iPhone 11 Pro | 256GB        | Max midnight green unlocked |
