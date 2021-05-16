import os
import difflib


class Command:
    def __init__(self, name):
        self.name = name

    def run(self):
        pass


def predict_command_by_name(predictName, commands):
    result = None
    bestMatch = 45
    for command in commands:
        seq = difflib.SequenceMatcher(None, command.name, predictName).ratio() * 100

        if bestMatch < seq:
            result = command
            bestMatch = seq

    return result


class OpenBrowserCommand(Command):
    def __init__(self):
        super().__init__('Открыть браузер')

    def run(self):
        os.system('start www.google.com')


stroka = 'зарыть браузер'
bc = OpenBrowserCommand()

res = predict_command_by_name(stroka, [bc])

