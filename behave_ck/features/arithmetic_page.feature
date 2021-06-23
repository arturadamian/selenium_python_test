Feature: Testing Ck12 arithmetic page functionality

  Scenario: User navigates to arithmetic page and checks if the title is correct
    Given User opens arithmetic page
    Then Check arithmetic page header


  Scenario: User navigates to arithmetic page and checks accordion opening
    Given User opens arithmetic page
    Then Check arithmetic page accordion opening


  Scenario: User navigates to arithmetic page and checks links correct redirection
    Given User opens arithmetic page
    Then Click accordion links and check redirection
