#!/usr/bin/python
import sys, datetime, calendar, os, re, io
sys.path.append('database/')
sys.path.append('logic/')
import DiaryDatabaseWrapper, addTask, commonDiaryFunctions

def newBuild(argv):
    """
        Generate a new build file.
    """
    # Get/validate tags and dates
    includeTagList, excludeTagList, dateList, taskLabelList = \
        validateInputsAndSetDefaults(argv)
    # Find the tasks with valid tags and the selected dates
    taskDict, extractedTagsList, extractedAuthorList = \
        getTaskDictionary(includeTagList, excludeTagList, dateList, \
        taskLabelList)
    # Write the extracted tags and titles to the tag dictionary file in the
    # buildFiles folder.
    writeTagsToTexDictionary(extractedTagsList)
    # Write the extracted authors to the author dictionary file in the
    # buildFiles folder.
    writeAuthorsToTexDictionary(extractedAuthorList)
    createBuildFile(taskDict)
    print('The tag dictionary and the task list have successfully been updated.')
    
# Input validation
def validateInputsAndSetDefaults(argv):
    """
        Validate the provided input and set the defaults values for
        the optional parameters if not specified or empty.
    """
    nInputs = len(argv)
    if nInputs==0:
        # Default setup for no input parameters
        includeTagList = getAllTags()
        excludeTagList = list()
        dateList = getDefaultDates()
        taskLabelList = list()
    elif nInputs==1:
        if argv[0]=='all' or argv[0]=='':
            # Include all tags and dates
            includeTagList = getAllTags()
            excludeTagList = list()
        else:
            # Only tags are specified
            includeTagList, excludeTagList = separateAndValidateTags(argv[0])
        dateList = getAllDatesWithEntries()    
        taskLabelList = list()
    elif nInputs==2:
        if argv[0]=='all' or argv[0]=='':
            # Include all tags
            includeTagList = getAllTags()
            excludeTagList = list()
        else:
            includeTagList, excludeTagList = separateAndValidateTags(argv[0])
        if argv[1]=='all' or argv[1]=='':
            # Include all dates
            dateList = getAllDatesWithEntries()
        else:
            dateList = checkAndFindDates(argv[1])
        taskLabelList = list()
    elif nInputs==3:
        if argv[0]=='all' or argv[0]=='':
            # Include all tags
            includeTagList = getAllTags()
            excludeTagList = list()
        else:
            includeTagList, excludeTagList = separateAndValidateTags(argv[0])
        if argv[1]=='all' or argv[1]=='':
            # Include all dates
            dateList = getAllDatesWithEntries()
        else:
            dateList = checkAndFindDates(argv[1])
        if argv[2]=='all' or argv[2]=='':
            # An empty list means that all task labels should be included
            taskLabelList = list()
        else:
            taskLabelList = validateTaskLabels(argv[2])
    else:
        print("Error: You must specify 0, 1, 2, or 3 input parameters.")
        print("newBuild.py \'tagA, tagB\' \'YYYY-MM-DD, YYYY-MM\' " \
            "\'taskLabel1, taskLabel2\'")
        sys.exit(2)
    return includeTagList, excludeTagList, dateList, taskLabelList
    
# Get all tags
def getAllTags():
    """
        Retrieve all tags from the tags database.
    """
    # Create a diary database object.
    db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
    tagRows = db.selectFromTable('tags',('name',),'')
    db.close()
    return [element[0] for element in tagRows]

# Get the default dates with valid entries.
def getDefaultDates():
    """
        Get the default dates. These are the lastest 90 days.
    """
    nDays = 90
    dateNDaysAgo = datetime.date.today()-datetime.timedelta(days=nDays)
    return getAllDatesWithEntries(fromDate=dateNDaysAgo)
    
# Get all dates with entries
def getAllDatesWithEntries(fromDate=datetime.date(1970,1,1)):
    """
        Get all dates from a specific date.
    """
    dateList = list()
    entriesDir = commonDiaryFunctions.unicodeDir(os.path.abspath(__file__)) + \
        '/entries'
    yearFolders = getDigitFolders(entriesDir)
    for yearFolder in yearFolders:
        iPath = entriesDir + '/' + yearFolder
        monthFolders = getDigitFolders(iPath)
        for monthFolder in monthFolders:
            jPath = iPath + '/' + monthFolder
            dayFolders = getDigitFolders(jPath)
            for dayFolder in dayFolders:
                candidateDate = datetime.date(year=int(yearFolder),\
                    month=int(monthFolder),day=int(dayFolder))
                if fromDate<=candidateDate:
                    dateList.append(candidateDate)
    return sorted(dateList)
    
