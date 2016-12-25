from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon, QAction
import sys

__author__ = 'Bartosz Kościów'


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, state, communication, parent=None):
        QSystemTrayIcon.__init__(self, parent)
        self.icons = {
            'unknown': QtGui.QIcon('img/unknown.png'),
            'detect.light': QtGui.QIcon('img/busy.png'),
            'detect.dark': QtGui.QIcon('img/empty.png')
        }
        self.communication = communication
        self.state_change(state)
        self.create_menu(parent)
        self.communication['state'].state.connect(self.state_change)

    def create_menu(self, parent):
        menu = QMenu(parent)
        exit_action = menu.addAction("Exit")
        exit_action.triggered.connect(self.exit)
        self.setContextMenu(menu)

    def exit(self):
        self.communication['close'].close.emit()
        QtCore.QCoreApplication.exit()

    def state_change(self, event):
        if event in self.icons:
            self.setIcon(self.icons[event])
        else:
            self.setIcon(self.icons['unknown'])


def run_gui(state, communication):
    app = QApplication([])
    trayIcon = SystemTrayIcon(state, communication)
    trayIcon.show()
    sys.exit(app.exec_())