from threading import Thread
import speech_recognition as sr

from tray import SystemTrayIconVoiceAssistant


class Worker(Thread):
    def __init__(self, icon):
        super().__init__()
        self.icon = icon

    def run(self):
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        while True:
            with microphone as source:
                try:
                    print("Говорите")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source)
                    data = recognizer.recognize_google(audio, language="ru-RU")
                    print("Вы сказали: " + data.lower())
                except Exception as e:
                    print(e)


def main():
    icon = SystemTrayIconVoiceAssistant()
    worker = Worker(icon)
    worker.daemon = True
    worker.start()
    print('dsadsa')
    icon.start_processor()


if __name__ == '__main__':
    main()
