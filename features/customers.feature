Feature: The Customer service back-end
    As a Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my customers

Background:
    Given the following customers
      | id | firstname | lastname | email        | subscribed | address1  | address2 | city    | province | country | zip    |
      | 1  | John      | Doe      | j@email.com  | True       | 2 Main St | 3B       | Toronto | Ontario  | Canada  | MH48J4 |
      | 2  | Steve     | Nadh     | j@email.com  | True       | 1 Main St | 3B       | Toronto | Ontario  | Canada  | MH48J3 |
      | 3  | Ivan      | Mar      | iv@email.com | False      | 4 Main St | 2E       | Toronto | New York | USA     | 10042  |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"


Scenario: Delete an Customer
   When I visit the "Home Page"
   And I set the "ID" to "2"
   And I press the "delete" customer button
   Then I should see the message "Customer Deleted!"

 Scenario: List all customers
     When I visit the "Home Page"
     And I press the "Search" button
     Then I should see "John" in the results
     And I should see "Steve" in the results
     And I should see "Ivan" in the results
