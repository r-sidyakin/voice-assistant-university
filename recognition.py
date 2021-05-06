import json
import os
import subprocess
import string
import fuzz as fuzz
import vlc
import speech_recognition as sr
from fuzzywuzzy import fuzz

current_radio = None


def Execute_command(commands, name):
    need_command = None
    best_ratio = 0
    global current_radio
    try:
        if (name.find("найди") != -1):
            request = str(name[6:]).replace(" ", "%20")

            os.system('start https://yandex.ru/search/?text=' + request)
            print("ищу" + str(name[6:]))
            return
        if (name == "тише"):
            print("делаю тише")
            prev_volume = current_radio.audio_get_volume()
            # print(prev_volume)
            current_radio.audio_set_volume(prev_volume - 10)
            # print(current_radio.audio_get_volume())
            return
        if (name == "громче"):
            print("делаю громче")
            current_radio.audio_set_volume(current_radio.audio_get_volume() + 10)
            return
        if (name.find("громкость") != - 1):
            print("da gromkost")
            print(name[10:])
            current_radio.audio_set_volume(int(name[10:]))
            return
    except:
        pass
    for command in commands:
        if fuzz.ratio(command.name, name) > best_ratio:
            need_command = command
            best_ratio = fuzz.ratio(command.name, name)
    if (best_ratio >= 53):
        print("Подходящая комманда :" + need_command.name)
        print(best_ratio)
        # global current_radio
        if (need_command.name.find("радио") != -1):
            try:
                current_radio.stop()
            except:
                pass
            try:
                current_radio = None
                need_command.url

                current_radio = need_command.run()
                print("Включаем радио")
                print(current_radio.audio_get_volume())
                return
            except:
                pass
        if (need_command.name == "выключи радио"):
            print("ВЫключаем радио")
            current_radio.stop()

            current_radio = None
            return

        need_command.run()
    else:
        print("Ниче не понял")
        print(best_ratio)
        return


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
        print(os.system('start ' + self.path))


class CommandRadio(Command):

    def __init__(self, name, url=None):
        super().__init__(name)
        self.url = url

    def run(self):
        p = vlc.MediaPlayer(self.url)
        p.play()
        return p

    # except:
    # print("Ошибка работы с радио")
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

    def load_radio(self, path):
        file = open(path, 'r', encoding='utf-8')  # открываем файл на чтение
        data = json.load(file)  # загружаем из файла данные в словарь data
        file.close()
        radioList = []
        for element_array in data:
            new_radio = CommandRadio("включи радио " + element_array["name"], element_array["url"])
            radioList.append(new_radio)
        return radioList


loader = CommandsLoader()
commands = loader.load_commands('test.json')
radio_list = loader.load_radio('radio.json')
for el in radio_list:
    commands.append(el)
# commands.append(loader.load_radio('radio.json'))
commands.append(CommandRadio("включи радио", "http://eptop128server.streamr.ru:8033/eptop128"))
commands.append(CommandRadio("радио", "http://eptop128server.streamr.ru:8033/eptop128"))
commands.append(CommandRadio("выключи радио"))
commands.append(CommandRadio("тише"))
commands.append(CommandRadio("громче"))


# Пример работы команд
# ExecuteCommand(commands, "Время")
# ExecuteCommand(commands, "Открыть браузер")
# Execute_command(commands, "Радио")
# Execute_command(commands, "Открыть браузер")
def Recognize_command():
    r = sr.Recognizer()
    with sr.Microphone(device_index=1)as source:
        print("Говорите");
        audio = r.listen(source)
        data = r.recognize_google(audio, language="ru-RU")
        print("Вы сказали: " + data.lower())
        return data.lower()


# s="включи радио европа плюс"
# print(s.find("европа плюс"))
while True:
    # print(fuzz.ratio("привет","привет"))
    try:
        Execute_command(commands, Recognize_command())
    except:
        print('Команда не распознана')
input()
