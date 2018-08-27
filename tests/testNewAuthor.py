# -*- coding: utf-8 -*-
import unittest, os, sys, time, shutil
sys.path.append('../')
sys.path.append('../database')
sys.path.append('../logic')
import newAuthor, DiaryDatabaseWrapper, commonDiaryFunctions

class TestNewAuthor(unittest.TestCase):
    
    def setUp(self):
        # Move current database to a temporary file if it exists
        self.testDir = \
            commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))
        self.databaseFile = self.testDir + '/../database/diaryDatabase.db'
        self.databaseFileBackup = \
            self.testDir + '/../database/diaryDatabase.backup.db'
        if os.path.isfile(self.databaseFile):
            shutil.move(self.databaseFile,self.databaseFileBackup)
            
    def testAuthorAdding(self):
        # Valid authors
        validAuthorInitialsList = ('jkn','jd')
        if sys.version_info[0] < 3:
            authorNameList = ('Jesper Kjær Nielsen'.decode('utf-8'),'John Doe')
        else:
            authorNameList = ('Jesper Kjær Nielsen','John Doe')
        
        authorEmailList = ('jkn@es.aau.dk','j.doe@gmail.com')
        authorIndex = 0
        for authorInitials in validAuthorInitialsList:
            newAuthor.addAuthor2database((authorInitials, \
                authorNameList[authorIndex], authorEmailList[authorIndex]))
            db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
            authorRows = db.selectFromTable('authors',('name',),\
                'WHERE initials=\'' + authorInitials + '\'')
            self.assertTrue(len(authorRows)==1)
            db.close()
            authorIndex = authorIndex + 1
        # Invalid authors
        if sys.version_info[0] < 3:
            invalidAuthorInitialsList = ('test_','','??!ee',' ','-.pp', \
                'testæøå'.decode('utf-8'))
        else:
            invalidAuthorInitialsList = ('test_','','??!ee',' ','-.pp', \
                'testæøå')
        for authorInitials in invalidAuthorInitialsList:
            with self.assertRaises(SystemExit) as cm:
                newAuthor.addAuthor2database((authorInitials, \
                authorNameList[0], authorEmailList[0]))
            self.assertEqual(cm.exception.code, 2)
        
        
    def tearDown(self):
        # Restore the old database
        if os.path.isfile(self.databaseFileBackup):
            shutil.move(self.databaseFileBackup,self.databaseFile)
          
    # The functions below are not test functions

        
if __name__ == '__main__':
    unittest.main()
