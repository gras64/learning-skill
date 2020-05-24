import time
from behave import given, then, when
from mycroft.messagebus.message import Message
from mycroft.filesystem import FileSystemAccess
import os

@then('delete learn private')
def delete_learn(self): #example
    #time.sleep(3)
    #os.remove("~/.mycroft/skills/LearningSkill/private/humor/dialog/en-us/banana.crooked.dialog")
    #os.remove("~/.mycroft/skills/LearningSkill/private/humor/vocab/en-us/banana.crooked.intent")
    pass

@then('delete learn public')
def delete_public_learn(self): #example
    #time.sleep(3)
    #os.remove("~/.mycroft/skills/LearningSkill/public/humor/dialog/en-us/banana.crooked.dialog")
    #os.remove("~/.mycroft/skills/LearningSkill/public/humor/vocab/en-us/banana.crooked.intent")
    pass