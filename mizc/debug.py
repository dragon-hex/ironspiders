class debugLogging:
    def __init__(self, enabled, debugFrom):
        self.enabled = enabled
        self.debugFrom = debugFrom
        self.__debugOutputs = []
        self.__debugMessageIndexer = 0
    
    def __safeInvoke(self, function, args, returnException=False):
        try:
            return function(args)
        except Exception as E:
            return E if returnException else -1

    def report(self, string):
        """report: write your debug!"""
        if len(self.__debugOutputs) <= 0:
            return
        else:
            for debugOutput in self.__debugOutputs:
                self.__safeInvoke(
                    debugOutput.write, 
                    "[debug: %s - %0.8d]: %s\n" % (self.debugFrom, self.__debugMessageIndexer, string)
                )
            self.__debugMessageIndexer += 1
    
    def debugOutputNew(self, newDebugOutput):
        self.__debugOutputs.append(newDebugOutput)
        self.report("new debug was inserted: %s" % newDebugOutput.name)

# functions here!

def showMemoryHexView(buffer, mark=-1):
    """
    showMemoryHexView: show the memory in a column.
    if you want to show a specific byte, use mark keyword.
    """
    print() # -> give a space between the debugs!
    print(" " * 0x10 + "Memory View: 0x0 -> %d" % len(buffer))
    memoryIndex, memorySize = 0, len(buffer)
    columnIndex = 0xF+1
    print(" " * 0x10, end='')
    for count in range(0,0xf+1):
        print("%0.2x   " % count, end='')
    print()
    while memoryIndex < memorySize:
        if columnIndex >= 0xF+1:
            print("\n%0.14x" % memoryIndex, end='')
            columnIndex = 0
        if mark == memoryIndex:
            print(" [%0.2x]" % buffer[memoryIndex],end='')
        else:
            print("  %0.2x " % buffer[memoryIndex],end='')
        columnIndex, memoryIndex = columnIndex + 1, memoryIndex + 1
    print()