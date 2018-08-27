import sys, os

def unicodeDir(path):
    """
        Returns the directory name as a unicoded string from a file at path.
    """
    if sys.version_info[0] < 3:
        # The Python version is smaller than 3
        fileEncoding = sys.getfilesystemencoding()
        absolutePath = os.path.dirname(unicode(path, fileEncoding))
    else:
        # The Python version is greater than or equal to 3
        absolutePath = os.path.dirname(path)
    return absolutePath
    
def getUserInput():
    """
        Get keyboard input from the user.
    """
    if sys.version_info[0] < 3:
        # The Python version is smaller than 3
        terminalEncoding = sys.stdin.encoding
        userInput = raw_input().decode(encoding=terminalEncoding,\
            errors='strict')
    else:
        # The Python version is greater than or equal to 3
        userInput = input()
    return userInput

def unicodeStr(inputObject):
    """
        Converts an input to a unicoded string.
    """
    if sys.version_info[0] < 3:
        # The Python version is smaller than 3
        return unicode(str(inputObject),'utf-8')
    else:
        # The Python version is greater than or equal to 3
        return str(inputObject)
        
def convertTerminalInputs2Unicode(rawInputList):
    """
        Convert a list/tuple to a list of unicoded strings.
    """
    if sys.version_info[0] < 3:
        # The Python version is smaller than 3
        fileEncoding = sys.getfilesystemencoding()
        unicodedInputList = list()
        for rawInput in rawInputList:
            unicodedInputList.append(\
                rawInput.decode(encoding=fileEncoding,\
                errors='strict'))
        return unicodedInputList
    else:
        # The Python version is greater than or equal to 3
        return list(rawInputList)
