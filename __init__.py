from os.path import dirname
from mycroft import MycroftSkill, intent_file_handler

_author__ = 'gras64'
# Release - 000001

class Learning(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.local_path = ".private"
        self.public_path = ".public"


    @intent_file_handler('learning.intent')
    def handle_learning(self, message):
        self.speak_dialog('learning')

    @intent_file_handler('private.intent')
    def handle_answers_thebest(self, message):
        self.speak_dialog('private')

def create_skill():
    return Learning()

