# -*- coding: utf-8 -*-
import unittest, os, sys, time, shutil
sys.path.append('../')
sys.path.append('../database')
sys.path.append('../logic')
import changeTag, newTag, DiaryDatabaseWrapper, commonDiaryFunctions, \
    commonDiaryTestFunctions

class TestChangeTag(unittest.TestCase):
    
    def setUp(self):
        # Move current database to a temporary file if it exists
        self.testDir = \
            commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))
        self.databaseFile = self.testDir + '/../database/diaryDatabase.db'
        self.databaseFileBackup = \
            self.testDir + '/../database/diaryDatabase.backup.db'
        if os.path.isfile(self.databaseFile):
            shutil.move(self.databaseFile,self.databaseFileBackup)
        # Move all entries to a backup
        self.entriesDir = self.testDir + '/../entries'
        self.entriesDirBackup = self.testDir + '/../entriesBackup'
        shutil.copytree(self.entriesDir, self.entriesDirBackup)
        shutil.rmtree(self.entriesDir)
        # Setup the new entries
        self.testEntriesDir = self.testDir + '/test_change_tag_files/entries'
        shutil.copytree(self.testEntriesDir, self.entriesDir)
        self.entryPath = self.testDir + '/../entries/2014/08/24/20140824_0.tex'
            
    def testChangeValidTagAndTitle(self):
        oldTag = 'testTag'
        anotherTag = 'anotherTestTag'
        oldTagTitle = 'Test title'
        anotherTagTitle = 'Another Test title'
        # Add the old tag to the tag database
        newTag.addTag2database(list((oldTag,oldTagTitle)))
        newTag.addTag2database(list((anotherTag,anotherTagTitle)))
        # The new tag and tag title
        expNewTag = 'newTestTag'
        expNewTagTitle = 'New Test Title'
        # Change the tag and tag title
        changeTag.updateTag(list((oldTag,expNewTag,expNewTagTitle)))
        # Check that the tag and tag title has been updated
        db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
        tagRows = db.selectFromTable('tags',('name','title'),\
            'WHERE name=\'' + expNewTag + '\'')
        self.assertTrue(len(tagRows)==1)
        self.assertEqual(tagRows[0][0],expNewTag)
        self.assertEqual(tagRows[0][1],expNewTagTitle)
        # Check that the entries have been updated
        expEntry = \
            self.testDir + '/test_change_tag_files/tag_and_title/20140824_0.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.entryPath,expEntry))
        
    def testChangeAndReplaceValidTag(self):
        oldTag = 'testTag'
        anotherTag = 'anotherTestTag'
        oldTagTitle = 'Test title'
        anotherTagTitle = 'Another Test title'
        # Add the old tag to the tag database
        newTag.addTag2database(list((oldTag,oldTagTitle)))
        newTag.addTag2database(list((anotherTag,anotherTagTitle)))
        # The new tag and tag title
        expNewTag = 'anotherTestTag'
        expNewTagTitle = oldTagTitle
        # Change the tag and tag title
        changeTag.updateTag(list((oldTag,expNewTag)))
        # Check that the tag and tag title has been updated
        db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
        tagRows = db.selectFromTable('tags',('name','title'),\
            'WHERE name=\'' + expNewTag + '\'')
        self.assertTrue(len(tagRows)==1)
        self.assertEqual(tagRows[0][0],expNewTag)
        self.assertEqual(tagRows[0][1],expNewTagTitle)
        # Check that the entries have been updated
        expEntry = \
            self.testDir + '/test_change_tag_files/tag_replace/20140824_0.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.entryPath,expEntry))
        
    def tearDown(self):
        # Restore the entries and remove the backup
        shutil.rmtree(self.entriesDir)
        shutil.copytree(self.entriesDirBackup,self.entriesDir)
        shutil.rmtree(self.entriesDirBackup)
        # Restore the old database
        if os.path.isfile(self.databaseFileBackup):
            shutil.move(self.databaseFileBackup,self.databaseFile)
          
    # The functions below are not test functions

        
if __name__ == '__main__':
    unittest.main()
