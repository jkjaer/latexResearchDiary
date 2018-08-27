# -*- coding: utf-8 -*-
import unittest, os, sys, time, shutil
sys.path.append('../')
sys.path.append('../database')
sys.path.append('../logic')
import newBuild, DiaryDatabaseWrapper, commonDiaryFunctions, \
    commonDiaryTestFunctions

class TestNewBuild(unittest.TestCase):
    
    def setUp(self):
        # If they exists, move current build files to temporary files 
        self.testDir = \
            commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))
        self.taskList = self.testDir + '/../buildFiles/taskList.tex'
        self.tagDictionary = self.testDir + '/../buildFiles/tagDictionary.tex'
        self.authorDictionary = \
            self.testDir + '/../buildFiles/authorDictionary.tex'
        self.taskListBackup = \
            self.testDir + '/../buildFiles/taskList.backup.tex'
        self.tagDictionaryBackup = \
            self.testDir + '/../buildFiles/tagDictionary.backup.tex'
        self.authorDictionaryBackup = \
            self.testDir + '/../buildFiles/authorDictionary.backup.tex'
        if os.path.isfile(self.taskList):
            shutil.move(self.taskList,self.taskListBackup)
        if os.path.isfile(self.tagDictionary):
            shutil.move(self.tagDictionary,self.tagDictionaryBackup)
        if os.path.isfile(self.authorDictionary):
            shutil.move(self.authorDictionary,self.authorDictionaryBackup)
        # Move all entries to a backup
        self.entriesDir = self.testDir + '/../entries'
        self.entriesDirBackup = self.testDir + '/../entriesBackup'
        shutil.copytree(self.entriesDir, self.entriesDirBackup)
        shutil.rmtree(self.entriesDir)
        # Setup the new entries
        self.testEntriesDir = self.testDir + '/test_new_build_files/entries'
        shutil.copytree(self.testEntriesDir, self.entriesDir)
        # Setup the test database
        self.databaseFile = self.testDir + '/../database/diaryDatabase.db'
        self.databaseFileBackup = \
            self.testDir + '/../database/diaryDatabase.backup.db'
        self.testDatabaseFile = self.testDir + '/test_db/diaryDatabase.db'
        if os.path.isfile(self.databaseFile):
            shutil.move(self.databaseFile,self.databaseFileBackup)
        shutil.copyfile(self.testDatabaseFile,self.databaseFile)
        
            
    def testNewBuildDefault(self):
        # Test ./newBuild.sh
        newBuild.newBuild('')
        expTaskList = \
            self.testDir + '/test_new_build_files/default/taskList.tex'
