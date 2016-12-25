from PyQt5.QtCore import pyqtSignal, QObject

__author__ = 'Bartosz Kościow'


class StateChange(QObject):
    state = pyqtSignal(str)


class ExitApplication(QObject):
    close = pyqtSignal()