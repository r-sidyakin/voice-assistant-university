import sys

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

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            self.set_default()

    def set_default(self):
        self.update_Icon(self.pathIconDefault)

    def set_correct(self):
        self.update_Icon(self.pathIconCorrect)

    def set_error(self):
        self.update_Icon(self.pathIconExit)

    def update_Icon(self, path):
        self.setIcon(QtGui.QIcon(path))
