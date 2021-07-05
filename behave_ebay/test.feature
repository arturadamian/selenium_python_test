Feature: eBay Regression Testing


  Scenario: Verify Advanced Search options
    Given Data stored for Advanced Search
    When Open Advanced search
    And Type grill portable in the search field
    And In keywords options select Exact words, any order
    And Check Title and description
    And In Price put from 50 to 500
    And Check Buy It Now
    And Check Auction
    And Check New
    And Check Sale items
    And Check Free shipping
    And In Location select 1000 miles of 94607
    And In Sort by select Distance: nearest first
    And In View results select All items
    And In Results per page select 25
    And Press search button
    Then Verfiy number of results is <= 25
    Then Verify listings sorted by Distance: nearest first and the index is correct
    Then Verify the price of the listing on the page is from 50 to 500
    When Collect listing titles
    Then Verify that titles contain exact words grill and portable


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
    Given Saved data
    When Select <category>
    And Type <item> in the search field
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
      | shoes men   | 19        | 0         | 5              | 2                     | Auction |
      | shoes women | 30        | 17        | 50             | 1                     | Auction |

  Scenario Outline: Verify Recent searches in suggested search menu
    Given Set up necessary data
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


  Scenario Outline: Search for a very specific item and verfify results
    Given Data for navigation
    When Type <keywords> in the search field
    When Press search button
    Then Verify correct search
    When Collect listing titles
    Then Calculate result match
    Then Verify match score > <min_match_score> and full title match score > <min_full_title_match_score>

    Examples:
      | keywords                   | min_match_score | min_full_title_match_score |
      | green inflatable crocodile | 50              | 20                         |


  Scenario Outline: Search for a specific item with details and verfify results
    Given Some data stored
    When Type <main_search> <main_details> <other_details> in the search field
    When Press search button
    Then Verify correct search
    When Collect listing titles
    Then Verify all listing titles contain the <main_search> with important <main_details>
#    Then Verify most items contain "<other_details>"

    Examples:
      | main_search   | main_details | other_details               |
      | iPhone 11 Pro | 256GB        | Max midnight green unlocked |
