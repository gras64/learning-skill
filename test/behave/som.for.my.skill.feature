Feature: Something for my skill

    Scenario: Something for my reminder
        Given an english speaking user
        When the user says "you should reminding me of eating"
        Then wait some time 
        Then "UnknownSkill" should reply with dialog from "unknown.dialog"
        And the user replies "how would it be with the reminder skill"
        Then "learning" should reply with dialog from "save.update.dialog"
        And the user replies "yes"
        Then "reminder" should reply with dialog from "ParticularTime.dialog"
        And the user replies "no"
        Then wait some time
        Then delete learn Something for my skill