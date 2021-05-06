import os
import sys
import threading
from PySide2 import QtWidgets, QtGui


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    """
    CREATE A SYSTEM TRAY ICON CLASS AND ADD MENU
    """
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'Voice Assistant')
        menu = QtWidgets.QMenu(parent)

        set_def = menu.addAction("Set default")
        set_def.triggered.connect(self.set_default)
        set_def.setIcon(QtGui.QIcon("icon_default.png"))

        set_corr = menu.addAction("Set correct")
        set_corr.triggered.connect(self.set_correct)
        set_corr.setIcon(QtGui.QIcon("icon_correct.png"))

        set_err = menu.addAction("Set Error")
        set_err.triggered.connect(self.err_set)
        set_err.setIcon(QtGui.QIcon("icon_error.png"))

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        exit_.setIcon(QtGui.QIcon("icon.png"))

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            self.set_default()

    def set_default(self):
        self.Update_Icon("icon_default.png")

    def set_correct(self):
        self.Update_Icon("icon_correct.png")

    def set_error(self):
        self.Update_Icon("icon_error.png")

    def Update_Icon(self, path):
        self.setIcon(QtGui.QIcon(path))

#?????
    def err_set(self):
        self.set_error
        t = threading.Timer(5.0, self.set_default)
        t.start()

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    tray_icon = SystemTrayIcon(QtGui.QIcon("icon_default.png"), w)
    tray_icon.show()
    tray_icon.showMessage('VFX Pipeline', 'Hello "Name of logged in ID')
    sys.exit(app.exec_())
    print()


if __name__ == '__main__':
    main()
