from ironspiders.utils import debugLogging, convert8
# virtual machine --
class vm:
    def __init__(self):
        """
        VM: this is main vm instance, it stores the registers, memory, etc.

        This virtual machine implementation is supposed to be easy and quick
        to develop programs, it runs totally on simulation, the memory is
        mostly of the time, very consistent, the registers & stack are
        stored out of such memory & program execution.
        """
        self.registers      = [0 for count in range(0,9+1)]
        self.stack          = []
        self.programCounter = 0
        self.program        = []
    
    def loadProgram(self, program):
        """loadProgram: set the program."""
        self.program = program
        self.programCounter = 0
    
    def tick(self):
        """tick: perform the instruction on the program counter."""
        pass