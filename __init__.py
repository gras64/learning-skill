from adapt.intent import IntentBuilder
from os.path import join, dirname, abspath, os, sys
from mycroft.messagebus.message import Message
from mycroft import MycroftSkill, intent_handler, intent_file_handler
from mycroft.filesystem import FileSystemAccess
from mycroft.audio import wait_while_speaking
from mycroft.skills.core import FallbackSkill
from mycroft.util.log import LOG, getLogger
import random

_author__ = 'gras64'

LOGGER = getLogger(__name__)


class LearningSkill(FallbackSkill):
    def __init__(self):
        super(LearningSkill, self).__init__("LearningSkill")
        #self.settings.get('enable_fallback'),
        self.enable_fallback = "True"
        #self.settings.get('local_path'),
        self.local_path = "/home/pi/.mycroft/learning-skill/private"
        #self.settings.get('public_path'),
        self.public_path = "/home/pi/.mycroft/learning-skill/public"
        #self.settings.get('allow_category'),
        self.allow_category = ["humor", "love", "science"]
        #self.intent_path = "/home/pi/.mycroft/skills/LearningSkill/public/humor/vocab/de-de/hallo"
        self.privacy = ""
        self.catego = ""
        self.Category = ""


    def initialize(self):
        self.settings.get('public_path'),
        self.settings.get('local_path'),
        self.settings.get('allow_category'),
        self.settings.get('enable_fallback'),

        path = dirname(abspath(__file__))

        path_to_humor_words = join(path, 'vocab', self.lang, 'Humor.voc')
        self._humor_words = self._lines_from_path(path_to_humor_words)

        path_to_science_words = join(path, 'vocab', self.lang, 'Science.voc')
        self._science_words = self._lines_from_path(path_to_science_words)

        path_to_love_words = join(path, 'vocab', self.lang, 'Love.voc')
        self._love_words = self._lines_from_path(path_to_love_words)

        path_to_cancel_words = join(path, 'vocab', self.lang, 'Cancel.voc')
        self._cancel_words = self._lines_from_path(path_to_cancel_words)

        if self.settings.get('enable_fallback') == True:
            self.register_fallback(self.handle_fallback, 5)
        else:
            self.enable_fallback = False
        LOG.debug('Learning-skil-fallback enabled: %s' % self.enable_fallback)


    def _lines_from_path(self, path):
        with open(path, 'r') as file:
            lines = [line.strip().lower() for line in file]
            return lines

    def read_intent_lines(self, name, int_path):
        #self.speak(int_path)
        with open(self.find_resource(name + '.intent', int_path)) as f:
            #self.log.info('load intent: ' + f)
            return filter(bool, map(str.strip, f.read().split('\n')))


    def handle_fallback(self, message):

        utterance = message.data['utterance']
        path = self.local_path

        for f in os.listdir(path):
            int_path = path+"/"+f+"/"+"vocab"+"/"+self.lang
            try:
                self.report_metric('failed-intent', {'utterance': utterance})
            except:
                self.log.exception('Error reporting metric')

            for a in os.listdir(int_path):
                i = a.replace(".intent", "")
                for l in self.read_intent_lines(i, int_path):
                    if utterance.startswith(l):
                        self.log.debug('Fallback type: ' + i)
                        dig_path = path+"/"+f
                        e = join(dig_path, 'dialog', self.lang, i +'.dialog')
                        self.log.debug('Load Falback File: ' + e)
                        lines = open(e).read().splitlines()
                        i =random.choice(lines)
                        self.speak_dialog(i)
                        return True
            self.log.debug('fallback learning: ignoring')

        path = self.public_path
        for f in os.listdir(path):
            int_path = path+"/"+f+"/"+"vocab"+"/"+self.lang
            try:
                self.report_metric('failed-intent', {'utterance': utterance})
            except:
                self.log.exception('Error reporting metric')

            for a in os.listdir(int_path):
                i = a.replace(".intent", "")
                for l in self.read_intent_lines(i, int_path):
                    if utterance.startswith(l):
                        self.log.debug('Fallback type: ' + i)
                        dig_path = path+"/"+f
                        e = join(dig_path, 'dialog', self.lang, i +'.dialog')
                        self.log.debug('Load Falback File: ' + e)
                        lines = open(e).read().splitlines()
                        i =random.choice(lines)
                        self.speak_dialog(i)
                        return True
            self.log.debug('fallback learning: ignoring')


    #@intent_file_handler('Learning.intent')
    @intent_handler(IntentBuilder("").require("Query").optionally("Something").
                    optionally("Private").require("Learning"))
    def handle_interaction(self, message):
        private = message.data.get("Private", None)
        self.speak(private)
        if private is None:
            privacy = self.public_path
            catego = self.get_response("begin.learning")
        else:
            privacy = self.local_path
            catego = self.get_response("begin.private")
        #privacy = self.public_path
        if catego in self._humor_words:
            #self.speak("humor")
            Category = "humor"
        elif catego in self._science_words:
            #self.speak("science")
            Category = "science"
        elif catego in self._love_words:
            #self.speak("love")
            Category = "love"
        elif catego in self._cancel_words:
            self.speak_dialog("Cancel")
            return
        else:
            self.speak_dialog("invalid.category")
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
        answer_path = privacy+"/"+Category+"/"+"dialog"+"/"+self.lang
        question_path = privacy+"/"+Category+"/"+"vocab"+"/"+self.lang
        if not os.path.isdir(answer_path):
            os.makedirs(answer_path)
        if not os.path.isdir(question_path):
            os.makedirs(question_path)
        self.speak_dialog("save.learn",
                          data={"question": question,
                                "answer": answer},
                                expect_response=True)

        save_dialog = open(answer_path+"/"+keywords.replace(" ", ".")+".dialog", "a")
        save_dialog.write(answer+"\n")
        save_dialog.close()
        save_intent = open(question_path+"/"+keywords.replace(" ", ".")+".intent", "a")
        save_intent.write(question+"\n")
        save_intent.close()

    def shutdown(self):
        self.remove_fallback(self.handle_fallback)
        super(LearningSkill, self).shutdown()


def create_skill():
    return LearningSkill()
