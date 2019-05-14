Feature: The Customer service back-end
    As a Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
      | firstname | lastname | email         | subscribed | address1  | address2 | city     | province | country | zip    |
      | John      | Doe      | jd@email.com  | True       | 2 Main St | 3B       | Toronto  | Ontario  | Canada  | MH48J4 |
      | Steve     | Park     | sn@email.com  | True       | 1 Main St | 1C       | Toronto  | Ontario  | Canada  | MH48J3 |
      | Dave      | Jones    | dj@email.com  | True       | 1 Main St | 3B       | Brooklyn | New York | USA     | 11201  |



Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Customer
   When I visit the "Home Page"
   And I set the "First Name" to "Isabel"
   And I set the "Last Name" to "Smith"
   And I set the "Email" to "ismith@test.com"
   And I set the "Subscribed" to "True"
   And I press the "Create" button
   Then I should see the message "Success"

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

Scenario: Delete a Customer
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "John" in the results
    When I set the "ID" to "John"
    When I press the "Delete" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I set the "City" to "Toronto"
    And I press the "Search" button
    Then I should see "Steve" in the results
    And I should not see "John" in the results

Scenario: Unsubscribe a customer
    When I visit the "Home Page"
    And I press the "Clear" button
    And I press the "Search" button
    Then I should see "John" in the results
    When I set the "ID" to "John"
    And I copy the "ID" field
    And I paste the "ID" field
    And I press the "Unsubscribe" button
    Then I should see the message "Success"
    Then I should see "False" in the "Subscribed" dropdown

Scenario: Update a Customer
    When I visit the "Home Page"
    And I set the "ID" to "John"
    And I press the "Retrieve" button
    Then I should see "John" in the "First Name" field
    And I should see "Doe" in the "Last Name" field
    When I change "Last Name" to "Wick"
    And I press the "Update" button
    Then I should see the message "Success"
