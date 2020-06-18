Feature: edit your dialogues

    Scenario: edit your dialogues
        Given an english speaking user
        When the user says "can you edit your dialogues in personal skill"
        Then "learning" should reply with dialog from "read.for.dialog"
        And "learning" should reply with anything
        And the user replies "yes"
        Then "learning" should reply with dialog from "found.output.dialog"
        And the user replies "I couldn't find that date for you"
        Then "learning" should reply with dialog from "save.update.dialog"
        And the user replies "no"
        Then "learning" should reply with dialog from "continue.dialog"
        And the user replies "no"
