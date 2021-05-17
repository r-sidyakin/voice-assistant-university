import os
import difflib
import webbrowser


class Command:
    def __init__(self, name):
        self.name = name

    def run(self):
        pass


class OpenBrowserCommand(Command):
    def __init__(self):
        super().__init__('Открыть браузер')

    def run(self):
        webbrowser.open("https://google.com")


def predict_command_by_name(predict_name, commands):
    result = None
    best_match = 45
    for command in commands:
        seq = difflib.SequenceMatcher(None, command.name, predict_name.lower()).ratio() * 100
        if best_match < seq:
            result = command
            best_match = seq

    return result
