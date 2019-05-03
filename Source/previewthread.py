import os
import subprocess

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread

from pdf2image import convert_from_path

class PreviewThread(QThread):
    signal = QtCore.pyqtSignal(bool)

    def __init__(self):
        QThread.__init__(self)

    def set_file(self, file):
        self.input = file

    def run(self):
        _, tail = os.path.split(self.input)
        ret = subprocess.call([
            'pdflatex', '-halt-on-error', '-interaction=nonstopmode',
            self.input + '.tex'])
        subprocess.call(['pdfcrop',tail + '.pdf'], shell=False)
        flag = True
        if ret == 0:
            pages = convert_from_path(tail + '-crop.pdf')
            pages[0].save(tail + '.jpg', 'JPEG')
            flag = True
        else:
            flag = False
        self.signal.emit(flag)

    def stop(self):
        self.terminate()