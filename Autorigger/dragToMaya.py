import os
from maya import cmds

# Get user's maya folder
USERAPPDIR = cmds.internalVar(userAppDir=True)

# Append modules folder
DIRECTORY = os.path.join(USERAPPDIR, 'modules')

# The name for the module configuration
MODFILE = 'MightyEagles.mod'

# This function creates a new file in the specified directory
def createFile(directory = DIRECTORY):
    filePath = os.path.join(directory, MODFILE)
    modPath = os.path.split(__file__)[0]
    foldername = os.path.basename(modPath)

    logfile = open(filePath, 'w')
    logfile.write('+ {myModule} {version} {path}'.format(myModule=foldername, version=1.0, path=modPath))
    logfile.close()

# This function creates a folder in the directory if it doesn't exist
def createDirectory(directory = DIRECTORY):
    if not os.path.exists(directory):
        os.mkdir(directory)

# This function is in charge of the module setup
def setUpModules():
    createDirectory()
    createFile()
    cmds.confirmDialog( title='Confirm', message='Module installed, please restart Maya')

# Function available since Maya 2018. Maya shows a warning if we don't implement it
def onMayaDroppedPythonFile(*args):
    pass

# Call the function for setting up the modules
setUpModules()