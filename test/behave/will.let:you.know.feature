Feature: will let you know

    Scenario: will let know
        Given an english speaking user
        When the user says "how does jack pay for the tram"
        Then "UnknownSkill" should reply with dialog from "unknown.dialog"
        And the user replies "that has something to do with humor"
        Then "learning" should reply with dialog from "keywords.dialog"
        And the user replies "Juck tram"
        Then "learning" should reply with dialog from "answer.dialog"
        And the user replies "bach doesn't pay him at all"
        Then "learning" should reply with "So I'm supposed to answer the question how does jack pay for the tram with bach doesn't pay him at all"
        And the user replies "no"