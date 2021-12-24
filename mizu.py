import mizc
import sys
import os

# debug the file.
DEBUG_THIS_FILE = True

class mizuApp:
    def __init__(self):
        """
        mizuApp: this is a quick wrapper.
        """
        self.fileTarget     	= None # -> file to open
        self.fileVM         	= None # -> the virtual machine to run the program
        self.fileBinary     	= None # -> the binary stuff to execute the machine.
        self.fileOutput	   	    = None # -> the file to write the binary code.
        self.showBinary   	    = False# -> show the binary.
        self.enableDebug        = False# -> show the debug.
    
    def run(self, args):
        """
        run: run the mizuApp.
        """
        argIndex, argsCountered = 1, len(args)
        if argsCountered < 2: self.die("nothing to do.")
        fileLoaded=None
        _OA=("-output","--output","-o")
        _SB=("-show-binary","--show-binary","-sbin")
        _DE=("-debug","--debug","-d")
        while argIndex < argsCountered:
            arg = args[argIndex]
            if os.path.exists(arg) and not fileLoaded:
                fileLoaded=os.path.abspath(arg)
            elif arg in _SB:
                # show the binary
                self.showBinary = True
            elif arg in _OA:
                # find the output file!
                if argIndex+1 >= argsCountered:
                    self.die("%s needs <file>."%arg)
                self.fileOutput=args[argIndex+1]
                argIndex+=1
            elif arg in _DE:
                # enable the debug on the program!
                self.enableDebug = True
            else:
                self.die("invalid argument '%s'."%arg)
            argIndex+=1
        # open the file!
        self.openFile(fileLoaded)
        if self.fileOutput: self.generateBinary()
    
    def die(self, exception, code=-1):
        """die: only used when exception!"""
        exit(print("[fatal] %s" % str(exception)) or code)

    def generateBinary(self):
        """generateBinary: generate the binary."""
        self.fileOutput=open(self.fileOutput,'wb')
        self.fileOutput.write(bytearray(self.fileBinary))
        self.fileOutput.close()

    def openFile(self, fileName):
        """
        openFile: load the file here.
        """
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
            binaryGen = mizc.lexer(lines,debug=self.enableDebug)
        else:
            try:    binaryGen = mizc.lexer(lines)
            except Exception as E: self.die(E)
        if self.showBinary: mizc.showMemoryHexView(binaryGen)
        self.fileBinary = binaryGen

if __name__ == '__main__':
    mA = mizuApp()
    mA.run(sys.argv)