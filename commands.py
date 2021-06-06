import json
import os
import difflib
import subprocess
import webbrowser
import speech_recognition as sr
import time
import math
import logging
import pyaudio
import collections
import struct
import vlc


class VoiceRecognizer:
    def __init__(self, tray_interface=None):
        self.recognizer = sr.Recognizer()
        self.stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                             channels=1,
                                             rate=16000,
                                             input=True,
                                             output=True,
                                             frames_per_buffer=1024)
        self.tray_interface = tray_interface

    def rms(self, frame, width, short_normalize):
        count = len(frame) / width
        format = "%dh" % (count)
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * short_normalize
            sum_squares += n * n
        rms = math.pow(sum_squares / count, 0.5)

        return rms * 1000

    def record(self, stream, rate):
        threshold = 10
        short_normalize = (1.0 / 32768.0)
        chunk = 1024
        width = 2
        timeout_length = 1

        while True:
            input = stream.read(chunk)
            rms_val = self.rms(input, width, short_normalize)
            if rms_val > threshold:
                break

        print('Шум обнаружен, началась запись')
        logging.info('Шум обнаружен, началась запись')

        if self.tray_interface is not None:
            self.tray_interface.set_correct()

        rec = collections.deque()
        current = time.time()
        end = time.time() + timeout_length

        while current <= end and len(rec) <= 124:
            data = stream.read(chunk)
            if self.rms(data, width, short_normalize) >= threshold: end = time.time() + timeout_length
            current = time.time()
            rec.append(data)

        if self.tray_interface is not None:
            self.tray_interface.set_default()

        logging.info('Запись остановлена')
        return sr.AudioData(b"".join(rec), rate, width)

    def recognize_voice(self):
        audio = self.record(self.stream, 16000)
        return self.recognizer.recognize_google(audio, language="ru-RU")


def predict_command_by_name(predict_name, commands):
    result = (None, None)
    best_match = 50
    tuples = [(predict_name, '')]
    split = predict_name.split()
    if len(split) > 1:
        tuples = []
        for i in range(1, len(split) + 1):
            tuples.insert(0, (" ".join(split[0:i]), " ".join(split[i:])))

    for t in tuples:
        for command in commands:
            seq = difflib.SequenceMatcher(None, command.name, t[0].lower()).ratio() * 100
            if best_match < seq:
                result = (command, t[1])
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

    def run(self, argument=None):
        pass


class OpenBrowserCommand(Command):
    def __init__(self):
        super().__init__('Открыть браузер')

    def run(self, argument=None):
        webbrowser.open("https://google.com")


class CloseBrowserCommand(Command):
    def __init__(self):
        super().__init__('Закрой браузер')

    def run(self, argument=None):
        r = webbrowser.get()
        os.system("pkill firefox")


class ClosePlayerCommand(Command):
    def __init__(self):
        super().__init__('Закрой плеер')

    def run(self, argument=None):
        os.system("pkill vlc")


class Exit(Command):
    def __init__(self, app):
        self.app = app
        super().__init__('Выключайся')

    def run(self, argument=None):
        self.app.quit()


class OpenNewsCommand(Command):
    def __init__(self):
        super().__init__('Открыть новости')

    def run(self, argument=None):
        webbrowser.open("https://yandex.ru/news/")


class FindCommand(Command):
    def __init__(self):
        super().__init__('Найти')

    def run(self, argument=None):
        webbrowser.open('https://yandex.ru/search/?text=' + argument)


class CloseCommand(Command):
    def __init__(self):
        super().__init__('Закрой калькулятор')

    def run(self, argument=None):
        os.system("pkill galculator")


class RadioCommand(Command):
    def __init__(self):
        self.current_index_radio = 0
        file = open("stantions.json", 'r', encoding='utf-8')  # открываем файл на чтение
        data = json.load(file)  # загружаем из файла данные в словарь data
        file.close()
        self.radios = data;
        self.player = vlc.MediaPlayer("http://eptop128server.streamr.ru:8033/eptop128")
        self.player.audio_set_volume(20)
        super().__init__('Радио')

    def run(self, argument=None):
        if argument == 'включить':
            self.player.play()
        elif argument == 'выключить':
            self.player.stop()
        elif argument == 'громче':
            self.player.audio_set_volume(self.player.audio_get_volume() - 10)
        elif argument == 'тише':
            self.player.audio_set_volume(self.player.audio_get_volume() + 10)
        elif argument == 'следующая станция':
            self.current_index_radio += 1
            if self.current_index_radio >= len(self.radios):
                self.current_index_radio = 0
            self.player.set_mrl(self.radios[self.current_index_radio])
            self.player.play()
        elif argument == 'предыдущая станция':
            self.current_index_radio -= 1
            if self.current_index_radio < 0:
                self.current_index_radio = len(self.radios)-1
            self.player.set_mrl(self.radios[self.current_index_radio])
            self.player.play()


class ShellCommand(Command):
    def __init__(self, name, path):
        super().__init__(name)
        self.path = path

    def run(self, argument=None):
        if not os.path.exists(self.path):
            raise FileNotFoundError("Command file not found")
        if self.path.lower().endswith(('cmd', 'sh')):
            process = subprocess.Popen([self.path, self.name])
        else:
            raise FileExistsError("File extensions must be sh or cmd")
