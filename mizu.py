import mizc
import sys

DEBUG_THIS_FILE = True

class mizuApp:
    def __init__(self):
        self.fileTarget     = None # -> file to open
        self.fileVM         = None # -> the virtual machine to run the program
        self.fileBinary     = None # -> the binary stuff to execute the machine.
    
    def die(self, exception, code=-1):
        """die: only used when exception!"""
        exit(print("[fatal] %s" % str(exception)) or code)

    def openFile(self, fileName):
        self.fileTarget = fileName
        fileN, lines = open(fileName, 'r'), []
        for fileLine in fileN:
            lines.append(
                mizc.parser(
                    fileLine.replace('\t', ' ').replace('\n','')
                )
            )
        fileN.close()
        # lexer state & binary generation!
        if DEBUG_THIS_FILE:
            binaryGen = mizc.lexer(lines)
        else:
            try:    binaryGen = mizc.lexer(lines)
            except Exception as E: self.die(E)
        mizc.showMemoryHexView(binaryGen)

if __name__ == '__main__':
    mA = mizuApp()
    mA.openFile(sys.argv[1])