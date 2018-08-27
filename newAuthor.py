#!/usr/bin/python
import sys, re
sys.path.append('database/')
sys.path.append('logic/')
import DiaryDatabaseWrapper, commonDiaryFunctions

# Add an author to the author database
def addAuthor2database(argv):
    """
        Add an author to the database.
    """
    authorInitials, authorName, authorEmail = validateInputs(argv)
    # Create a diary database object. If the diary database does not exist,
    # it will be created automatically.
    db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
    # Is the author already in the database?
    authorRows = db.selectFromTable('authors',('initials',),\
        'WHERE initials=\'' + authorInitials + '\'')
    if len(authorRows)>0:
        print("The author '%s' has already been defined." % authorInitials)
        sys.exit(2)
    # If not, add the author to the database and close the database
    db.insertInTable('authors',('initials', 'name', 'email'), \
        (authorInitials, authorName, authorEmail))
    db.close()
    print("The author '%s (%s)' was successfully added to the database." \
        % (authorInitials, authorName))
    
# Validate the input variables
def validateInputs(argv):
    """
        Validate the input variables
    """
    nInputs = len(argv)
    # Validate that 2 input variables are given
    if nInputs!=3:
        print("Error: You must specify 3 input parameters.")
        print("newAuthors.py authorInitials \"name\" \"email\"")
        sys.exit(2)
    # Ensure that an author only contains the letter a-zA-Z and the number 0-9.
    authorInitialsPattern =  re.compile('^[a-zA-Z0-9]+$')
    if not re.match(authorInitialsPattern,argv[0]):
        print("Error: The author initials can only consist of the characters "\
            "a-zA-Z0-9.")
        sys.exit(2)
    return argv[0], argv[1], argv[2]
    
if __name__ == '__main__':
    unicodedInputList = \
        commonDiaryFunctions.convertTerminalInputs2Unicode(sys.argv[1:])
    addAuthor2database(unicodedInputList)
