Feature: Amazon regretion testing

  Scenario: Verify the prices advertised on the main page
    Given Search environment
    When Collect item's urls and prices on the main page
    Then Verify that item prices are the same as on the main page
