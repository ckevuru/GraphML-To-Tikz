'''
This file acts as a connection between the frontend and the backend.
'''

from classparse import ParseTikz

class Model:
    def __init__(self):
        '''
        Initializes the thrre members the class holds:
        the file name, its contents and an object of class ParseTikz.
        '''
        self.fileName = None
        self.parse = ParseTikz()
        self.fileContent = ""

    def isValid(self, fileName):
        '''
        returns True if the file exists and can be
        opened.  Returns False otherwise.
        '''
        try:
            file = open(fileName, 'r')
            file.close()
            return True
        except:
            return False

    def setFileName(self, fileName):
        '''
        sets the member fileName to the value of the argument
        if the file exists.  Otherwise resets both the filename
        and file contents members.
        '''
        if self.isValid(fileName):
            self.fileName = fileName
            self.fileContents = open(fileName, 'r').read()
        else:
            self.fileContents = ""
            self.fileName = ""

    def getFileName(self):
        '''
        Returns the name of the file name member.
        '''
        return self.fileName

    def getGraphML(self):
        '''
        Returns the contents of the file if it exists, otherwise
        returns an empty string.
        '''
        return self.fileContents

    def getFileContents(self):
        '''
        Returns the contents of the file if it exists, otherwise
        returns an empty string.
        '''
        flag, exception, contents = self.parse.getTikzFile(
            self.fileName, 'advanced')
        return flag, exception, contents

    def convertSlot(self):
        '''
        Writes the string that is passed as argument to a
        a text file with name equal to the name of the file
        that was read, plus the suffix ".graphml"
        '''
        return self.parse.getTikzFile(self.fileName, 'simple')
