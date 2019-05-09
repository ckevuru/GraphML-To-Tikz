import os
import pdf2image
import qdarkgraystyle

from shutil import copyfile

from PyQt5.Qt import PYQT_VERSION_STR

if __name__ == "__main__":
    print("PyQt version : ", PYQT_VERSION_STR)
    print("QDarkGrayStyle version : ",qdarkgraystyle.__version__)
    print("Pdf2Image verification : ",pdf2image.__package__)