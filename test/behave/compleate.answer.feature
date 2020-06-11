Feature: Complete your answers

    Scenario: complete answers
        Given an english speaking user
        When the user says "how are you"
        Then "mycroft-hello-world" should reply with dialog from "how.are.you.dialog"
        And the user replies "complete also sometimes your answers"
        Then "learning" should reply with dialog from "found.output.dialog"
        And the user replies "better than you"
        Then "learning" should reply with "should I add the sentence: better than you"
        And the user replies "yes"
        Then wait some time
        Then delete learn complete answers
