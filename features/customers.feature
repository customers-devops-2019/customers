Feature: The Customer service back-end
    As a e-commerce store owner
    I need a RESTful customer service
    So that I can keep track of all my customer


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Customer Demo RESTful Service" in the title
    And I should not see "404 Not Found"
