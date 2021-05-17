import json
import os
import difflib
import webbrowser


def predict_command_by_name(predict_name, commands):
    result = None
    best_match = 45
    for command in commands:
        seq = difflib.SequenceMatcher(None, command.name, predict_name.lower()).ratio() * 100
        if best_match < seq:
            result = command
            best_match = seq

    return result


def load_commands(path):
    file = open(path, 'r', encoding='utf-8')  # открываем файл на чтение
    data = json.load(file)  # загружаем из файла данные в словарь data
    file.close()
    commands = []
    for element_array in data:
        new_command = ShellCommand(element_array["name"], element_array["path"])
        commands.append(new_command)
    return commands


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


class OpenCalcCommand(Command):
    def __init__(self):
        super().__init__('Открыть калькулятор')

    def run(self):
        os.system("start calc")


class ShellCommand(Command):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path

    def run(self):
        print(os.system('start ' + self.path))
