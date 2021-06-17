Feature: Testing Ck12 home page functionality

  Scenario: User navigates to home page and checks if the title is correct
    Given User opens home page
    Then Check home title

  Scenario: User navigates to home page and opens the sign in modal window
    Given User opens home page
    When Click sign in button
    Then Modal window is open

  Scenario Outline: User logs in
    Given User opens home page
    When Click sign in button
    And Enters "<username>" and "<password>" and click submit button
    Then User "<name>" successfully logged in

    Examples:
      | username | password | name   |
      | enlil    | Test123  | en lil |

  Scenario: User navigates to home page and changes the languages
    Given User opens home page
    Then Choose another lang
