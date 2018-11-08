from mycroft import MycroftSkill, intent_file_handler


class Learning(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('learning.intent')
    def handle_learning(self, message):
        self.speak_dialog('learning')


def create_skill():
    return Learning()

