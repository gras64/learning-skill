from adapt.intent import IntentBuilder
from os.path import join, dirname, abspath
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.audio import wait_while_speaking
from mycroft.util.log import LOG, getLogger
import requests

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
        self.Category = ""

    def initialize(self):
#        self.scheduler = BackgroundScheduler()
#        self.scheduler.start()

#        self._routines = defaultdict(dict)
#        self._routines.update(self._load_routine_data())

#        self._routine_to_sched_id_map = {}
#        self._register_routines()

        path = dirname(abspath(__file__))

        path_to_humor_words = join(path, 'vocab', self.lang, 'Humor.voc')
        self._humor_words = self._lines_from_path(path_to_humor_words)

        path_to_science_words = join(path, 'vocab', self.lang, 'Science.voc')
        self._science_words = self._lines_from_path(path_to_science_words)

        path_to_love_words = join(path, 'vocab', self.lang, 'Love.voc')
        self._love_words = self._lines_from_path(path_to_love_words)

        path_to_cancel_words = join(path, 'vocab', self.lang, 'Cancel.voc')
        self._cancel_words = self._lines_from_path(path_to_cancel_words)

    def _lines_from_path(self, path):
        with open(path, 'r') as file:
            lines = [line.strip().lower() for line in file]
            return lines

    @intent_file_handler('Private.intent')
    def handle_interaction(self, message):
        catego = self.get_response("begin.private")
        if catego in self._humor_words:
            self.speak("humor")
            Category = humor
        elif catego in self._science_words:
            self.speak("science")
            Category = science
        elif catego in self._love_words:
            self.speak("love")
            Category = love
        elif catego in self._cancel_words:
            self.speak("cancel")
            return
        else:
            self.speak("invalid.category")
            return catego
        question = self.get_response("question")
        if not question:
            return  # user cancelled
        keywords = self.get_response("keywords")
        if not keywords:
            return  # user cancelled
        answer = self.get_response("answer")
        if not answer:
            return  # user cancelled
        self.speak("save.learn",
                    data={"question": question,
                          "answer": answer},
                           expect_response=True)

    @intent_file_handler('Learning.intent')
    def handle_interaction(self, message):
        catego = self.get_response("begin.learning")
        if catego in self._humor_words:
            self.speak("humor")
            Category = humor
        elif catego in self._science_words:
            self.speak("science")
            Category = science
        elif catego in self._love_words:
            self.speak("love")
            Category = love
        elif catego in self._cancel_words:
            self.speak("cancel")
            return
        else:
            self.speak("invalid.category")
            return catego
        question = self.get_response("question")
        if not question:
            return  # user cancelled
        keywords = self.get_response("keywords")
        if not keywords:
            return  # user cancelled
        answer = self.get_response("answer")
        if not answer:
            return  # user cancelled
        self.speak("save.learn",
                    data={"question": question,
                          "answer": answer},
                           expect_response=True)

    # @intent_file_handler("private.intent")
    # def handle_private(self, message):
    #    self.speak_dialog('private')
    # category = get_category_response(self, message)

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
