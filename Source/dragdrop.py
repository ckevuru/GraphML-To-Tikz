from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QObject, pyqtSlot, QThread, pyqtSignal, QSize
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QDialog

class DragLineEdit(QtWidgets.QLineEdit):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        ''' Controlling the drag event.
        '''
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        ''' Controlling the drop event.
        '''
        for url in event.mimeData().urls():
            print(url.toLocalFile())
        self.setText(url.toLocalFile())