Feature: learn public
  Scenario: learn invalid category
    Given an english speaking user
    When the user says "may i teach you something"
    Then "learning" should reply with dialog from "begin.learning.dialog"
    And the user says "top"
    Then "learning" should reply with dialog from "invalid.category.dialog"

  Scenario: learn public
    Given an english speaking user
    When the user says "may i teach you something"
    Then "learning" should reply with dialog from "begin.learning.dialog"
    And the user replies "funny"
    Then "learning" should reply with dialog from "question.dialog"
    And the user replies "why is the banana crooked"
    Then "learning" should reply with dialog from "keywords.dialog"
    And the user replies "banana crooked"
    Then "learning" should reply with dialog from "answer.dialog"
    And the user replies "because nobody went to watch forest to straighten them"
    Then "learning" should reply with "So I'm supposed to answer the question why is the banana crooked with because nobody went to watch forest to straighten them?"
    And the user replies "yes"
    Then delete learn public