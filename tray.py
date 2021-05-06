import sys

from PySide2 import QtWidgets, QtGui
from PySide2.QtCore import QRunnable, QThreadPool


class Worker(QRunnable):

    def __init__(self, app):
        super().__init__()
        self.app = app

    def run(self):
        self.app.exec_()


class SystemTrayIconVoiceAssistant(QtWidgets.QSystemTrayIcon):

    def __init__(self):
        QtWidgets.QSystemTrayIcon.__init__(self, QtGui.QIcon("icons/icon_default.png"), self.w)

        self.pathIconDefault = "icons/icon_default.png"
        self.pathIconCorrect = "icons/icon_correct.png"
        self.pathIconExit = "icons/icon_error.png"

        self.app = QtWidgets.QApplication()
        self.w = QtWidgets.QWidget()

        self.setToolTip(f'Voice Assistant')
        menu = QtWidgets.QMenu(self.w)

        set_def = menu.addAction("Set default")
        set_def.triggered.connect(self.set_default)
        set_def.setIcon(QtGui.QIcon(self.pathIconDefault))

        set_corr = menu.addAction("Set correct")
        set_corr.triggered.connect(self.set_correct)
        set_corr.setIcon(QtGui.QIcon(self.pathIconCorrect))

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        exit_.setIcon(QtGui.QIcon(self.pathIconExit))

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)
        self.show()
        self.app.exec_()

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            self.set_default()

    def set_default(self):
        self.Update_Icon(self.pathIconDefault)

    def set_correct(self):
        self.Update_Icon(self.pathIconCorrect)

    def set_error(self):
        self.Update_Icon(self.pathIconExit)

    def Update_Icon(self, path):
        self.setIcon(QtGui.QIcon(path))
