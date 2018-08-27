import unittest, os, sys, time, shutil
sys.path.append('../database')
sys.path.append('../logic')
import DiaryDatabaseWrapper

class TestDiaryDatabaseWrapper(unittest.TestCase):
    
    def setUp(self):
        # Move current database to a temporary file if it exists
        self.testDir = os.path.dirname(os.path.abspath(__file__))
        self.databaseFile = self.testDir + '/../database/diaryDatabase.db'
        self.databaseFileBackup = \
            self.testDir + '/../database/diaryDatabase.backup.db'
        if os.path.isfile(self.databaseFile):
            shutil.move(self.databaseFile,self.databaseFileBackup)
            
    def testDatabaseCreation(self):
        db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
        # Check that a new database file is created
        self.assertTrue(os.path.isfile(self.databaseFile))
        # Check that the correct tables have been created
        expTableNames = sorted(('tags','authors'))
        actTableNames = sorted(self.getTableNamesList())
        iTableName = 0
        for expTableName in expTableNames:
            self.assertTrue(expTableName == actTableNames[iTableName])
            iTableName = iTableName+1
        db.close()
        
        
    def testDatabaseInsertionSelection(self):
        db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
        # We test that we can insert into and select from the tags database
        tagName = 'testTag'
        tagTitle = 'This is a test'
        db.insertInTable('tags',('name', 'title'), (tagName,tagTitle))
        tagRows = db.selectFromTable('tags',('name', 'title'),'')
        self.assertTrue(tagName == tagRows[0][0])
        self.assertTrue(tagTitle == tagRows[0][1])
        # We test that we can insert into and select from the authors database
        authorInitials = 'jd'
        authorName = 'John Doe'
        authorEmail = 'john@doe.com'
        db.insertInTable('authors',('initials', 'name', 'email'), \
            (authorInitials, authorName, authorEmail))
        tagRows = db.selectFromTable('authors',('initials', 'name', 'email'),'')
        self.assertTrue(authorInitials == tagRows[0][0])
        self.assertTrue(authorName == tagRows[0][1])
        self.assertTrue(authorEmail == tagRows[0][2])
        db.close()
     
    def testDatabaseUpdating(self):
        db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
        tagName = 'testTag'
        tagTitle = 'This is a test'
        db.insertInTable('tags',('name', 'title'), (tagName,tagTitle))
        updatedTagTitle = 'This is an updated tag title'
        db.updateTable('tags',('title',),(updatedTagTitle,), \
            'name=\'' + tagName + '\'')
        tagRows = db.selectFromTable('tags',('title',),'')
        self.assertTrue(updatedTagTitle == tagRows[0][0])
        db.close()
        
    def testDatabaseDeletion(self):
        db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
        # Add an entry
        tagName = 'testTag'
        tagTitle = 'This is a test'
        db.insertInTable('tags',('name', 'title'), (tagName,tagTitle))
        tagRows = db.selectFromTable('tags',('title',),'')
        nEntriesBeforeDelete = len(tagRows)
        # Delete an entry
        db.deleteInTable('tags','name=\'' + tagName + '\'')
        tagRows = db.selectFromTable('tags',('title',),'')
        nEntriesAfterDelete = len(tagRows)
        self.assertTrue(nEntriesBeforeDelete-nEntriesAfterDelete==1)
        db.close()  
        
    def tearDown(self):
        # Restore the old database
        if os.path.isfile(self.databaseFileBackup):
            shutil.move(self.databaseFileBackup,self.databaseFile)
          
    # The functions below are not test functions
    def getTableNamesList(self):
        db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
        # Check that the correct tables have been created
        tableNames = db.selectFromTable('sqlite_master',('name',), \
            'WHERE type=\'table\'')
        db.close()
        return [tableName[0] for tableName in tableNames]
        
if __name__ == '__main__':
    unittest.main()
