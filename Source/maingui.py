'''
This file handles the overall gui for the module.
'''

import os.path
import qdarkgraystyle

from model import Model
from shutil import copyfile
from codeeditor import CodeEditor
from genwidget import GeneralWidget

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSlot, QSize
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QDialog



class Ui_MainWindow(QObject):
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.count = 1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 700)
        MainWindow.setStyleSheet(qdarkgraystyle.load_stylesheet(
        ) + 'QPlainTextEdit {selection-background-color: white}')
        icon = QIcon()
        icon.addFile('../Images/python.png', QSize(256, 256))
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = GeneralWidget()
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionnewAction = QtWidgets.QAction(MainWindow)
        self.actionnewAction.setObjectName("actionnewAction")
        self.tabWidget.setTabsClosable(True)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBarDoubleClicked['int'].connect(self.addTab)
        self.tabWidget.tabCloseRequested['int'].connect(self.tab_close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GraphML-To-Tikz"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(
            self.tab), _translate("MainWindow", "Tab 1"))
        self.actionnewAction.setText(_translate("MainWindow", "newAction"))
        self.actionnewAction.setShortcut(_translate("MainWindow", "Ctrl+N"))

    def tab_close(self, i):
        '''Function to handle closing of tabs.
        '''
        if self.tabWidget.count() < 2:
            return
        self.count = self.count - 1
        self.tabWidget.removeTab(i)

    def addTab(self, qurl=None, label="Blank"):
        '''Function to handle addition of tabs.
        '''
        newtab = GeneralWidget()
        self.count = self.count + 1
        label = "Tab" + str(self.count)
        i = self.tabWidget.addTab(newtab, label)
        self.tabWidget.setCurrentIndex(i)

    def current_tab_changed(self, i):
        '''Function to handle current tab change.
        '''
        self.tab = self.tabWidget.widget(i)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
