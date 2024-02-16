Feature: Tracking state

    Scenario: Transition from patrol to track
        Given A map is initialized
        And A patrolling minotaur will see a damsel
        When The track state is initialized
        Then Tracking state is entered
        And Tracking will last 2 seconds 
        And Tracking will released at the end of the state
