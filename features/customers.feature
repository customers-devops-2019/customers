Feature: The Customer service back-end
    As a Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
      | id | firstname | lastname | email        | subscribed | address1  | address2 | city    | province | country | zip    |
      |   | John      | Doe      | jd@email.com  | True       | 2 Main St | 3B       | Toronto | Ontario  | Canada  | MH48J4 |
      |   | Steve     | Nadh     | sn@email.com  | True       | 1 Main St | 1C       | Toronto | Ontario  | Canada  | MH48J3 |
      |   | Dave     | Jones     | dj@email.com  | True       | 1 Main St | 3B       | Brooklyn | New York  | USA  | 11201 |




Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"


Scenario: List all customers
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "John" in the results
    And I should see "Steve" in the results
    And I should see "Dave" in the results

  Scenario: List all people from Ontario
    When I visit the "Home Page"
    And I press the "Clear" button
    And I set the "Province" to "Ontario"
    And I press the "Search" button
    Then I should see "John" in the results
    And I should see "Steve" in the results
    And I should not see "Dave" in the results
