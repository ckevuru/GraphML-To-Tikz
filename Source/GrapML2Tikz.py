'''
Main file to start the module. This file is the first part of the module.
'''


from PyQt5 import QtWidgets
from maingui import Ui_MainWindow
from shutil import copyfile
import sys
from model import Model


class MainWindowUIClass(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.model = Model()

    def setupUi(self, MW):
        super().setupUi(MW)

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
