class SearchPage:
    """Contains locators on the search page"""

    SIGN_IN = '//span[@id = "gh-ug"]/a[text() = "Sign in"]'
    REGISTER = '//span[@id = "gh-ug-flex"]/a[text() = "register"]'
    DAILY_DEALS = '//a[@class = "gh-p" and normalize-space() = ' \
                  '"Daily Deals"]'
    BRAND_OUTLET = '//a[@class = "gh-p" and normalize-space() = ' \
                   '"Brand Outlet"]'
    HELP_AND_CONTACT = '//a[@class = "gh-p" and normalize-space() = ' \
                       '"Help & Contact"]'
    COUPON = '//img[@id = "gh-hsi"]'
    SELL = '//a[@class = "gh-p" and normalize-space() = "Sell"]'
    WATCHLIST = '//li[@id = "gh-wl-click"]//a[@title = "Watchlist"]'
    MY_EBAY = '//li[@id = "gh-eb-My"]//a[@title = "My eBay"]'
    BELL = '//i[@id = "gh-Alerts-i"]'
    CART = '//li[@id = "gh-minicart-hover"]'
    EBAY_LOGO = '//a[@id = "gh-la"]'
    SHOP_BY_CATEGORY = '//button[@id = "gh-shop-a"]'
    SEARCH_FIELD = '//input[@id = "gh-ac"]'
    SELECT_CATEGORY = '//select[@id = "gh-cat"]'
    SEARCH_BUTTON = '//input[@id = "gh-btn"]'
    ADVANCED = '//a[@id = "gh-as-a"]'
    MINICART_ITEM_TITLE = '//li[@id = "gh-minicart-hover"]' \
                          '/descendant::div[@class = "gh-info__title"][1]'

    SEARCH_RESULTS = '//ul[contains(@class, "srp-results")]/li'
    RESULTS_IMAGE = '//div[@class = "s-item__image-section"]'


class ItemPage:
    """Contains locators on the item's page"""

    ADD_TO_CART = '//a[@id = "atcRedesignId_btn"]'
    TITLE = '//h1[@id = "itemTitle"]'
