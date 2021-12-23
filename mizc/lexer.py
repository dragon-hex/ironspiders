from .opcode import *
from .utility import *

DEBUG_THIS_FILE = True
from .debug import debugLogging
import sys

class invalidOpcodeError(Exception):
    def __init__(self, line, char, message):
        self.message = "invalid opcode: %s, line: %d, char: %d" % (
            message, line, char
        )
        super().__init__(self.message)

class invalidSyntax(Exception):
    def __init__(self, line, char, message):
        self.message = "invalid syntax: %s, line: %d, char: %d" % (
            message, line, char
        )
        super().__init__(self.message)

def convertToData(string):
    """
        convertToData: return the data as it is supposed to be referenced on the memory.
        <data>: FLAGS (0x00, 0x00) [0x0: type of data, 0x0: size of data] | data.
    """

    dataSequence = []
    _ST = ('"', "'")
    _RT = {
        'pc': 40,  # -> program counter
        'sp': 42,  # -> stack position
        'r0': 10, 'r1': 11, 'r2': 12, 'r3': 13, 'r4': 14, 'r5': 15,     # -> general proporse registers
        'r0': 16, 'r1': 17, 'r2': 18, 'r3': 19, 'r9': 20,               # -> general proporse registers
    }

    if string[0] in _ST:
        stringLength    = len(string) - 2
        string          = string[1:len(string)-1]
        # NOTE the strings has 16 bit size! So, it comes in pair with the High Byte, Mid Byte and Low Byte!
        # this allows for more interactions of characters, such as hiragana.
        data = [DATA_TYPE_STRING] + split8(stringLength, length=4)
        for char in string:
            charSet = split8(ord(char),length=3)
            data.append(charSet[0])
            data.append(charSet[1])
            data.append(charSet[2])
        return data

    # TODO: implement DECIMAL numbers!
    elif string[0] == '$': 
        numberLength = 4
        stackValue = int(string[1:len(string)])
        return [DATA_TYPE_STACK_POINTER, numberLength] + split8(stackValue,length=numberLength)
    elif string in _RT.keys():
        return [DATA_TYPE_REGISTER, _RT.get(string)]
    else:
        # TODO: optimize the number pool!
        numberLength = 4
        return [DATA_TYPE_NUMBER, numberLength] + split8(int(string),length=numberLength)


def lexer(lines):
    """lexer: get all the tokens and convert to bytecode."""
    __l = debugLogging(DEBUG_THIS_FILE, 'lexer')
    if DEBUG_THIS_FILE: __l.debugOutputNew(sys.stdout)

    # NOTE the bytecode doesn't need of any ',', so remove
    # it here, this only serves to decorate.
    for line in lines:
        while ',' in line:
            line.remove(',')

    lineIndex, lineLength = 0, len(lines)
    binaryGen, address = [], {}
    while lineIndex < lineLength:
        line = lines[lineIndex]
        tokenIndex, lineSize = 0, len(line)
        while tokenIndex < lineSize:
            token = line[tokenIndex]
            if token[len(token)-1] == ':':
                # NOTE find the token to label definition.
                # TODO remove this NOP instruction to save
                # memory on the future! the NOP instruction,
                # althrough don't use any VM time, it still
                # costing 1 byte to use it anyway.
                possibleTokenName = token[0:len(token)-1]
                possibleAddress = len(binaryGen)
                
                __l.report("new possible label found: %s, address: %d" % (possibleTokenName, possibleAddress))

                address[possibleTokenName] = possibleAddress
                binaryGen.append(OPCODE_NOPE[0])
                tokenIndex += 1
            else:
                # the code needs to detect if we are on the instruction or not.
                OPCODE_TABLE_DATA = OPCODE_TABLE.get(token.lower())
                if OPCODE_TABLE_DATA:
                    # assert that the opcode is complete, that means the opcode
                    # has the necessary number of arguments to be setup!
                    numberArguments = OPCODE_TABLE_DATA[1]
                    if tokenIndex + (numberArguments + 1) > lineSize:
                        raise invalidSyntax(lineIndex+1, tokenIndex, "'%s' requires %d argument(s)!" % (token.lower(), numberArguments))
                    
                    arguments = line[tokenIndex+1:tokenIndex+OPCODE_TABLE_DATA[1]+1]
                    __l.report("found possible keyword for opcode: %s" % (token))
                
                    # translate to binary instructions!
                    opcodeNumber = OPCODE_TABLE_DATA[0]
                    for argument in arguments:
                        aData = convertToData(argument)
                        __l.report(aData)
                        binaryGen += aData

                    # get all the possible arguments for the opcodes
                    tokenIndex += (1 + OPCODE_TABLE_DATA[1])
                else:
                    __l.report("invalid opcode: %s" % token)
                    raise invalidOpcodeError(lineIndex+1, tokenIndex, token)
        lineIndex += 1
    return binaryGen