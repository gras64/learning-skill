Feature: Complete your answers

    Scenario: complete answers
        Given an english speaking user
        When the user says "how are you"
        Then "mycroft-hello-world" should reply with dialog from "how.are.you.dialog"
        And the user says "complete also sometimes your answers"
        