# Separates the provided tags into including and excluding tags
def separateAndValidateTags(tagListString):
    """
        Separates the provided tags into two list. The first list consists
        of tags without a leading exclamation mark while the second list
        only consists of tags with a leading exclamation mark.
    """
    rawTagList = tagListString.split(',')
    rawIncludeTagList = list()
    rawExcludeTagList = list()
    for tag in rawTagList:
        # Remove leading and trailing spaces
        tag = tag.strip()
        # Separate the tags
        if tag[0] == '!':
            rawExcludeTagList.append(tag[1:])
        else:
            if tag == 'all':
                rawIncludeTagList = getAllTags()
            else:
                rawIncludeTagList.append(tag)
    # Check the tags
    if len(rawExcludeTagList):
        excludeTagList = addTask.checkTags(','.join(rawExcludeTagList))[1]
    else:
        excludeTagList = list()
    if len(rawIncludeTagList):
        includeTagList = addTask.checkTags(','.join(rawIncludeTagList))[1]
    else:
        includeTagList = list()
    return includeTagList, excludeTagList

# Validates that the provided task labels have the correct format
def validateTaskLabels(taskLabelListString):
    """
        Validates that the provided task labels have the correct format.
    """
    taskLabelList = taskLabelListString.split(',')
    validatedTaskLabelList = list()
    # The task labels must match the pattern YYYYMMDD_XXXI
    # where XXX are optional initials (letters a-zA-Z) and I is a number.
    taskLabelPattern = re.compile(r'^([0-9]{8})_([a-zA-Z]*)([0-9]+)$')
    for taskLabel in taskLabelList:
        # Remove leading and trailing spaces
        taskLabel = taskLabel.strip()
        # Check if the first eight characters corresponds to a valid date
        try:
            validDateTime = datetime.datetime.strptime(taskLabel[0:8], '%Y%m%d')
        except ValueError:
            raise ValueError("Invalid task label supplied" + taskLabel + \
                ". Should be YYYYMMDD_XXXI where YYYYMMDD are the "\
                "date, XXX are optional initials (letters a-zA-Z), "\
                "and I is a number.")
        # Check the task labels
        if re.match(taskLabelPattern, taskLabel):
            validatedTaskLabelList.append(taskLabel)
        else:
            print("Invalid task label supplied" + taskLabel + \
                 ". Should be YYYYMMDD_XXXI where YYYYMMDD are the "\
                "date, XXX are optional initials (letters a-zA-Z), "\
                "and I is a number.")
            sys.exit(2)
    return validatedTaskLabelList
        
# Returns a list of folders consisting of only digits
def getDigitFolders(path):
    """
        Returns a list folders consisting of only digits.
    """
    digitFolderList = list()
    filesAndFolders = os.listdir(path)
    for fileAndFolder in filesAndFolders:
        iPath = path + '/' + fileAndFolder
        if fileAndFolder.isdigit() and os.path.isdir(iPath):
            digitFolderList.append(fileAndFolder)
    return digitFolderList
    
# Check if the provided dates are valid
def checkAndFindDates(dateListString):
    """
        Check if the provided dates are valid
    """
    rawDateList = dateListString.split(',')
    allDatesList = list()
    for date in rawDateList:
        # First remove space around the date
        date = date.strip()
        try:
            # First see if the date is a specific day
            validDateTime = datetime.datetime.strptime(date, '%Y-%m-%d')
            allDatesList.append(validDateTime.date())
        except ValueError:
            try:
                # If not a specific day, see if it is a specific month.
                validDateTime = datetime.datetime.strptime(date, '%Y-%m')
                allDatesList.extend(getAllDatesFromYearMonth(validDateTime.year,\
                    validDateTime.month))
            except ValueError:
                try:
                    # If neither a specific day or month, see if it is a 
                    # specific year.
                    validDateTime = datetime.datetime.strptime(date, '%Y')
                    allDatesList.extend(getAllDatesFromYear(validDateTime.year))
                except ValueError:
                    raise ValueError("Incorrect data format, should be " + \
                        "either YYYY-MM-DD, YYYY-MM, or YYYY.")
    # Remove duplicate dates and sort the list
    uniqueDatesList = list(set(allDatesList))
    # Only retain those dates with entries
    dateList = list()
    for date in uniqueDatesList:
        if dateHasEntry(date):
            dateList.append(date)
    return sorted(dateList)

