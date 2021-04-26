import json
import os
import subprocess
import vlc
import speech_recognition as sr

def Execute_command(commands, name):
    for command in commands:
        if command.name == name:
            command.run()


class Command:
    def __init__(self, name):
        self.name = name

    def run(self):
        pass


class ShellCommand(Command):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path

    def run(self):
        print("hehe")
        print(os.system('start ' + self.path))


class CommandRadio(Command):
    def __init__(self, name):
        super().__init__(name)

    def run(self):
        p = vlc.MediaPlayer("http://eptop128server.streamr.ru:8033/eptop128")
        p.play()
        # subprocess.call(self.path_to_command, shell=True)
        # exec(open(self.path_to_command).read())


# python start script from another script
# subprocess start another script
# subprocess deatached

class CommandsLoader:
    def load_commands(self, path):
        file = open(path, 'r', encoding='utf-8')  # открываем файл на чтение
        data = json.load(file)  # загружаем из файла данные в словарь data
        file.close()
        commands = []
        for element_array in data:
            new_command = ShellCommand(element_array["name"], element_array["path"])
            commands.append(new_command)
        return commands


loader = CommandsLoader()
commands = loader.load_commands('test.json')
commands.append(CommandRadio("радио"))

# Пример работы команд
# ExecuteCommand(commands, "Время")
# ExecuteCommand(commands, "Открыть браузер")
#Execute_command(commands, "Радио")
#Execute_command(commands, "Открыть браузер")
def Recognize_command():

    r=sr.Recognizer()
    with sr.Microphone(device_index=1)as source:
        print("Скажи");
        audio=r.listen(source)
        data=r.recognize_google(audio, language ="ru-RU")
        print("Вы сказали: " + data.lower())
        return data.lower()

Execute_command(commands,Recognize_command())
input()
