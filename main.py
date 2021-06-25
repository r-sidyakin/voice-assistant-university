import difflib
import time
from threading import Thread

from speech_recognition import UnknownValueError

from tray import SystemTrayIconVoiceAssistant
from commands import *
import logging
import keyboard
from logging.handlers import RotatingFileHandler
class Worker(Thread):

    def __init__(self, icon, seqLevel, key_phrase='помощник',bestMatch=50,key="c",slen=10,app_log=None):
        super().__init__()
        self.icon = icon
        self.seqLevel=seqLevel
        self.key_phrase=key_phrase
        self.bestMatch=bestMatch
        self.key = key
        self.slen=slen
        self.app_log=app_log
    def check_log(self,maxCount):
        logfile=open("app.log",'r')
        list=logfile.readlines()
        count=len(list)
        logfile.close()

        print(count)
        if (count > maxCount):
            print("замена очка")
            # os.remove("app.log")
            logfilew=open("app.log",'w')
            for el in list:
                el = ' '.join(el.split())
                print("+",el)
            print(list[count - maxCount:count])
            logfilew.writelines(list[count-maxCount:count])
            logfilew.close()


        #print(count)
    def run(self):
        recognizer = VoiceRecognizer(self.icon)
        commands = [OpenBrowserCommand(), OpenNewsCommand(), FindCommand(), RadioCommand(), CloseCommand(),
                    CloseBrowserCommand(), Exit(self.icon.app), ClosePlayerCommand()]
        commands.extend(load_commands("commands.json"))
        #key_phrase = 'помощник'
        
        self.key_phrase=self.key_phrase.lower()
        while True:
            time.sleep(0.5)
            try:
                self.check_log(self.slen)
            except:
                pass
            print(self.icon.checkkey())
            # if self.keymode=="True":
            #     keyboard.wait(self.key)
            if self.icon.checkkey()==True:
                #keyboard.wait(self.key)
                if not keyboard.is_pressed(self.key):
                    continue
            try:
                self.icon.set_default()
                print("Говорите")
                data = recognizer.recognize_voice()
                print("Вы сказали: " + data.lower())
                self.app_log.info("Вы сказали: " + data.lower())
                voice_text = data.lower()

                if len(voice_text) < len(self.key_phrase):
                    continue

                seq = difflib.SequenceMatcher(None, self.key_phrase, voice_text[0:len(self.key_phrase)]).ratio() * 100

                if seq < self.seqLevel and self.icon.checkkey()==False:
                    print('не с ключевой')
                    self.app_log.error('ключевое слово не распознано: ' + data.lower())
                    self.icon.set_error()
                    continue

                if self.icon.checkkey()==False:
                    command, argument = predict_command_by_name(voice_text[len(self.key_phrase):].strip(), commands, self.bestMatch)
                else:
                    command, argument = predict_command_by_name(voice_text, commands,
                                                                self.bestMatch)
                if command is not None:
                    command.run(argument if len(argument) != 0 else None)
                else:
                    self.app_log.info("Такой команды нет: " + data.lower())
                    self.icon.set_error()
            except Exception as e:
                print(e)
                if e.__class__ == UnknownValueError:
                    continue
                self.icon.set_error()


def main():
    file_settings = open("settings.json", 'r', encoding='utf-8')  # открываем файл на чтение
    settings_data = json.load(file_settings)  # загружаем из файла данные в словарь data
    file_settings.close()
    try:
        slen=settings_data[4]
        key=settings_data[3]
        #keymode=settings_data[3]
        bestMatch=settings_data[2]
        seqLevel=settings_data[1]
        key_word=settings_data[0]
    except:
        pass
    #keyboard.add_hotkey('f', lambda: print('Hello'))
    #keyboard.wait("s")
    # logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s',
    #                     level=logging.INFO)
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    logFile = 'app.log'

    my_handler = RotatingFileHandler(logFile, mode='a',
                                     backupCount=0, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)

    app_log.addHandler(my_handler)

    icon = SystemTrayIconVoiceAssistant()
    worker = Worker(icon, seqLevel,key_word,bestMatch,key,slen,app_log)
    worker.daemon = True
    worker.start()
    icon.start_processor()


if __name__ == '__main__':
    main()
