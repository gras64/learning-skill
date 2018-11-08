from adapt.intent import IntentBuilder
from os.path import dirname
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.audio import wait_while_speaking
from mycroft.util.log import LOG, getLogger

_author__ = 'gras64'
LOGGER = getLogger(__name__)

class Learning(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.local_path = ".private"
        self.public_path = ".public"
        self.privacy = ""

    def get_category_response(self, dialog):
                while True:
                    catego = self.get_response(dialog)
                    #more of categorys enter here
                    if catego == "humor.intent":
                    elif catego == "science.intent":
                    elif catego == "love.intent":
                    else:
                        self.speak_dialog("invalid.category")

    @intent_file_handler('learning.intent')
    def handle_learning(self, message):
        self.speak_dialog('learning')

    @intent_file_handler('private.intent')
    def handle_private(self, message):
        self.speak_dialog('private')
        category = get_category_response("get.lower")

def create_skill():
    return Learning()

