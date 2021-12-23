OPCODE_NOPE     = [1, 0]        # NOPE
OPCODE_MOVE     = [2, 2]        # MOVE <source> -> <dest>
OPCODE_INEW     = [3, 1]        # INEW <value>
OPCODE_SNEW     = [4, 1]        # SNEW <value>
OPCODE_DNEW     = [5, 1]        # DNEW <value>
OPCODE_SYSC     = [6, 1]        # SYSC <code>

# opcode table
OPCODE_TABLE    = {
    'nope'  : OPCODE_NOPE,
    'move'  : OPCODE_MOVE,
    'inew'  : OPCODE_INEW,
    'snew'  : OPCODE_SNEW,
    'dnew'  : OPCODE_DNEW,
    'sysc'  : OPCODE_SYSC
}

# DATA flags
DATA_TYPE_NUMBER    = 1
DATA_TYPE_STRING    = 2
DATA_TYPE_DECIMAL   = 3
DATA_TYPE_POINTER   = 4
DATA_TYPE_REGISTER  = 5
DATA_TYPE_STACK_POINTER = 6