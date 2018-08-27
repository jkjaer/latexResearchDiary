# -*- coding: utf-8 -*-
import unittest, os, sys, time, shutil, datetime
sys.path.append('../')
sys.path.append('../database')
sys.path.append('../logic')
import addTask, DiaryDatabaseWrapper, commonDiaryFunctions, \
    commonDiaryTestFunctions

class TestAddTask(unittest.TestCase):
    
    def setUp(self):
        self.testDir = \
            commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))
        # Move all entries to a backup
        self.entriesDir = self.testDir + '/../entries'
        self.entriesDirBackup = self.testDir + '/../entriesBackup'
        shutil.copytree(self.entriesDir, self.entriesDirBackup)
        shutil.rmtree(self.entriesDir)
        # Setup the new empty entries dir
        os.makedirs(self.entriesDir)
        # Setup the test database
        self.databaseFile = self.testDir + '/../database/diaryDatabase.db'
        self.databaseFileBackup = \
            self.testDir + '/../database/diaryDatabase.backup.db'
        self.testDatabaseFile = self.testDir + '/test_db/diaryDatabase.db'
        if os.path.isfile(self.databaseFile):
            shutil.move(self.databaseFile,self.databaseFileBackup)
        shutil.copyfile(self.testDatabaseFile,self.databaseFile)
            
    def testNewDefaultTask(self):
        # Generate two new tasks
        if sys.version_info[0] < 3:
            addTask.addTask(('testTag1,testTag2',\
                'This is the title of the task ÆØÅ'.decode('utf-8')))
            addTask.addTask(('testTag1,testTag2',\
                'This is the title of the task ÆØÅ'.decode('utf-8')))
        else:
            addTask.addTask(('testTag1,testTag2',\
                'This is the title of the task ÆØÅ'))
            addTask.addTask(('testTag1,testTag2',\
                'This is the title of the task ÆØÅ'))
        # Find the current date
        year, month, day = self.getTodayStrings()
        # Update the expected task file with the date label
        expTaskTemplatePath = self.testDir + \
            '/test_add_task_files/default/default.tpl.tex'
        expTaskPath0 = self.createExpTaskFile(expTaskTemplatePath,'default',\
            year,month,day,'',0)
        expTaskPath1 = self.createExpTaskFile(expTaskTemplatePath,'default',\
            year,month,day,'',1)
        # Check that the actual task file is identical to the expected
        actTaskPath0 = self.testDir + '/../entries/' + year + '/' + month + \
            '/' + day + '/' + year + month + day + '_0.tex'
        actTaskPath1 = self.testDir + '/../entries/' + year + '/' + month + \
            '/' + day + '/' + year + month + day + '_1.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            actTaskPath0,expTaskPath0))
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            actTaskPath1,expTaskPath1))
        # remove the generated task file
        os.remove(expTaskPath0)
        os.remove(expTaskPath1)
        
    def testNewTemplate(self):
        # Generate a new task
        addTask.addTask(('testTag1,testTag2','This is the title of the task',\
            '','review'))
        # Find the current date
        year, month, day = self.getTodayStrings()
        # Update the expected task file with the date label
        expTaskTemplatePath = self.testDir + \
            '/test_add_task_files/template/review.tpl.tex'
        expTaskPath = self.createExpTaskFile(expTaskTemplatePath,'template',\
            year,month,day,'',0)
        # Check that the actual task file is identical to the expected
        actTaskPath = self.testDir + '/../entries/' + year + '/' + month + \
            '/' + day + '/' + year + month + day + '_0.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            actTaskPath,expTaskPath))
        # remove the generated task file
        os.remove(expTaskPath)
        
    def testAuthorInitials(self):
        # Generate a new task
        addTask.addTask(('testTag1,testTag2','This is the title of the task',\
            'jkn'))
        addTask.addTask(('testTag1,testTag2','This is the title of the task',\
            'shj'))
        addTask.addTask(('testTag1,testTag2','This is the title of the task',\
            'jkn,shj'))
        addTask.addTask(('testTag1,testTag2','This is the title of the task',\
            'shj,jkn'))
        # Find the current date
        year, month, day = self.getTodayStrings()
        # Update the expected task file with the date label
        expTaskTemplatePath = self.testDir + \
            '/test_add_task_files/author/default.tpl.tex'
        expTaskPathJkn0 = self.createExpTaskFile(expTaskTemplatePath,'author',\
            year,month,day,('jkn',),0)
        expTaskPathJkn1 = self.createExpTaskFile(expTaskTemplatePath,'author',\
            year,month,day,('jkn','shj'),1)
        expTaskPathShj0 = self.createExpTaskFile(expTaskTemplatePath,'author',\
            year,month,day,('shj',),0)
        expTaskPathShj1 = self.createExpTaskFile(expTaskTemplatePath,'author',\
            year,month,day,('shj','jkn'),1)
        # Check that the actual task file is identical to the expected
        actTaskPathJkn0 = self.testDir + '/../entries/' + year + '/' + month + \
            '/' + day + '/' + year + month + day + '_jkn0.tex'
        actTaskPathJkn1 = self.testDir + '/../entries/' + year + '/' + month + \
            '/' + day + '/' + year + month + day + '_jkn1.tex'
        actTaskPathShj0 = self.testDir + '/../entries/' + year + '/' + month + \
            '/' + day + '/' + year + month + day + '_shj0.tex'
        actTaskPathShj1 = self.testDir + '/../entries/' + year + '/' + month + \
            '/' + day + '/' + year + month + day + '_shj1.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            actTaskPathJkn0,expTaskPathJkn0))
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            actTaskPathJkn1,expTaskPathJkn1))
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            actTaskPathShj0,expTaskPathShj0))
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            actTaskPathShj1,expTaskPathShj1))
        # remove the generated task file
        os.remove(expTaskPathJkn0)
        os.remove(expTaskPathJkn1)
        os.remove(expTaskPathShj0)
        os.remove(expTaskPathShj1)
        
    def testSetDate(self):
        # Generate a new task
        year = '2014'
        month = '06'
        day = '01'
        addTask.addTask(('testTag1,testTag2','This is the title of the task',\
            '','',year + '-' + month + '-' + day))
        # Update the expected task file with the date label
        expTaskTemplatePath = self.testDir + \
            '/test_add_task_files/date/default.tpl.tex'
        expTaskPath = self.createExpTaskFile(expTaskTemplatePath,'date',\
            year,month,day,'',0)
        # Check that the actual task file is identical to the expected
        actTaskPath = self.testDir + '/../entries/' + year + '/' + month + \
            '/' + day + '/' + year + month + day + '_0.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            actTaskPath,expTaskPath))
        # remove the generated task file
        os.remove(expTaskPath)
        
    def tearDown(self):
        # Restore the entries and remove the backup
        shutil.rmtree(self.entriesDir)
        shutil.copytree(self.entriesDirBackup,self.entriesDir)
        shutil.rmtree(self.entriesDirBackup)
        # Restore the database
        if os.path.isfile(self.databaseFileBackup):
            shutil.move(self.databaseFileBackup,self.databaseFile)
          
    # The functions below are not test functions
    def getTodayStrings(self):
        now = datetime.datetime.now()
        year = str(now.year)
        month = str(now.month).zfill(2)
        day = str(now.day).zfill(2)
        return year, month, day
        
    def createExpTaskFile(self,expTaskTemplatePath,testName,year,month,day,\
            authorList,index):
        if len(authorList)>0:
            author = authorList[0]
        else:
            author = ''
        expTaskPath = self.testDir + '/test_add_task_files/' + testName + \
            '/' + year + month + day + '_' + author + str(index) + '.tex'
        templateTaskFile = open(expTaskTemplatePath,'r')
        taskFile = open(expTaskPath,'w')
        for line in templateTaskFile:
            line = line.replace('@label', year + month + day + '_' + \
                author + str(index))
            line = line.replace('@author', ','.join(authorList))
            taskFile.write(line)
        templateTaskFile.close()
        taskFile.close()
        return expTaskPath
        
if __name__ == '__main__':
    unittest.main()
