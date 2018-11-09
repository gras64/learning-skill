from adapt.intent import IntentBuilder
from os.path import dirname
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.audio import wait_while_speaking
from mycroft.util.log import LOG, getLogger

_author__ = 'gras64'

LOGGER = getLogger(__name__)


class LearningSkill(MycroftSkill):
    def __init__(self):
        super(LearningSkill, self).__init__("LearningSkill")
        self.enable_fallback = True
        self.local_path = ".private"
        self.public_path = ".public"
        self.privacy = ""
        self.catego = ""

    #def initialize(self):

    def get_category_response(self, dialog):
        while True:
            catego = self.get_response(dialog)
            #more of categorys enter here
            if catego == ("humor.intent"):
                return
            elif catego == ("science.intent"):
                return
            elif catego == ("love.intent"):
                return
            else:
                self.speak_dialog("invalid.category")

    @intent_handler(IntentBuilder("LearningIntent").require("Learning.intent").optionally("Category").one_of('Humor', 'Science', 'Love' ).build())
    def handle_learning_intent(self, message):
        self.speak_dialog('learning')
        category = get_category_response(self, message)
        
    @intent_handler(IntentBuilder("PrivateIntent").require("Learning.intent").require("Private.intent").one_of('Humor', 'Science', 'Love' ).build())
    def handle_private_intent(self, message):
        self.speak_dialog('private')
        category = get_category_response(self, message)

    #@intent_file_handler("private.intent")
    #def handle_private(self, message):
    #    self.speak_dialog('private')
        #category = get_category_response(self, message)
        
#    def handle_fallback(self, message):
#        LOG.debug("entering handle_fallback with utterance '%s'" %
#                  message.data.get('utterance'))
#        if not self.enable_fallback:
#            LOG.debug("fallback not enabled!")
#            return False
#            
#    def shutdown(self):
#        self.remove_fallback(self.handle_fallback)
#        super(LearingSkill, self).shutdown()

def create_skill():
    return LearningSkill()

