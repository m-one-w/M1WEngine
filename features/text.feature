Feature: Text objects
    Scenario: Creating a text object
        Given pygame is initialized
        When the word apple is created at position (0,0)
        Then the string is correct
        And the position is correct
