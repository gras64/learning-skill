import time
from behave import given, then, when
from mycroft.messagebus.message import Message
from mycroft.filesystem import FileSystemAccess
import os

@then('delete learn private')
def delete_learn(self):
    #time.sleep(3)
    os.remove(os.path.expanduser("~/.mycroft/skills/LearningSkill/private/humor/dialog/en-us/banana.crooked.dialog"))
    os.remove(os.path.expanduser("~/.mycroft/skills/LearningSkill/private/humor/vocab/en-us/banana.crooked.intent"))

@then('delete learn public')
def delete_public_learn(self):
    #time.sleep(3)
    os.remove(os.path.expanduser("~/.mycroft/skills/LearningSkill/public/humor/dialog/en-us/banana.crooked.dialog"))
    os.remove(os.path.expanduser("~/.mycroft/skills/LearningSkill/public/humor/vocab/en-us/banana.crooked.intent"))

@then('delete learn Something for my skill')
def delete_learn_something_for_my_skill(self):
    if os.path.isfile(os.path.expanduser("~/.mycroft/skills/LearningSkill/mycroft-skills/mycroft-reminder/locale/en-us/SomethingReminder.intent")):
        os.remove(os.path.expanduser("~/.mycroft/skills/LearningSkill/mycroft-skills/mycroft-reminder/locale/en-us/SomethingReminder.intent"))
    ### to do delete only new data
    elif os.path.isfile(os.path.expanduser("~/.mycroft/skills/PootleSync/mycroft-skills/mycroft-reminder/locale/en-us/SomethingReminder.intent")):
        os.remove(os.path.expanduser("~/.mycroft/skills/PootleSync/mycroft-skills/mycroft-reminder/locale/en-us/SomethingReminder.intent"))
    elif os.path.isfile(os.path.expanduser("~/.mycroft/translation_dir/mycroft-reminder/locale/en-us/SomethingReminder.intent")):
        os.remove(os.path.expanduser("~/.mycroft/translation_dir/mycroft-reminder/locale/en-us/SomethingReminder.intent"))
    else:
        return False