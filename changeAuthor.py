#!/usr/bin/python
import sys, re, os, shutil, io
sys.path.append('database/')
sys.path.append('../logic')
import newAuthor, DiaryDatabaseWrapper, newBuild, commonDiaryFunctions

# Change an author in the database.
def updateAuthor(argv):
    """
        Change an author in the database.
    """
    if len(argv) < 2:
        print('At least two input parameters must be specified.')
        print('changeAuthor.py oldInitials newInitials \"New name\" \"New email\"')
        return
    # check if the old and/or new author are in the database
    oldAuthorInitials, oldAuthorName, oldAuthorEmail = \
        retrieveAuthorInfo(argv[0])
    if oldAuthorInitials == '':
        print('The old author with initials %s is not in the database.' % argv[0])
        return
    newAuthorInitials, newAuthorName, newAuthorEmail = \
        retrieveAuthorInfo(argv[1])
    authorMustBeReplaced = newAuthorInitials != ''
    if authorMustBeReplaced:
        print('The new author with initials %s is already in the database.'\
            % argv[1])
        sys.stdout.write("Do you want to replace this author (y/N)? ")
        choice = commonDiaryFunctions.getUserInput().lower()
        if choice in ('','n','no'):
            print('No author was changed.')
            return
        
    # if only two input parameters are set, set the new author info to
    # the old one
    if len(argv) == 2:
        argv.extend((oldAuthorName, oldAuthorEmail))
    elif len(argv) == 3:
        argv.append(oldAuthorEmail)
    newAuthorInitials, newAuthorName, newAuthorEmail = \
        newAuthor.validateInputs(argv[1:])
    # update the authors in the diary tasks
    if oldAuthorInitials != newAuthorInitials:
        updateDiaryTasks(oldAuthorInitials,newAuthorInitials)
    # update the database
    updateAuthorDatabase(oldAuthorInitials,newAuthorInitials,newAuthorName,\
        newAuthorEmail,authorMustBeReplaced)
    print("The author database and the diary entries have been " \
        "successfully updated.")
    
# check if an author is in the database and retrieve info if true
def retrieveAuthorInfo(authorInitials):
    """
        check that the old author is in the database
    """
    db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
    authorRows = db.selectFromTable('authors',('initials','name','email'),\
        'WHERE initials=\'' + authorInitials + '\'')
    db.close()
    if len(authorRows)!=1:
        return '','',''
    else:
        return authorRows[0][0], authorRows[0][1], authorRows[0][2]
    
# update the author database
def updateAuthorDatabase(oldAuthorInitials,newAuthorInitials,newAuthorName,\
        newAuthorEmail,authorMustBeReplaced):
    """
        Update the author database.
    """
    # Create a diary database object.
    db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
    # First delete an author if needed
    if authorMustBeReplaced:
        db.deleteInTable('authors','initials=\'' + newAuthorInitials + '\'')
    # update the database
    db.updateTable('authors',('initials','name','email'),\
        (newAuthorInitials,newAuthorName,\
        newAuthorEmail),'initials=\'' + \
        oldAuthorInitials + '\'')
    db.close()
    
# update the author initials in the diary entries
def updateDiaryTasks(oldAuthorInitials,newAuthorInitials):
    """
        Update the author initials in the diary entries
    """
    dateList = newBuild.getAllDatesWithEntries()
    diaryDir = commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))
    tmpTaskFilePath = diaryDir + '/buildFiles/tmpTask.tex'
    authorStringPattern = re.compile(r'^\s*\\authors\{(([a-zA-Z0-9\s]*,)*)' + \
        oldAuthorInitials + '(([a-zA-Z0-9\s]*,)*)([a-zA-Z0-9\s]*)\}\s*$')
    for date in dateList:
        relativeDateDir = 'entries/' + str(date.year) + '/' + \
            str(date.month).zfill(2) + '/' + str(date.day).zfill(2)
        # The file name of a task must match the pattern YYYYMMDD_XXXI.tex
        # where XXX are optional initials (letters a-zA-Z) and I is a number.
        fileNamePattern = re.compile(r'^' + str(date.year) + \
            str(date.month).zfill(2) + str(date.day).zfill(2) + \
            '_([a-zA-Z]*)([0-9]+)\.tex$')
        # Retrieve a sorted list of all files and folders in relativeDateDir
        filesAndFoldersList = \
            sorted(os.listdir(diaryDir + '/' + relativeDateDir))
        validTaskPathList = list()
        for fileOrFolder in filesAndFoldersList:
            relativeTaskPath = relativeDateDir + '/' + fileOrFolder
            taskPath = diaryDir + '/' + relativeTaskPath
            if os.path.isfile(taskPath) and \
                    re.match(fileNamePattern, fileOrFolder):
                oldTaskFile = io.open(taskPath,'r',encoding='utf-8')
                tmpTaskFile = io.open(tmpTaskFilePath,'w',encoding='utf-8')
                authorIsUpdated = False
                # search for the old author initials
                for line in oldTaskFile:
                    # to avoid scanning all lines in the file, a flag is set 
                    # when the author initials have been updated
                    if not authorIsUpdated and re.match(authorStringPattern,line):
                        authorPattern = \
                            re.compile(r'^\s*\\authors\{(!*[a-zA-Z0-9,\s]+)\}\s*$')
                        authorList = \
                            re.search(authorPattern,line).group(1).split(',')
                        updatedAuthorList = list()
                        for author in authorList:
                            # remove white space
                            author = author.strip()
                            # update the old author initials with the new.
                            # Remove any duplicates.
                            if author == oldAuthorInitials:
                                updatedAuthorList.append(newAuthorInitials)
                            elif author != newAuthorInitials:
                                updatedAuthorList.append(author)
                        # write the updated author line
                        line = commonDiaryFunctions.unicodeStr('\\authors{' +\
                            ','.join(updatedAuthorList) + '}\n')
                        authorIsUpdated = True
                    tmpTaskFile.write(line)
                oldTaskFile.close()
                tmpTaskFile.close()
                # the temporary task file contains the updated author. Replace the 
                # old task file with this new one
                shutil.move(tmpTaskFilePath,taskPath)
    
if __name__ == '__main__':
    unicodedInputList = \
        commonDiaryFunctions.convertTerminalInputs2Unicode(sys.argv[1:])
    updateAuthor(unicodedInputList)
