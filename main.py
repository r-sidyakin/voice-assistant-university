import collections
import struct
from threading import Thread
import speech_recognition as sr
import pyaudio
import wave
import audioop
from collections import deque
import os
import urllib
import time
import math
from tray import SystemTrayIconVoiceAssistant
from commands import predict_command_by_name, OpenBrowserCommand


def rms(frame, width, short_normalize):
    count = len(frame) / width
    format = "%dh" % (count)
    shorts = struct.unpack(format, frame)

    sum_squares = 0.0
    for sample in shorts:
        n = sample * short_normalize
        sum_squares += n * n
    rms = math.pow(sum_squares / count, 0.5)

    return rms * 1000


def record(stream, rate, icon):
    threshold = 10
    short_normalize = (1.0 / 32768.0)
    chunk = 1024
    width = 2
    timeout_length = 1

    while True:
        input = stream.read(chunk)
        rms_val = rms(input, width, short_normalize)
        if rms_val > threshold:
            break

    print('Шум обнаружен, началась запись')
    icon.set_correct()
    rec = collections.deque()
    current = time.time()
    end = time.time() + timeout_length

    while current <= end:
        data = stream.read(chunk)
        if rms(data, width, short_normalize) >= threshold: end = time.time() + timeout_length
        current = time.time()
        rec.append(data)

    icon.set_default()
    print('Запись остановлена')
    return sr.AudioData(b"".join(rec), rate, width)


class Worker(Thread):
    def __init__(self, icon):
        super().__init__()
        self.icon = icon

    def run(self):
        recognizer = sr.Recognizer()
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        output=True,
                        frames_per_buffer=1024)
        commands = [OpenBrowserCommand()]
        key_phrase = 'генри'
        while True:
            try:
                print("Говорите")
                audio = record(stream, 16000, self.icon)
                data = recognizer.recognize_google(audio, language="ru-RU")
                print("Вы сказали: " + data.lower())
                voice_text = data.lower()
                command = predict_command_by_name(voice_text, commands)

                if not voice_text.startswith(key_phrase):
                    print(voice_text, 'не с ключевой')
                    continue

                if command is not None:
                    command.run()
                else:
                    print("Такой команды нет")

            except Exception as e:
                print(e)


def main():
    icon = SystemTrayIconVoiceAssistant()
    worker = Worker(icon)
    worker.daemon = True
    worker.start()
    icon.start_processor()


if __name__ == '__main__':
    main()
