import os
import sys
from threading import Thread
import time

from PySide2.QtCore import QRunnable, QThreadPool

from tray import SystemTrayIconVoiceAssistant




def main():

    icon = SystemTrayIconVoiceAssistant()
    input()


if __name__ == '__main__':
    main()