# Get all dates from year and month
def getAllDatesFromYearMonth(year,month):
    """
        Get all dates from year and month.
    """
    if month<12:
        nDays = (datetime.date(year,month+1,1)-\
            datetime.date(year,month,1)).days
    else:
        nDays = (datetime.date(year+1,1,1)-\
            datetime.date(year,month,1)).days
    dateList = list()
    for dayNo in range(1,nDays+1):
        dateList.append(datetime.date(year,month,dayNo))
    return dateList
    
# Get all datas from year
def getAllDatesFromYear(year):
    """
        Get all datas from year.
    """
    dateList = list()
    for monthNo in range(1,13):
        dateList.extend(getAllDatesFromYearMonth(year,monthNo))
    return dateList
    
# Check if a date folder has been created
def dateHasEntry(date):
    """
        Returns true if a folder structure exists for the day
    """
    dir = commonDiaryFunctions.unicodeDir(os.path.abspath(__file__)) + \
        '/entries/' + str(date.year) + '/' + str(date.month).zfill(2) + \
        '/' + str(date.day).zfill(2)
    if os.path.isdir(dir):
        return True
    else:
        return False

# Write the tags and titles to the tag dictionary file in the build files folder.
def writeTagsToTexDictionary(tagList):
    """
        Write the tags and titles to the tag dictionary file in the build files
        folder.
    """
    tagTitleList = getTagTitles(tagList)
    buildFilesDir = commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))\
        + '/buildFiles'
    if not os.path.exists(buildFilesDir):
        os.makedirs(buildFilesDir)
    tagDictionaryFile = io.open(buildFilesDir + '/tagDictionary.tex',\
        'w',encoding='utf-8')
    nTags = len(tagList)
    for iTag in range(nTags):
        tagTitle = tagTitleList[iTag]
        tagDictionaryFile.write('\expandafter\\newcommand\csname tag' + \
            tagList[iTag] + '\endcsname{' + tagTitle + '}\n')
    tagDictionaryFile.close()
    
# Retrieve the tag titles associated with the tag names.
def getTagTitles(tagList):
    """
        Retrieve the tag titles associated with the tag names.
    """
    db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()    
    tagTitles = list()
    for tag in tagList:
        tagRows = db.selectFromTable('tags',('title',),\
            'WHERE name=\'' + tag + '\'')
        tagTitles.append(tagRows[0][0])
    db.close()
    return tagTitles

# Write the authors to the tag dictionary file in the build files folder.
def writeAuthorsToTexDictionary(authorInitialsList):
    """
        Write the authors to the tag dictionary file in the build files
        folder.
    """
    authorNameList, authorEmailList = getAuthorNamesAndEmail(authorInitialsList)
    buildFilesDir = commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))\
        + '/buildFiles'
    if not os.path.exists(buildFilesDir):
        os.makedirs(buildFilesDir)
    authorDictionaryFile = io.open(buildFilesDir + '/authorDictionary.tex',\
        'w',encoding='utf-8')
    nAuthors = len(authorInitialsList)
    for iAuthor in range(nAuthors):
        authorName = authorNameList[iAuthor]
        authorEmail = authorEmailList[iAuthor]
        authorDictionaryFile.write('\expandafter\\newcommand\csname author' + \
            authorInitialsList[iAuthor] + \
            'name\endcsname{' + authorName +'}\n')
        authorDictionaryFile.write('\expandafter\\newcommand\csname author' + \
            authorInitialsList[iAuthor] + \
            'email\endcsname{' + \
            authorEmail +'}\n')
    authorDictionaryFile.close()

# Retrieve the author names and emails from the author initials.
def getAuthorNamesAndEmail(authorInitialsList):
    """
        Retrieve the author names and emails from the author initials.
    """
    db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()    
    authorNameList = list()
    authorEmailList = list()
    for authorInitials in authorInitialsList:
        authorRows = db.selectFromTable('authors',('name','email'),\
            'WHERE initials=\'' + authorInitials + '\'')
        authorNameList.append(authorRows[0][0])
        authorEmailList.append(authorRows[0][1])
    db.close()
    return authorNameList, authorEmailList
        
# Find the tasks with valid tags and the selected dates
def getTaskDictionary(includeTagList, excludeTagList, dateList, \
    taskLabelList):
    """
        Find the tasks with valid tags and the selected dates. The key of the
        returned dictionary is the date and the values are the file names of
        the tags.
    """
    taskDict = dict()
    extractedTagsList = list()
    extractedAuthorList = list()
    diaryDir = commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))
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
                # If the taskLabelList is not empty, check if the file name
                # is in the list
                if len(taskLabelList)==0 or fileOrFolder[:-4] in taskLabelList:
                    extractedTags = extractTagsFromValidTask(taskPath, \
                        includeTagList, excludeTagList)
                    if len(extractedTags)>0:
                        extractedAuthors = extractAuthorsFromTask(taskPath)
                        if len(extractedAuthors)>0:
                            extractedAuthorList.extend(extractedAuthors)
                        validTaskPathList.append(relativeTaskPath)
                        extractedTagsList.extend(extractedTags)
        # If a least one task path has been added, add it to the dictionary
        if len(validTaskPathList)>0:
            taskDict[date] = validTaskPathList
    # return the task dictionary and the unique extracted tags and authors
    return taskDict, sorted(list(set(extractedTagsList))), \
        sorted(list(set(extractedAuthorList)))
    
