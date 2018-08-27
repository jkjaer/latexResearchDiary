#!/usr/bin/python
import sys, re, os, shutil, io
sys.path.append('database/')
sys.path.append('../logic')
import newTag, DiaryDatabaseWrapper, newBuild, commonDiaryFunctions

# Change a tag in the database.
def updateTag(argv):
    """
        Change a tag in the database.
    """
    if len(argv) < 2:
        print('At least two input parameters must be specified.')
        print('changeTag.py oldTag newTag \"New tag title\"')
        return
    # check if the old and/or new tags are in the database
    oldTagName, oldTagTitle = retrieveTagInfo(argv[0])
    if oldTagName == '':
        print('The old tag %s is not in the database.' % argv[0])
        return
    newTagName, newTagTitle = retrieveTagInfo(argv[1])
    tagMustBeReplaced = newTagName != ''
    if tagMustBeReplaced:
        print('The new tag %s is already in the database.' % argv[1])
        sys.stdout.write("Do you want to replace this tag (y/N)? ")
        choice = commonDiaryFunctions.getUserInput().lower()
        if choice in ('','n','no'):
            print('No tag was changed.')
            return
    # if only two input parameters are set, set the new tag title to the old one
    if len(argv) == 2:
        argv.append(oldTagTitle)
    newTagName, newTagTitle = newTag.validateInputs(argv[1:])
    # update the tags in the diary tasks
    if oldTagName != newTagName:
        updateDiaryTasks(oldTagName,newTagName)
    # update the database
    updateTagDatabase(oldTagName,newTagName,newTagTitle,tagMustBeReplaced)
    print("The tag database and the diary entries have been " \
        "successfully updated.")
    
# check if the tag is in the database and retrieve info if so
def retrieveTagInfo(tagName):
    """
        check if the tag is in the database and retrieve info if so
    """
    db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
    tagRows = db.selectFromTable('tags',('name','title'),\
        'WHERE name=\'' + tagName + '\'')
    db.close()
    if len(tagRows)!=1:
        return '',''
    else:
        return tagRows[0][0], tagRows[0][1]
    
# update the tag database
def updateTagDatabase(oldTagName,newTagName,newTagTitle,tagMustBeReplaced):
    """
        Update the tag database.
    """
    # Create a diary database object.
    db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
    # First delete a tag if needed
    if tagMustBeReplaced:
        db.deleteInTable('tags','name=\'' + newTagName + '\'')
    # update the database
    db.updateTable('tags',('name','title'),\
        (newTagName,newTagTitle),'name=\'' + oldTagName + '\'')
    db.close()
    
# update the tags in the diary entries
def updateDiaryTasks(oldTagName,newTagName):
    """
        update the tags in the diary entries
    """
    dateList = newBuild.getAllDatesWithEntries()
    taskDict, extractedTagsList, extractedAuthorList = \
        newBuild.getTaskDictionary(oldTagName, list(), dateList, list())
    # the task dict contains a list of all the tasks tagged with the old tag.
    # We now cycle through all these files and update this tag
    diaryPath = commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))
    tmpTaskFilePath = diaryPath + '/buildFiles/tmpTask.tex'
    pattern = re.compile(r'^\s*\\tags\{(([a-zA-Z0-9\s]*,)*)' + \
        oldTagName + '(([a-zA-Z0-9\s]*,)*)([a-zA-Z0-9\s]*)\}\s*$')
    for date, taskPathList in sorted(taskDict.items()):
        for relativeTaskPath in taskPathList:
            taskPath = diaryPath + '/' + relativeTaskPath
            oldTaskFile = io.open(taskPath,'r',encoding='utf-8')
            tmpTaskFile = io.open(tmpTaskFilePath,'w',encoding='utf-8')
            tagIsUpdated = False
            for line in oldTaskFile:
                # to avoid scanning all lines in the file, a flag is set when
                # the tag has been updated
                if not tagIsUpdated and re.match(pattern,line):
                    tagPattern = \
                        re.compile(r'^\s*\\tags\{(!*[a-zA-Z0-9,\s]+)\}\s*$')
                    tagList = \
                        re.search(tagPattern,line).group(1).split(',')
                    updatedTagList = list()
                    for tag in tagList:
                        # remove white space
                        tag = tag.strip()
                        # Remove any duplicates.
                        if tag == oldTagName:
                            updatedTagList.append(newTagName)
                        elif tag != newTagName:
                            updatedTagList.append(tag)
                    # write the updated tag line
                    line = commonDiaryFunctions.unicodeStr('\\tags{' + \
                        ','.join(updatedTagList) + '}\n')
                    tagIsUpdated = True
                tmpTaskFile.write(line)
            oldTaskFile.close()
            tmpTaskFile.close()
            # the temporary task file contains the updated tag. Replace the 
            # old task file with this new one
            shutil.move(tmpTaskFilePath,taskPath)
    
if __name__ == '__main__':
    unicodedInputList = \
        commonDiaryFunctions.convertTerminalInputs2Unicode(sys.argv[1:])
    updateTag(unicodedInputList)
