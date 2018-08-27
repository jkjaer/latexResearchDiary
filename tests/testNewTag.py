# -*- coding: utf-8 -*-
import unittest, os, sys, time, shutil
sys.path.append('../')
sys.path.append('../database')
sys.path.append('../logic')
import newTag, DiaryDatabaseWrapper, commonDiaryFunctions

class TestNewTag(unittest.TestCase):
    
    def setUp(self):
        # Move current database to a temporary file if it exists
        self.testDir = \
            commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))
        self.databaseFile = self.testDir + '/../database/diaryDatabase.db'
        self.databaseFileBackup = \
            self.testDir + '/../database/diaryDatabase.backup.db'
        if os.path.isfile(self.databaseFile):
            shutil.move(self.databaseFile,self.databaseFileBackup)
            
    def testTagAdding(self):
        # Valid tags
        validTagNameList = ('testTag','123test','12345','test321','t1e2s3t')
        if sys.version_info[0] < 3:
            tagTitle = 'This is a tag title æøå'.decode('utf-8')
        else:
            tagTitle = 'This is a tag title æøå'
        for tagName in validTagNameList:
            newTag.addTag2database((tagName,tagTitle))
            db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
            tagRows = db.selectFromTable('tags',('name',),\
                'WHERE name=\'' + tagName + '\'')
            self.assertTrue(len(tagRows)==1)
            db.close()
        # Invalid tags
        if sys.version_info[0] < 3:
            invalidTagNameList = ('test_','','??!ee',' ','-.pp', \
                'testæøå'.decode('utf-8'))
        else:
            invalidTagNameList = ('test_','','??!ee',' ','-.pp', \
                'testæøå')
        for tagName in invalidTagNameList:
            with self.assertRaises(SystemExit) as cm:
                newTag.addTag2database((tagName,tagTitle))
            self.assertEqual(cm.exception.code, 2)
        
        
    def tearDown(self):
        # Restore the old database
        if os.path.isfile(self.databaseFileBackup):
            shutil.move(self.databaseFileBackup,self.databaseFile)
          
    # The functions below are not test functions

        
if __name__ == '__main__':
    unittest.main()
