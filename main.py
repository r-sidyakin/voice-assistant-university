import time
from threading import Thread

from speech_recognition import UnknownValueError

from tray import SystemTrayIconVoiceAssistant
from commands import predict_command_by_name, OpenBrowserCommand, OpenNewsCommand, load_commands, VoiceRecognizer
import logging


class Worker(Thread):
    def __init__(self, icon):
        super().__init__()
        self.icon = icon

    def run(self):
        recognizer = VoiceRecognizer(self.icon)
        commands = [OpenBrowserCommand(), OpenNewsCommand()]
        commands.extend(load_commands("commands.json"))
        key_phrase = 'помощник'
        while True:
            try:
                print("Говорите")
                data = recognizer.recognize_voice()
                print("Вы сказали: " + data.lower())
                logging.info("Вы сказали: " + data.lower())
                voice_text = data.lower()

                if not voice_text.startswith(key_phrase):
                    print('не с ключевой')
                    logging.info('не с ключевой')
                    self.icon.set_error()
                    time.sleep(1)
                    self.icon.set_default()
                    continue

                command = predict_command_by_name(voice_text[len(key_phrase):].strip(), commands)

                if command is not None:
                    command.run()
                else:
                    logging.info("Такой команды нет")
                    self.icon.set_error()
                    time.sleep(1)
                    self.icon.set_default()

            except Exception as e:
                print(e)
                if e.__class__ == UnknownValueError:
                    continue

                self.icon.set_error()
                time.sleep(1)
                self.icon.set_default()


def main():
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    icon = SystemTrayIconVoiceAssistant()
    worker = Worker(icon)
    worker.daemon = True
    worker.start()
    icon.start_processor()


if __name__ == '__main__':
    main()
