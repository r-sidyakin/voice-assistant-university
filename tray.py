import subprocess
import sys
import os
from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QRunnable, QThreadPool


class SystemTrayIconVoiceAssistant(QtWidgets.QSystemTrayIcon):

    def start_processor(self):
        self.app.exec_()

    def __init__(self):
        self.pathIconDefault = "icons/icon_default.png"
        self.pathIconCorrect = "icons/icon_correct.png"
        self.pathIconExit = "icons/icon_error.png"

        self.app = QtWidgets.QApplication()
        self.w = QtWidgets.QWidget()
        QtWidgets.QSystemTrayIcon.__init__(self, QtGui.QIcon(self.pathIconDefault), self.w)

        self.setToolTip(f'Voice Assistant')
        menu = QtWidgets.QMenu(self.w)

        set_def = menu.addAction("Open Log file")
        set_def.triggered.connect(self.openLog)

        set_def = menu.addAction("Open json file")
        set_def.triggered.connect(self.openJson)
        self.keyModeMenu = menu.addAction("Active key")
        self.keyModeMenu.setCheckable(True)
        self.keyModeMenu.triggered.connect(self.checkkey)

        exit_ = menu.addAction("Exit")

        exit_.triggered.connect(lambda: sys.exit())

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)
        self.show()

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            self.set_default()
    def checkkey(self):
        return self.keyModeMenu.isChecked()
    def openLog(self):
        if sys.platform == "win32":
            os.startfile('app.log')
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, 'app.log'])

    def openJson(self):
        if sys.platform == "win32":
            os.startfile('commands.json')
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, 'commands.json'])

    def set_default(self):
        self.update_Icon(self.pathIconDefault)

    def set_correct(self):
        self.update_Icon(self.pathIconCorrect)

    def set_error(self):
        self.update_Icon(self.pathIconExit)

    def update_Icon(self, path):
        self.setIcon(QtGui.QIcon(path))
