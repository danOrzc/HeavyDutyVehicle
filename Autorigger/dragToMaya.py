"""Maya module configuration

This file configures the tool's module.
- It gets the userAppDir to get Maya's directory
- It looks into that directory to see if it has a modules folder
- If it doesn't, it creates it
- Inside the modules folder, it creates a .mod file
- The .mod file includes the path to the tool's scripts folder

By doing this, Maya now recognizes the module's scripts folder and 
is able to import Python modules from it.
"""

import os
from maya import cmds

# Get user's maya folder
USERAPPDIR = cmds.internalVar(userAppDir=True)

# Append modules folder
# Using os.path.join so the path gets appended correctly
# no matter what Operative System the user has
# as some os' use "/" and others "\" to separate folders
DIRECTORY = os.path.join(USERAPPDIR, 'modules')

# The name for the module configuration file
MODFILE = 'MightyEagles.mod'

def __createFile(directory = DIRECTORY):
    """This function creates a new .mod file in the specified directory"""

    # Append the name of the file to the path created
    filePath = os.path.join(directory, MODFILE)

    # Get the folder where this .py file is saved
    # os.path.split() returns a tuple with two elements
    # element [0] has the path except for what comes
    # after the last slash.
    # element [1] is just the final part of the path,
    # in this case just the name of the .py
    modPath = os.path.split(__file__)[0]

    # os.path.basename returns the last part of the path
    # In this case, the name of the folder in which this
    # .py file is saved
    foldername = os.path.basename(modPath)

    # Try to open the file, if it doesn't exist, it will create it
    logfile = open(filePath, 'w')
    # Write the module info, it must include its name, version and it's path
    logfile.write('+ {myModule} {version} {path}'.format(myModule=foldername, version=1.0, path=modPath))
    # Close the file
    logfile.close()

def __createDirectory(directory = DIRECTORY):
    """This function creates a folder in the directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.mkdir(directory)

def __setUpModules():
    """This function is in charge of the module setup"""
    # Verify there is a modules folder
    __createDirectory()
    # Create/write .mod file
    __createFile()
    # Show confirmation dialog to user
    cmds.confirmDialog( title='Confirm', message='Module installed, please restart Maya')

def onMayaDroppedPythonFile(*args):
    """This function was added in Maya 2018 and it gives a warning if we don't implement it"""
    pass

# Call the function for setting up the modules
__setUpModules()