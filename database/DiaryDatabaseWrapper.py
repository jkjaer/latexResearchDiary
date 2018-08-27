import sqlite3, os.path, sys
sys.path.append('logic')
import commonDiaryFunctions

class DiaryDatabaseWrapper:
    """
        A simple wrapper class for the SQLite 3 diary database.
    """
    def __init__(self):
        databaseDir = \
            commonDiaryFunctions.unicodeDir(os.path.abspath(__file__))
        databaseName = 'diaryDatabase.db'
        databasePath = databaseDir + '/' + databaseName
        if not os.path.isfile(databasePath):
            # Create the database files and all tables
            self.connection = self.__connect(databasePath)
            self.__createTables()
        else:
            # Open a connection to the database
            self.connection = self.__connect(databasePath)
        # Support mapping access by column name and index, iteration, 
        # representation, equality testing and len().
        # http://docs.python.org/2/library/sqlite3.html#sqlite3.Row
        self.connection.row_factory = sqlite3.Row
        
    # Connect to a database
    def __connect(self,databasePath):
        """
            Connect to a database.
        """
        return sqlite3.connect(databasePath)

    # Create all tables in the database
    def __createTables(self):
        """
            Creates the diary database with the following tables.
            1) The tag table which contains the tags and the tag titles.
            2) The author table which contains the author initials and names.
        """
        self.__createTable('tags','id INTEGER PRIMARY KEY, \
            name TEXT, title TEXT')
        self.__createTable('authors','id INTEGER PRIMARY KEY, \
            initials TEXT, name TEXT, email TEXT')
        
    # Create a new table
    def __createTable(self, tableName, columnDefinition):
        """
            Create a table with name tableName. The column names and associated 
            data types are given as a list.
        """
        cursor = self.connection.cursor()
        sqlCommand = 'CREATE TABLE %s (%s);' % (tableName, columnDefinition)
        cursor.execute(sqlCommand)
        cursor.close()
            
    # Insert a row into a table
    def insertInTable(self,tableName,columnNamesList,valuesList):
        """
            Insert a row into a table.
        """
        cursor = self.connection.cursor()
        placeHolders = ','.join('?'*len(valuesList))
        columnNamesString = ','.join(columnNamesList)
        sqlCommand = '''INSERT INTO %s (%s) VALUES (%s)''' \
            % (tableName, columnNamesString, placeHolders)
        cursor.execute(sqlCommand,(valuesList))
        self.connection.commit()
        cursor.close()
                    
    # Select from table
    def selectFromTable(self,tableName,columnNamesList,conditions):
        """
            Select rows from a table.
        """
        cursor = self.connection.cursor()
        columnNamesString = ','.join(columnNamesList)
        sqlCommand = '''SELECT %s FROM %s %s''' \
            % (columnNamesString,tableName,conditions)
        cursor.execute(sqlCommand)
        results = cursor.fetchall()
        cursor.close()
        return results
        
    # Update table
    def updateTable(self,tableName,columnNamesList,newValuesList,conditions):
        """
            Update rows in the table.
        """
        cursor = self.connection.cursor()
        # Make a formatted update lists of the form nameA=?, ... nameY=?
        updateListString = \
            ', '.join([columnName + '=?' for columnName in columnNamesList])
        sqlCommand = '''UPDATE %s SET %s WHERE %s''' \
            % (tableName,updateListString,conditions)
        cursor.execute(sqlCommand,newValuesList)
        self.connection.commit()
        cursor.close()
        
    # Delete row(s) in the table
    def deleteInTable(self,tableName,conditions):
        """
            Delete row(s) in the table.
        """
        cursor = self.connection.cursor()
        sqlCommand = '''DELETE FROM %s WHERE %s''' \
            % (tableName,conditions)
        cursor.execute(sqlCommand)
        self.connection.commit()
        cursor.close()
            
    # Close the database
    def close(self):
        """
            Close the connection to the database
        """
        self.connection.close()
        
