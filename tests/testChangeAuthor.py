# -*- coding: utf-8 -*-
import unittest, os, sys, time, shutil
sys.path.append('../')
sys.path.append('../database')
sys.path.append('../logic')
import changeAuthor, newAuthor, DiaryDatabaseWrapper, commonDiaryFunctions, \
    commonDiaryTestFunctions

class TestChangeAuthor(unittest.TestCase):
    
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
        self.testEntriesDir = self.testDir + '/test_change_author_files/entries'
        shutil.copytree(self.testEntriesDir, self.entriesDir)
        self.entryPath = self.testDir + '/../entries/2014/08/24/20140824_jkn0.tex'
            
    def testChangeValidAuthor(self):
        oldAuthorInitials = 'jkn'
        anotherAuthorInitials = 'jd'
        if sys.version_info[0] < 3:
            oldAuthorName = 'Jesper Kjær Nielsen'.decode('utf-8')
        else:
            oldAuthorName = 'Jesper Kjær Nielsen'
        anotherAuthorName = 'John Doe'
        oldAuthorEmail = 'jkn@es.aau.dk'
        anotherAuthorEmail =  'jd@gmail.com'
        # Add the old author to the author database
        newAuthor.addAuthor2database(list((oldAuthorInitials,oldAuthorName,\
            oldAuthorEmail)))
        newAuthor.addAuthor2database(list((anotherAuthorInitials,anotherAuthorName,\
            anotherAuthorEmail)))
        # The new author
        expNewAuthorInitials = 'jk'
        if sys.version_info[0] < 3:
            expNewAuthorName = 'Jesper Kjaer Nielsen'.decode('utf-8')
        else:
            expNewAuthorName = 'Jesper Kjaer Nielsen'
        expNewAuthorEmail = 'jk@gmail.com'
        # Change the author info
        changeAuthor.updateAuthor(list((oldAuthorInitials,expNewAuthorInitials,\
            expNewAuthorName,expNewAuthorEmail)))
        # Check that the author info has been updated
        db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
        authorRows = db.selectFromTable('authors',('initials','name','email'),\
            'WHERE initials=\'' + expNewAuthorInitials + '\'')
        self.assertTrue(len(authorRows)==1)
        self.assertEqual(authorRows[0][0],expNewAuthorInitials)
        self.assertEqual(authorRows[0][1],expNewAuthorName)
        self.assertEqual(authorRows[0][2],expNewAuthorEmail)
        # Check that the entries have been updated
        expEntry = \
            self.testDir + '/test_change_author_files/author_info/20140824_jkn0.tex'
        self.assertTrue(commonDiaryTestFunctions.isFileContentIdentical(\
            self.entryPath,expEntry))
        
    def testChangeValidAuthorInitials(self):
        oldAuthorInitials = 'jkn'
        anotherAuthorInitials = 'jd'
        if sys.version_info[0] < 3:
            oldAuthorName = 'Jesper Kjær Nielsen'.decode('utf-8')
        else:
            oldAuthorName = 'Jesper Kjær Nielsen'
        anotherAuthorName = 'John Doe'
        oldAuthorEmail = 'jkn@es.aau.dk'
        anotherAuthorEmail =  'jd@gmail.com'
        # Add the old author to the author database
        newAuthor.addAuthor2database(list((oldAuthorInitials,oldAuthorName,\
            oldAuthorEmail)))
        newAuthor.addAuthor2database(list((anotherAuthorInitials,anotherAuthorName,\
            anotherAuthorEmail)))
        # The new author
        expNewAuthorInitials = 'jd'
        expNewAuthorName = oldAuthorName
        expNewAuthorEmail = oldAuthorEmail
        # Change the author info
        changeAuthor.updateAuthor(list((oldAuthorInitials,expNewAuthorInitials)))
        # Check that the author info has been updated
        db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
        authorRows = db.selectFromTable('authors',('initials','name','email'),\
            'WHERE initials=\'' + expNewAuthorInitials + '\'')
        self.assertTrue(len(authorRows)==1)
        self.assertEqual(authorRows[0][0],expNewAuthorInitials)
        if sys.version_info[0] < 3:
            self.assertEqual(authorRows[0][1],expNewAuthorName)
            self.assertEqual(authorRows[0][2],expNewAuthorEmail)
        else:
            self.assertEqual(authorRows[0][1],expNewAuthorName)
            self.assertEqual(authorRows[0][2],expNewAuthorEmail)
        # Check that the entries have been updated
        expEntry = self.testDir + \
            '/test_change_author_files/author_initials/20140824_jkn0.tex'
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
