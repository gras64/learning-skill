from adapt.intent import IntentBuilder
from os.path import join, dirname, abspath, os, sys
from mycroft.messagebus.message import Message
from mycroft import intent_handler, intent_file_handler
from mycroft.filesystem import FileSystemAccess
from mycroft.audio import wait_while_speaking
from mycroft.skills.core import FallbackSkill
from mycroft.util.log import LOG, getLogger
from mycroft.util import resolve_resource_file
from mycroft.util.parse import match_one
from mycroft.skills.msm_wrapper import build_msm_config, create_msm
from mycroft.configuration.config import Configuration
import re
import time
from msm import (
    MultipleSkillMatches,
    SkillNotFound,
)
import random

_author__ = 'gras64'

LOGGER = getLogger(__name__)


class LearningSkill(FallbackSkill):
    _msm = None #### From installer skill

    def __init__(self):
        super(LearningSkill, self).__init__("LearningSkill")
        self.privacy = ""
        self.catego = ""
        self.Category = ""

    def initialize(self):
        self.enable_fallback = self.settings.get('enable_fallback_ex') \
            if self.settings.get('enable_fallback_ex') is not None else True
        self.public_path = self.settings.get('public_path_ex') \
            if self.settings.get('public_path_ex') else self.file_system.path+"/public"
        self.local_path = self.settings.get('local_path_ex') \
            if self.settings.get('local_path_ex') else self.file_system.path+"/private"
        self.allow_category = self.settings.get('allow_category_ex') \
            if self.settings.get('allow_category_ex') else "humor,love,science"
        LOG.debug('local path enabled: %s' % self.local_path)
        self.save_path = self.file_system.path+"/mycroft-skills"
        self.saved_utt = ""
        self.save_answer = ""
        if self.enable_fallback is True:
            self.register_fallback(self.handle_fallback, 6)
            self.register_fallback(self.handle_save_fallback, 99)
            self.add_event('speak',
                            self.save_action)
        LOG.debug('Learning-skil-fallback enabled: %s' % self.enable_fallback)
        skillfolder = Configuration.get()['skills']['directory']
        self.log.info(skillfolder+"/PootleSync/mycroft-skills")
        if 'translations_dir' in Configuration.get(): ##path of second language files
            self.lang_path = Configuration.get()['translations_dir']
            self.log.info("set lang path to translation_dir")
        elif os.path.isdir(skillfolder+"/PootleSync/mycroft-skills"):
            self.lang_path = skillfolder+"/PootleSync/mycroft-skills"
            self.log.info("set lang path to PootleSync")
        else:
            self.lang_path = None
            self.log.info("set lang path to skill path")

    def add_category(self, cat):
        path = self.file_system.path + "/category/"+ self.lang
        Category = self.get_response("add.category",
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
        #self.log.info(int_path+name)
        with open(self.find_resource(name + '.intent', int_path)) as f:
            #self.log.info('load intent: ' + str(f))
            return filter(bool, map(str.strip, f.read().split('\n')))

    def handle_fallback(self, message):
        utterance = message.data['utterance']
        if os.path.exists(self.public_path):
            path = self.public_path
            return self.load_fallback(utterance, path)
        if os.path.exists(self.local_path):
            path = self.local_path
            return self.load_fallback(utterance, path)
    
    def save_action(self, message):
        self.save_answer = message.data['utterance']
        #self.save_skill = message.data['skill_id']
        self.log.info('save output for learning')

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
    def handle_interaction(self, message, Category=None, saved_utt=None):
        private = message.data.get("Private", None)
        if private is None:
            privacy = self.public_path
            if Category is None:
                catego = self.get_response("begin.learning")
        else:
            privacy = self.local_path
            if Category is None:
                catego = self.get_response("begin.private")
        if Category is None:
            for cat in self.allow_category.split(","):
                try:
                    if self.voc_match(catego, cat):
                        Category = cat
                except:
                    self.add_category(cat)
            if Category is None:        
                self.speak_dialog("invalid.category")
                return
        #privacy = self.public_path
        if saved_utt is None:
            question = self.get_response("question")
        else:
            self.log.info("become utt2"+saved_utt)
            question = saved_utt
            self.log.info("become utt"+question)
            
        if not question:
            self.log.info("stop")
            return  # user cancelled
        keywords = self.get_response("keywords")
        if not keywords:
            return  # user cancelled
        answer = self.get_response("answer")
        if not answer:
            return  # user cancelled
        answer_path = privacy+"/"+Category+"/"+"dialog"+"/"+self.lang+"/"
        question_path = privacy+"/"+Category+"/"+"vocab"+"/"+self.lang+"/"
        confirm_save = self.ask_yesno(
            "save.learn",
            data={"question": question, "answer": answer})
        if confirm_save != "yes":
            self.log.debug('new knowledge rejected')
            return  # user cancelled
        self.write_file(answer_path, answer, keywords.replace(" ", ".")+".dialog")
        self.write_file(question_path, question, keywords.replace(" ", ".")+".intent")

    def write_file(self, path, data, filename):
        if not os.path.isdir(path):
            os.makedirs(path)
        save_dialog = open(path+filename, "a")
        save_dialog.write(data+"\n")
        save_dialog.close()
        self.log.debug('new knowledge saved')

    def shutdown(self):
        self.remove_fallback(self.handle_fallback)
        self.remove_fallback(self.handle_save_fallback)
        super(LearningSkill, self).shutdown()

    def handle_save_fallback(self, message):
        self.saved_utt = message.data['utterance']
        self.log.info('save utterance for learning')

    @intent_file_handler('will_let_you_know.intent')
    def will_let_you_know_intent(self, message):
        catego = message.data.get("category")
        Category = None
        for cat in self.allow_category.split(","):
            try:
                if self.voc_match(catego, cat):
                    Category = cat
            except:
                self.add_category(cat)
        if not self.saved_utt is None:
            saved_utt = self.saved_utt
        else:
            saved_utt = None
        self.log.info("find Category: "+str(Category)+" and saved  utt: "+str(saved_utt))
        self.handle_interaction(message, Category, saved_utt)

    @intent_file_handler('say.differently.intent')
    def say_differently_intent(self, message):
        self.saved_answer = self.save_answer
        skills = [skill for skill in self.msm.all_skills if skill.is_local]
        for skill in skills:
            if not self.saved_answer is None:
                self.dialog_match(self.saved_answer, skill)
    
    def dialog_match(self, saved_dialog, skill):        
        if self.lang_path == None:
            path = skill.path
        else:
            path = self.lang_path+"/"+skill.name
        for root, dirs, files in os.walk(path):
            for f in files:
                ### for intent files
                filename = os.path.join(root, f)
                if self.lang in filename: ## reduce selection to reduce load list size
                    if filename.endswith(".dialog"):
                        match, confidence = match_one(self.saved_answer, self._lines_from_path(filename))
                        self.log.info("match "+str(match)+ " confidence "+ str(confidence))
                        if confidence > 0.8:
                            saved_utt = self.get_response("found.output", data={"match": match})
                            if saved_utt is not None:
                                match, saved_utt = self.var_found(saved_utt, match)
                                self.ask_save_intent_dialog(saved_utt, filename, match, skill)
                                acknowledge()
                            else:
                                self.speak_dialog("cancel")

                    #i = filename.replace(".dialog", "")


    @intent_file_handler('something_for_my_skill.intent')
    def something_for_my_skill_intent(self, message):
        utt_skill = message.data['skill']
        skills = [skill for skill in self.msm.all_skills if skill.is_local]
        for skill in skills:
            if str(utt_skill) in str(skill):
                self.log.info("find Skill: "+str(skill.name))
                if not self.saved_utt is None:
                    saved_utt = self.saved_utt
                    self.intent_match(saved_utt, skill, ".intent")
                else:
                    self.speak_dialog("no.old.inquiry")

    def intent_match(self, saved_utt, skill):
        vocs = []
        if self.lang_path == None:
            path = skill.path
        else:
            path = self.lang_path+"/"+skill.name
        for root, dirs, files in os.walk(path):
            for f in files:
                ### for intent files
                filename = os.path.join(root, f)
                if filename.endswith(".intent"):
                    i = filename.replace(".intent", "")
                    #for l in self.read_intent_lines(i, filename):
                    #self.log.info("test2"+str(self._lines_from_path(filename)))
                    match, confidence = match_one(saved_utt, self._lines_from_path(filename))
                    self.log.info("match "+str(match)+ " confidence "+ str(confidence))
                    if confidence > 0.5:
                        match, saved_utt = self.var_found(saved_utt, match)
                        self.ask_save_intent_dialog(saved_utt, filename, match, skill)
                        self.bus.emit(Message('recognizer_loop:utterance',
                              {"utterances": [match],
                               "lang": self.lang,
                               "session": skill.name}))
                        break
                #### for voc files
                if filename.endswith('.voc'):
                    vocs = vocs + [filename]
            exefile = skill.path+"/__init__.py"
            self.log.info(str(vocs))
            self.match_vocs(exefile, vocs)

    def match_vocs(self, exefile, vocs):
        fobj = open(exefile).read()
        #self.log.info(fobj)
        intents = re.findall(r"IntentBuilder.+\n.+", fobj, flags=re.M)
        for intent in intents:
            intent = str(intent).replace("\n", "").replace(" ", "")
            self.log.info(intent)       
        #fobj.close()
                


    def var_found(self, saved_utt, match):
        var = re.findall('{\S+}', match)#.replace("{", "").replace("}")
        if not var is None:
            for f in var:
                get = self.get_response("var.found", data={"var": f})
                self.log.info("become get "+str(get)+" match "+match+ " f "+f)
                e = f.replace("{", "").replace("}", "")
                i = 1
                while True and i <= 3:
                    if e in match:
                        self.log.info("found get "+str(get))
                        saved_utt = saved_utt.replace(get, f)
                        match = match.replace(f, get)
                        self.log.info("found get "+str(get))
                        break
                    elif i > 3:
                        get = self.get_response("second.try")
                        self.log.info("not found get"+str(get))
                        i = i + 1
                    else:
                        self.speak_dialog("no.old.inquiry")
                        pass
                    time.sleep(2)
        return match, saved_utt
        
    def ask_save_intent_dialog(self, saved_utt, filename, match, skill):
        confirm_save = self.ask_yesno(
            "save.update",
            data={"question": saved_utt})
        if confirm_save != "yes":
            self.log.debug('new knowledge rejected')
            return  # user cancelled
        if self.lang_path == None:
            path = self.save_path+"/"+skill.name+"/locale/"+self.lang+"/"
        else:
            path = self.lang_path+"/"+skill.name+"/locale/"+self.lang+"/"  
        filename = os.path.basename(filename)
        self.log.info("save querey"+str(path)+" filename "+filename+ "saved_utt "+saved_utt)
        self.write_file(path, saved_utt, filename)
        match = self.filter_sentence(match)
        self.log.info("match "+match)

    def filter_sentence(self, sentence): # filter intents data for utter event 
        sentence = re.sub(r'(\|\s?\w+)','', sentence, flags=re.M) # select one for poodle (emty|full)
        sentence = re.sub(r'[()%]|(^\\.+)*|(^#+\s?.*)', '', sentence, flags=re.M) # for poodle
        sentence = re.sub(r'(#+\s?.*)|(^[,.: ]*)', '', sentence, flags=re.M)
        sentence = sentence.replace('|', ' ').replace('  ', ' ')

        return sentence


    
    def find_skill(self, param, local): #### From installer skill
        """Find a skill, asking if multiple are found"""
        try:
            return self.msm.find_skill(param)
        except MultipleSkillMatches as e:
            skills = [i for i in e.skills if i.is_local == local]
            or_word = self.translate('or')
            if len(skills) >= 10:
                self.speak_dialog('error.too.many.skills')
                raise StopIteration
            names = [self.clean_name(skill) for skill in skills]
            if names:
                response = self.get_response(
                    'choose.skill', num_retries=0,
                    data={'skills': ' '.join([
                        ', '.join(names[:-1]), or_word, names[-1]
                    ])},
                )
                if not response:
                    raise StopIteration
                return self.msm.find_skill(response, skills=skills)
            else:
                raise SkillNotFound(param)
        
    @property #### From installer skill
    def msm(self):
        if self._msm is None:
            msm_config = build_msm_config(self.config_core)
            self._msm = create_msm(msm_config)

        return self._msm



def create_skill():
    return LearningSkill()
