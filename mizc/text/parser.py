class parserSyntaxError(Exception):
    def __init__(self, line, index, message):
        """parserSyntaxError: case the parser has reported a error."""
        self.message    = message + ", char: %d" % index
        self.atPos      = [line, index]
        super().__init__(self.message)

def parser(text):
    """parser: return your text string parsed with all the tokens marked."""
    tIndex, tLen    = 0, len(text)
    inStr, inStrCh  = False, None
    openedString    = 0
    tAcc, tokens    = "", []

    def __incString(token, string):
        if len(string) > 0:
            token.append(string)

    _ST = ('"',"'")
    _TK = (",")

    while tIndex < tLen:
        char = text[tIndex]
        if char == ' ' and not inStr:
            __incString(tokens, tAcc)   ;   tAcc = ""
            tAcc, tIndex = "", (tIndex + 1)
        elif char in _ST and not inStr:
            __incString(tokens, tAcc)
            tAcc, inStr, inStrCh = char, True, char
            tIndex, openedString = (tIndex + 1), tIndex
        elif char in _ST and inStr and char == inStrCh:
            __incString(tokens, tAcc+char)
            tAcc, inStr, inStrCh = "", False, None
            tIndex, openedString = (tIndex + 1), 0
        elif char in _TK and not inStr:
            __incString(tokens, tAcc)
            __incString(tokens, char)
            tAcc, tIndex = "", (tIndex + 1)
        else:
            tAcc, tIndex = tAcc + char, tIndex + 1
    
    # string not closed.
    if inStr: raise parserSyntaxError(0, openedString, "string not closed!")
    __incString(tokens, tAcc)
    return tokens