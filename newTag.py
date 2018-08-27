#!/usr/bin/python
import sys, re
sys.path.append('database/')
sys.path.append('logic/')
import DiaryDatabaseWrapper, commonDiaryFunctions

# Add a tag to the tag database
def addTag2database(argv):
    """
        Add a tag to the database.
    """
    tag, tagTitle = validateInputs(argv)
    # Create a diary database object. If the diary database does not exist,
    # it will be created automatically.
    db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
    # Is the tag already in the database?
    tagRows = db.selectFromTable('tags',('name',),\
        'WHERE name=\'' + tag + '\'')
    if len(tagRows)>0:
        print("The tag '%s' has already been defined." % tag)
        sys.exit(2)
    # If not, add the tag to the database and close the database
    db.insertInTable('tags',('name', 'title'), (tag,tagTitle))
    db.close()
    print("The tag '%s' was successfully added to the database." % tag)
    
# Validate the input variables
def validateInputs(argv):
    """
        Validate the input variables
    """
    nInputs = len(argv)
    # Validate that 2 input variables are given
    if nInputs!=2:
        print("Error: You must specify 2 input parameters.")
        print("newTag.py tag \"tag title\"")
        sys.exit(2)
    # Ensure that a tag only contains the letter a-zA-Z and the number 0-9.
    tagNamePattern =  re.compile('^[a-zA-Z0-9]+$')
    if not re.match(tagNamePattern,argv[0]):
        print("Error: The tag can only consist of the characters a-zA-Z0-9.")
        sys.exit(2)
    return argv[0], argv[1]
    
if __name__ == '__main__':
    if sys.argv[1] == '--list' or sys.argv[1] == '-l':
        db = DiaryDatabaseWrapper.DiaryDatabaseWrapper()
        tagRows = db.selectFromTable('tags', ('name',), '')
        print('Create a new tag by e.g. ./newTag myTag')
        print('Known tags are:')
        for t in tagRows:
            print('  %s' % t[0])
    else:
        unicodedInputList = \
            commonDiaryFunctions.convertTerminalInputs2Unicode(sys.argv[1:])
        addTag2database(unicodedInputList)
