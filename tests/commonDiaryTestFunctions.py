import sys, io

def isFileContentIdentical(pathA,pathB):
    """
        Do a line by line comparison of the content of two files. Return true
        if they are equal
    """
    # read the two files to two lists
    fileLineListA = createFileLineList(pathA)
    fileLineListB = createFileLineList(pathB)
    nLinesA = len(fileLineListA)
    nLinesB = len(fileLineListB)
    if nLinesA!=nLinesB:
        return False
    # do a line by line comparison
    for iLine in range(nLinesA):
        if fileLineListA[iLine] != fileLineListB[iLine]:
            return False
    # if the function has not returned False at this point, the two files are 
    # the same
    return True
    
def createFileLineList(path):
    """
        Create a list from a file where each line is an element in the list.
    """
    fileLineList = list()
    fileHandle = io.open(path,'r',encoding='utf-8')
    for line in fileHandle:
        if sys.version_info[0] < 2:
            fileLineList.append(line.decode('utf-8'))
        else:
            fileLineList.append(line)
    fileHandle.close()
    return fileLineList