#        self.assertTrue(os.stat(self.taskList)[6]==0)
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.taskList,expTaskList))
        expTagDictionary = \
            self.testDir + '/test_new_build_files/default/tagDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.tagDictionary,expTagDictionary))
        expAuthorDictionary = \
            self.testDir + '/test_new_build_files/default/authorDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.authorDictionary,expAuthorDictionary))
        
    def testNewBuildAll(self):   
        # Test ./newBuild.sh all all
        newBuild.newBuild(('all','all'))
        expTaskList = \
            self.testDir + '/test_new_build_files/all/taskList.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.taskList,expTaskList))
        expTagDictionary = \
            self.testDir + '/test_new_build_files/all/tagDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.tagDictionary,expTagDictionary))
        expAuthorDictionary = \
            self.testDir + '/test_new_build_files/all/authorDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(self.authorDictionary,expAuthorDictionary))
        
    def testNewBuildMonth(self):   
        # Test ./newBuild.sh all "2013-11,2014-02"
        newBuild.newBuild(('all','2013-11,2014-02'))
        expTaskList = \
            self.testDir + '/test_new_build_files/month/taskList.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.taskList,expTaskList))
        expTagDictionary = \
            self.testDir + '/test_new_build_files/month/tagDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.tagDictionary,expTagDictionary))
        expAuthorDictionary = \
            self.testDir + '/test_new_build_files/month/authorDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.authorDictionary,expAuthorDictionary))
        
    def testNewBuildTag(self):   
        # Test ./newBuild.sh "testTag1,testTag2"
        newBuild.newBuild(('testTag1,testTag2',))
        expTaskList = \
            self.testDir + '/test_new_build_files/tag/taskList.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.taskList,expTaskList))
        expTagDictionary = \
            self.testDir + '/test_new_build_files/tag/tagDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.tagDictionary,expTagDictionary))
        expAuthorDictionary = \
            self.testDir + '/test_new_build_files/tag/authorDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.authorDictionary,expAuthorDictionary))
        
    def testNewBuildTagDate(self):   
        # Test ./newBuild.sh "testTag1,testTag2" "2014-02-12, 2014-03"
        newBuild.newBuild(('testTag1,testTag2','2014-02-12,2014-03'))
        expTaskList = \
            self.testDir + '/test_new_build_files/tag_date/taskList.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.taskList,expTaskList))
        expTagDictionary = \
            self.testDir + '/test_new_build_files/tag_date/tagDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.tagDictionary,expTagDictionary))
        expAuthorDictionary = \
            self.testDir + '/test_new_build_files/tag_date/authorDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.authorDictionary,expAuthorDictionary))
        
    def testNewBuildIncompatibleTagDate(self):   
        # Test ./newBuild.sh "testTag2" "2014-02-12"
        newBuild.newBuild(('testTag2','2014-02-12'))
        expTaskList =  self.testDir + \
            '/test_new_build_files/incompatible_tag_date/taskList.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.taskList,expTaskList))
        expTagDictionary = self.testDir + \
            '/test_new_build_files/incompatible_tag_date/tagDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.tagDictionary,expTagDictionary))
        expAuthorDictionary = \
            self.testDir + '/test_new_build_files/incompatible_tag_date/authorDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.authorDictionary,expAuthorDictionary))
        
    def testNewBuildExcludeTag(self):   
        # Test ./newBuild.sh "testTag2,!testTag3"
        newBuild.newBuild(('testTag2,!testTag3',))
        expTaskList =  self.testDir + \
            '/test_new_build_files/exclude_one_tag/taskList.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.taskList,expTaskList))
        expTagDictionary = self.testDir + \
            '/test_new_build_files/exclude_one_tag/tagDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.tagDictionary,expTagDictionary))
        expAuthorDictionary = self.testDir + \
            '/test_new_build_files/exclude_one_tag/authorDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.authorDictionary,expAuthorDictionary))
        
    def testNewBuildAllExceptOneTag(self):   
        # Test ./newBuild.sh "all,!testTag3"
        newBuild.newBuild(('all,!testTag3',))
        expTaskList =  self.testDir + \
            '/test_new_build_files/include_all_but_one_tag/taskList.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.taskList,expTaskList))
        expTagDictionary = self.testDir + \
            '/test_new_build_files/include_all_but_one_tag/tagDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.tagDictionary,expTagDictionary))
        expAuthorDictionary = self.testDir + \
            '/test_new_build_files/include_all_but_one_tag/authorDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.authorDictionary,expAuthorDictionary))
        
    def testNewBuildTaskLabels(self):   
        # Test ./newBuild.sh all all '20131102_0,20140116_2'
        newBuild.newBuild(('all','all','20131102_0,20140116_2'))
        expTaskList =  self.testDir + \
            '/test_new_build_files/task_labels/taskList.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.taskList,expTaskList))
        expTagDictionary = self.testDir + \
            '/test_new_build_files/task_labels/tagDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.tagDictionary,expTagDictionary))
        expAuthorDictionary = self.testDir + \
            '/test_new_build_files/task_labels/authorDictionary.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.authorDictionary,expAuthorDictionary))
        
    def tearDown(self):
        # Restore the build files
        if os.path.isfile(self.taskListBackup):
            shutil.move(self.taskListBackup,self.taskList)
        if os.path.isfile(self.tagDictionaryBackup):
            shutil.move(self.tagDictionaryBackup,self.tagDictionary)
        if os.path.isfile(self.authorDictionaryBackup):
            shutil.move(self.authorDictionaryBackup,self.authorDictionary)
        # Restore the entries and remove the backup
        shutil.rmtree(self.entriesDir)
        shutil.copytree(self.entriesDirBackup,self.entriesDir)
        shutil.rmtree(self.entriesDirBackup)
        # Restore the database
        if os.path.isfile(self.databaseFileBackup):
            shutil.move(self.databaseFileBackup,self.databaseFile)
      
    # The functions below are not test functions

        
if __name__ == '__main__':
    unittest.main()
