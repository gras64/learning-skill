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
        self.privacy = ""
        self.catego = ""
        self.Category = ""

    def initialize(self):
        self.enable_fallback = self.settings.get("enable_fallback_ex", "True")
        self.public_path = self.settings.get('public_path_ex', self.file_system.path+"/public")
        self.local_path = self.settings.get('local_path_ex', self.file_system.path+"/private")
        self.allow_category = self.settings.get('allow_category_ex', "humor,love,science")
        LOG.debug('local path enabled: %s' % self.local_path)


        if self.enable_fallback is "True":
            self.register_fallback(self.handle_fallback, 5)
        LOG.debug('Learning-skil-fallback enabled: %s' % self.enable_fallback)

    def init_category(self, cat):
        path = dirname(abspath(__file__)) + '/vocab/'
        if os.path.isfile(path + self.lang + "/" + cat +'.voc'):
            path_to_words = path + self.lang + "/" + cat +'.voc'
            words = self._lines_from_path(path_to_words)
        else:
            path = self.file_system.path + "/category/"
            if os.path.isfile(path + self.lang + "/" + cat +'.voc'):
                path_to_words = path + self.lang + "/" + cat +'.voc'
                words = self._lines_from_path(path_to_words)
            else:
                self.add_category(cat, path)
                path_to_words = path + self.lang +"/"+ cat+'.voc'
                words = self._lines_from_path(path_to_words)
        return words

    def add_category(self, cat, path):
        path = path + "/"+ self.lang
        category = self.get_response("add.category",
                                    data={"cat": cat})
        if not os.path.isdir(path):
            os.makedirs(path)
        save_category = open(path +"/"+ cat+'.voc', "w")
        save_category.write(cat)
        save_category.close()
        return True

    def _lines_from_path(self, path):
        with open(path, 'r') as file:
            lines = [line.strip().lower() for line in file]
            return lines

    def read_intent_lines(self, name, int_path):
        # self.speak(int_path)
        with open(self.find_resource(name + '.intent', int_path)) as f:
            # self.log.info('load intent: ' + f)
            return filter(bool, map(str.strip, f.read().split('\n')))

    def handle_fallback(self, message):
        utterance = message.data['utterance']
        if os.path.exists(self.public_path):
            path = self.public_path
            return self.load_fallback(utterance, path)
        if os.path.exists(self.local_path):
            path = self.local_path
            return self.load_fallback(utterance, path)

    def load_fallback(self, utterance, path):
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
                            i = random.choice(lines)
                            self.speak_dialog(i)
                            return True
                self.log.debug('fallback learning: ignoring')
            return False

    @intent_handler(IntentBuilder("HandleInteraction").require("Query").optionally("Something").
                    optionally("Private").require("Learning"))
    def handle_interaction(self, message):
        private = message.data.get("Private", None)
        if private is None:
            privacy = self.public_path
            catego = self.get_response("begin.learning")
        else:
            privacy = self.local_path
            catego = self.get_response("begin.private")
        privacy = self.public_path
        Category =""
        for cat in self.allow_category.split(","):
            if catego in self.init_category(cat):
                Category = cat # set category
        if not Category:
            self.speak_dialog("invalid.category")
            return
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
                                expect_response = True)

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