# Extracts all the tags from a valid task.
def extractTagsFromValidTask(taskPath, includeTagList, excludeTagList):
    """
        Extracts all the tags from a valid task. A valid task contains at least
        one of the tags in the tagList and no excluding tags.
    """
    texFile = io.open(taskPath,'r',encoding='utf-8')
    for line in texFile:
        for includeTag in includeTagList:
            # The line must match the pattern \tags{tagA,...,tagN}
            pattern = re.compile(r'^\s*\\tags\{(([a-zA-Z0-9\s]*,)*)' + \
                includeTag + '(([a-zA-Z0-9\s]*,)*)([a-zA-Z0-9\s]*)\}\s*$')
            if re.match(pattern, line):
                # A valid tag was found in the entry. Extract all tags and
                # return.
                pattern = re.compile(r'^\s*\\tags\{(!*[a-zA-Z0-9,\s]+)\}\s*$')
                tagListString = re.search(pattern,line).group(1)
                # Check that the extracted tags are valid and split the
                # string into a list
                extractedTagList = addTask.checkTags(tagListString)[1]
                # Check that none of the tags are in the excludeTagList
                for extractedTag in extractedTagList:
                    if extractedTag in excludeTagList:
                        texFile.close()
                        return list()
                # If none of the extracted tags are in the excludeTagList,
                # return the extracted tag list
                texFile.close()
                return extractedTagList
    # None of the tags in the includeTagList was in the task
    texFile.close()
    return list()
    
# Extracts all the authors from a task.
def extractAuthorsFromTask(taskPath):
    """
        Extracts all the authors from a task
    """
    texFile = io.open(taskPath,'r',encoding='utf-8')
    for line in texFile:
        # The line must match the pattern \authors{initials1,...,initials2}
        pattern = \
            re.compile(r'^\s*\\authors\{(([a-zA-Z0-9\s]*,)*)([a-zA-Z0-9\s]*)\}\s*$')
        if re.match(pattern, line):
            # The author line was found. Extract all author initials
            pattern = re.compile(r'^\s*\\authors\{(!*[a-zA-Z0-9,\s]+)\}\s*$')
            authorListString = re.search(pattern,line).group(1)
            # Check that the authors are valid and split the
            # string into a list
            if len(authorListString)>0:
                extractedAuthorList = addTask.checkAuthors(authorListString)
            else:
                extractedAuthorList = list()
            texFile.close()
            return extractedAuthorList
    # The author string was not found in the file
    texFile.close()
    return list()
    
# Create the build file
def createBuildFile(taskDict):
    """
        Create the build file.
    """
    oldYear = 1970
    oldMonth = 0
    buildFilesDir = commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))\
        + '/buildFiles'
    buildFile = io.open(buildFilesDir + '/taskList.tex','w',encoding='utf-8')
    for date, taskPathList in sorted(taskDict.items()):
        # If a new year, month, and/or are started, add a new part, chapter,
        # and/or section
        year = date.year
        month = date.month
        day = date.day
        if oldYear!=year:
            buildFile.write('\part{'+ \
                commonDiaryFunctions.unicodeStr(year) +'}\n')
            oldYear = year
            # reset oldMonth
            oldMonth = 0
        if oldMonth!=month:
            buildFile.write('\chapter{'+ \
            commonDiaryFunctions.unicodeStr(calendar.month_name[month]) +'}\n')
            oldMonth=month
        buildFile.write('\section{'+ \
            commonDiaryFunctions.unicodeStr(calendar.month_name[month]) + \
            ' ' + commonDiaryFunctions.unicodeStr(day) + ', '\
            + commonDiaryFunctions.unicodeStr(year) +'}\n')
        # Add all tasks
        for taskPath in taskPathList:
            buildFile.write('\input{' + taskPath + '}\n')
    buildFile.close()

# The first function to be called when this file is used as a script
if __name__ == '__main__':
    unicodedInputList = \
        commonDiaryFunctions.convertTerminalInputs2Unicode(sys.argv[1:])
    newBuild(unicodedInputList)
