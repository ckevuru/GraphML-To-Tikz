'''
This file handles the gui per tab. It is responsible for creating the gui within a tab and handling all the functionality.
'''

import os
import qdarkgraystyle

from model import Model
from shutil import copyfile
from dragdrop import DragLineEdit
from codeeditor import CodeEditor
from previewthread import PreviewThread

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.QtCore import QObject, pyqtSlot, QThread, pyqtSignal, QSize
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QDialog


class GeneralWidget(QWidget):
    def __init__(self, parent=None):
        
        super(QWidget, self).__init__(parent)

        self.model = Model()
        self.type = 'advance'
        self.prev = ''
        self.window = None
        
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName("gridLayout_4")
        
        self.widget = QtWidgets.QWidget(self.tab)
        self.widget.setObjectName("widget")
        
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_3.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        
        self.splitter = QtWidgets.QSplitter(self.widget)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        
        self.gridLayout = QtWidgets.QGridLayout(self.frame)
        self.gridLayout.setContentsMargins(0, 0, 0, 3)
        self.gridLayout.setObjectName("gridLayout")
        
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, -1, 4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.label = QtWidgets.QLabel(self.frame)
        
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        
        self.label.setFont(font)
        self.label.setStyleSheet(
            "font: 10pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        self.label.setObjectName("label")
        
        self.horizontalLayout.addWidget(self.label)
        
        self.lineEdit = DragLineEdit(self.frame)
        self.lineEdit.setObjectName("lineEdit")
        
        self.horizontalLayout.addWidget(self.lineEdit)
        
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.pushButton.setObjectName("pushButton")
        
        self.horizontalLayout.addWidget(self.pushButton)
        
        self.pushButton_5 = QtWidgets.QPushButton(self.frame)
        self.pushButton_5.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.pushButton_5.setObjectName("pushButton_5")
        
        self.horizontalLayout.addWidget(self.pushButton_5)
        
        self.verticalLayout.addLayout(self.horizontalLayout)
        
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        
        self.label_2 = QtWidgets.QLabel(self.frame)
        
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        
        self.horizontalLayout_3.addWidget(self.label_2)
        spacerItem = QtWidgets.QSpacerItem(
            188, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        
        self.horizontalLayout_3.addItem(spacerItem)
        
        self.label_3 = QtWidgets.QLabel(self.frame)
        
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        
        self.horizontalLayout_3.addWidget(self.label_3)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        
        self.plainTextEdit = CodeEditor(self.frame)
        self.plainTextEdit.setStyleSheet("font: 10pt \"Courier New\";")
        self.plainTextEdit.setObjectName("plainTextEdit")
        
        self.horizontalLayout_4.addWidget(self.plainTextEdit)
        
        self.plainTextEdit_2 = CodeEditor(self.frame)
        self.plainTextEdit_2.setStyleSheet("font: 10pt \"Courier New\";")
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        
        self.horizontalLayout_4.addWidget(self.plainTextEdit_2)
        
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setObjectName("label_4")
        
        self.horizontalLayout_2.addWidget(self.label_4)
        spacerItem2 = QtWidgets.QSpacerItem(
            173, 22, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        
        self.pushButton_3 = QtWidgets.QPushButton(self.frame)
        self.pushButton_3.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.pushButton_3.setObjectName("pushButton_3")
        
        self.horizontalLayout_2.addWidget(self.pushButton_3)
        
        self.pushButton_4 = QtWidgets.QPushButton(self.frame)
        self.pushButton_4.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.pushButton_4.setObjectName("pushButton_4")
        
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.pushButton_2.setObjectName("pushButton_2")
        
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        
        self.plainTextEdit_3 = CodeEditor(self.splitter)
        
        self.splitter.setSizes([300, 100])
        
        self.plainTextEdit_3.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.plainTextEdit_3.setObjectName("plainTextEdit_3")
        
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        
        self.gridLayout_4.addWidget(self.widget, 0, 0, 1, 1)
        
        self.plainTextEdit.setAcceptDrops(False)
        self.plainTextEdit_3.setAcceptDrops(False)
        
        self.preview_thread = PreviewThread()
        self.preview_thread.signal.connect(self.loadPreview)
        
        self.label.setText("File Name : ")
        
        self.label_2.setText("Tikz : ")
        
        self.label_3.setText("GraphML : ")
        
        self.label_4.setText("Debug Logs : ")
        
        self.label_2.setStyleSheet(
            "font: 10pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        
        self.label_3.setStyleSheet(
            "font: 10pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        
        self.label_4.setStyleSheet(
            "font: 10pt \"MS Shell Dlg 2\";color: rgb(255, 255, 255);")
        
        self.pushButton.setText("Browse")
        
        self.pushButton_3.setText("Simple-Tikz")
        
        self.pushButton_2.setText("Save")
        
        self.pushButton_4.setText("Refresh")
        
        self.pushButton_5.setIcon(QtGui.QIcon('../Images/refresh.png'))
        
        self.pushButton.clicked.connect(self.browseSlot)
        
        self.lineEdit.returnPressed.connect(self.returnedPressedSlot)
        
        self.pushButton_3.clicked.connect(self.convertSlot)
        
        self.pushButton_4.clicked.connect(self.reloadSlot)
        
        self.pushButton_2.clicked.connect(self.saveSlot)
        
        #self.lineEdit.textChanged.connect(self.draganddrop)
        
        self.pushButton_5.clicked.connect(self.refreshSlot)
        
        self.setLayout(self.gridLayout_4)

    def debugPrint(self, msg):
        '''Print the message in the text edit at the bottom of the
        horizontal splitter.
        '''
        if self.prev != msg:
            self.prev = msg
            self.plainTextEdit_3.appendPlainText(str(msg))

    @pyqtSlot()
    def returnedPressedSlot(self):
        ''' Called when the user enters a string in the line edit and
        presses the ENTER key.
        '''
        fileName = self.lineEdit.text()
        extension = os.path.splitext(fileName)[1]
        self.debugPrint("Converting file : " + fileName)
        if self.model.isValid(fileName) and extension == '.graphml':
            self.model.setFileName(self.lineEdit.text())
            if self.type == 'simple':
                self.refreshAll()
            elif self.type == 'advance':
                self.refreshAllSimple()
        else:
            m = QtWidgets.QMessageBox()
            m.setText("File not supported or invalid path!\n" + fileName)
            m.setIcon(QtWidgets.QMessageBox.Warning)
            m.setStandardButtons(QtWidgets.QMessageBox.Ok
                                 | QtWidgets.QMessageBox.Cancel)
            m.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            m.exec_()
            self.lineEdit.setText("")
            self.plainTextEdit.setPlainText("")
            self.plainTextEdit_2.setPlainText("")
            self.debugPrint("Invalid file specified: " + fileName)

    @pyqtSlot()
    def convertSlot(self):
        ''' Called when the user presses the convert button.
        '''

        if self.model.getFileName():
            if self.type == 'simple':
                self.refreshAll()
                _translate = QtCore.QCoreApplication.translate
                self.pushButton_3.setText(
                    _translate("MainWindow", "Simple Tikz"))
                self.type = 'advance'
                self.debugPrint(
                    "Advanced mode chosen.Output modified.")
            elif self.type == 'advance':
                self.refreshAllSimple()
                _translate = QtCore.QCoreApplication.translate
                self.pushButton_3.setText(
                    _translate("MainWindow", "Adv-Tikz"))
                self.debugPrint(
                    "Simple mode chosen.Output modified.")
                self.type = 'simple'
        else:
            self.debugPrint("No file specified.")

    @pyqtSlot()
    def browseSlot(self):
        ''' Called when the user presses the Browse button
        '''
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Select GraphMl Files",
            "",
            filter="*.graphml",
            options=options)
        if fileName:
            self.debugPrint("Converting file : " + fileName)
            self.model.setFileName(fileName)
            try:
                self.window.close()
            except:
                pass
            if self.type == 'advance' : 
                self.refreshAll()
            else:
                self.refreshAllSimple()

    @pyqtSlot()
    def saveSlot(self):
        ''' Called when the user presses the Save button
        '''
        if self.model.getFileName():
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
                None, "QFileDialog.getSaveFileName()", "", ".tex", options=options)
            if fileName:
                content = self.plainTextEdit.toPlainText()
                with open(fileName+'.tex', 'w') as out:
                    out.write(content)
                self.debugPrint("File " + fileName + '.tex saved.')
        else:
            self.debugPrint("No file specified to save.")

    @pyqtSlot()
    def reloadSlot(self):
        ''' Called when the user presses the Refresh button.
        '''
        self.debugPrint('Refreshing preview....')
        if self.plainTextEdit.toPlainText() != '':
            fileName = self.model.getFileName()
            flin = os.path.splitext(fileName)[0]
            fileName = self.model.getFileName()
            flin = os.path.splitext(fileName)[0]
            fileout = flin + '.tex'
            tout = open(fileout, 'w')
            tout.write(
                '\\documentclass[11pt]{article}\n\\usepackage{tikz}\n\\thispagestyle{empty}\n\\usetikzlibrary{arrows,shapes}\n\\begin{document}\n')
            tout.write(self.plainTextEdit.toPlainText())
            tout.write('\\end{document}')
            tout.close()
            self.preview(flin)

    @pyqtSlot()
    def refreshSlot(self):
        ''' Called when the user presses the Reload symbol.
        '''
        self.debugPrint('Reloaded file.')
        self.returnedPressedSlot()

    @pyqtSlot()
    def draganddrop(self):
        ''' Called when the user drags and drops file on the line edit.
        '''
        if self.lineEdit.text() != '':
            try:
                self.window.close()
            except:
                pass
            self.returnedPressedSlot()

    def loadPreview(self, flag):
        ''' This function loads the preview in a different window.
        '''
        self.preview_thread.stop()
        fileName = self.model.getFileName()
        flin = os.path.splitext(fileName)[0]
        _, tail = os.path.split(flin)
        if flag:
            cwd = os.getcwd()
            img_path = cwd + '\\' + tail + '.jpg'
            img = QImage(img_path)
            self.window = PreviewWindow(cwd + '\\' + tail)
            pixmap = QPixmap(img_path)
            self.window.setPicSize(img.width(), img.height())
            self.window.label.setPixmap(pixmap.scaled(
                self.window.label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            icon = QIcon()
            icon.addFile('../Images/python.png', QSize(256, 256))
            self.window.setWindowIcon(icon)
            self.window.show()
            self.debugPrint("Preview loaded.")
            try:
                os.remove(flin+'.tex')
                os.remove(tail+'.log')
                os.remove(tail + '.aux')
                os.remove(tail + '.pdf')
                os.remove(tail+'-crop.pdf')
            except:
                pass
        else:
            try:
                self.window.close()
                os.remove(flin+'.tex')
                os.remove(tail+'.log')
                os.remove(tail + '.aux')
                os.remove(tail + '.pdf')
                os.remove(tail+'-crop.pdf')
            except:
                pass
            self.debugPrint("Preview failed due to latex compilation error.")

    def refreshAllSimple(self):
        '''
        Updates the widgets whenever an interaction happens.
        Typically some interaction takes place, the UI responds,
        and informs the model of the change.  Then this method
        is called, pulling from the model information that is
        updated in the GUI.
        '''
        self.debugPrint('Hereasdasdasdasdasdsassimp')
        self.lineEdit.setText(self.model.getFileName())
        flag, exception, contents = self.model.convertSlot()
        if flag == True:
            self.debugPrint(exception + ' in ' + str(self.model.getFileName()))
            self.debugPrint('Conversion for file : ' + str(self.model.getFileName()) + ' failed.')
            self.plainTextEdit.setPlainText('')
            self.plainTextEdit_2.setPlainText('')
        else:
            fileName = self.model.getFileName()
            flin = os.path.splitext(fileName)[0]
            fileout = flin + '.tex'
            tout = open(fileout, 'w')
            tout.write(
                '\\documentclass[11pt]{article}\n\\usepackage{tikz}\n\\thispagestyle{empty}\n\\usetikzlibrary{arrows,shapes}\n\\begin{document}\n')
            tout.write(contents)
            tout.write('\\end{document}')
            tout.close()
            self.plainTextEdit.setPlainText(contents)
            self.plainTextEdit_2.setPlainText(self.model.getGraphML())
            self.debugPrint('Conversion for file : ' + str(self.model.getFileName()) + ' successful.')
            self.debugPrint('Loading Preview....')
            self.preview(flin)

    def refreshAll(self):
        '''
        Updates the widgets for simple mode.
        '''
        self.debugPrint('Hereasdasdasdasdasdsas')
        self.lineEdit.setText(self.model.getFileName())
        flag, exception, contents = self.model.getFileContents()
        if flag == True:
            self.debugPrint(exception + ' in ' + str(self.model.getFileName()))
            self.debugPrint('Conversion for file : ' + str(self.model.getFileName()) + ' failed.')
            self.plainTextEdit.setPlainText('')
            self.plainTextEdit_2.setPlainText('')
        else:
            fileName = self.model.getFileName()
            flin = os.path.splitext(fileName)[0]
            fileout = flin + '.tex'
            tout = open(fileout, 'w')
            tout.write(
                '\\documentclass[11pt]{article}\n\\usepackage{tikz}\n\\thispagestyle{empty}\n\\usetikzlibrary{arrows,shapes}\n\\begin{document}\n')
            tout.write(contents)
            tout.write('\\end{document}')
            tout.close()
            self.plainTextEdit.setPlainText(contents)
            self.plainTextEdit_2.setPlainText(self.model.getGraphML())
            self.debugPrint('Conversion for file : ' + str(self.model.getFileName()) + ' successful.')
            self.debugPrint('Loading Preview....')
            self.preview(flin)

    def preview(self, flin):
        ''' This function is called before previewing which initialises threads.
        '''
        self.preview_thread.set_file(flin)
        self.preview_thread.start()

class PreviewWindow(QWidget):

    def __init__(self, flin):
        super().__init__()
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 1250
        self.top = 400
        self.width = 0
        self.height = 0
        self.input = flin
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon('../Images/python.png'))
        self.label = QLabel(self)
        self.label.setScaledContents(True)
        closeWindow = QAction("Quit", self)
        closeWindow.triggered.connect(self.closeEvent)

    def setPicSize(self, w, h):
        ''' Set the pic size for the preview.
        '''
        self.width = w
        self.height = h
        self.setWindowTitle(self.input + '.jpg')
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.label.resize(self.width, self.height)

    def resizeEvent(self, event):
        ''' Function handling the resize of the preview event.
        '''
        pixmap1 = QtGui.QPixmap(self.input + ".jpg")
        pixmap = pixmap1.scaled(
            self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)
        self.label.resize(self.size())

    def closeEvent(self, event):
        try:
            os.remove(self.input+'.jpg')
        except:
            pass