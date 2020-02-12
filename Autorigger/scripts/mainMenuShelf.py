"""Maya Shelf Creator

This script creates a Shelf in Maya's window.
If the shelf already exists, it deletes the old buttons and creates
new ones.

This tab contains buttons which open different our different windows
for the tools that we developed.

This file can also be imported as a module and contains the following
functions:

    * createShelf - creates the shelf
"""

from maya import mel
from maya import cmds
import logging

# Creating a logger for debug
logger = logging.getLogger("MenuShelf")
logger.setLevel(logging.DEBUG)  # Allows us to see debug messages, change to INFO to hide

def __makeAutoriggingWindow(*args):
    """Loads the autoriggingWindow module and creates a window out of it."""
    import autoriggingWindow

    # We can set to DEBUG to reload the module each time we run the code
    if logger.level == logging.DEBUG:
        reload(autoriggingWindow)

    # Create AutoRigging Window
    autoriggingWindow.makeWindow()

def __makeWheelWindow(*args):
    """Loads the wheelRigger module and creates a window out of it."""
    import wheelRigger

    # We can set to DEBUG to reload the module each time we run the code
    if logger.level == logging.DEBUG:
        reload(wheelRigger)

    #  Create Wheel window
    wheelRigger.makeWindow()

def __makeThreadWindow(*args):
    """Loads the ThreadMaker module and creates a window out of it."""
    import ThreadMaker

    # We can set to DEBUG to reload the module each time we run the code
    if logger.level == logging.DEBUG:
        reload(ThreadMaker)

    # Create thread window
    ThreadMaker.makeWindow()

def __makeArmWindow(*args):
    """Loads the ArmMaker module and creates a window out of it."""
    import ArmMaker

    # We can set to DEBUG to reload the module each time we run the code
    if logger.level == logging.DEBUG:
        reload(ArmMaker)

    # Create Arm window
    ArmMaker.makeWindow()

def __emptyShelf(shelf):
    """This function deletes all the buttons inside the shelf"""
    buttonList = cmds.shelfLayout(shelf, query=True, childArray=True)
    
    if buttonList:
        for i in xrange(len(buttonList)):
            cmds.deleteUI(buttonList[i])

        del buttonList[:]

def __populateShelf(shelf):
    """This function creates the buttons on the shelf"""

    # Shelf button for full vehicle rigging
    cmds.shelfButton(annotation='Create Full Vehicle',
        image='mayaIcon.png',
        command=__makeAutoriggingWindow,
        parent=shelf 
        )
    
    # Shelf button for wheel rig
    cmds.shelfButton(annotation='Create Wheel Rig',
        image='mayaIcon.png', 
        command=__makeWheelWindow,
        style='iconAndTextVertical',
        sic=True,
        parent=shelf 
        )
    
    # Shelf button for thread creation
    cmds.shelfButton(annotation='Create Thread mesh and rig',
        image='mayaIcon.png',
        command=__makeThreadWindow,
        parent=shelf 
        )
    
    # Shelf button for arm rig
    cmds.shelfButton(annotation='Create Arm Rig',
        image='mayaIcon.png',
        command=__makeArmWindow,
        parent=shelf 
        )

def createShelf():
    """This function creates a shelf in Maya"""
    shelfName='HD_Vehicle'

    # If the shelf doesn't exist, create it
    if not cmds.shelfLayout(shelfName,query=True, exists=True):
        # Execute mel command to create shelf
        createdShelf=mel.eval('addNewShelfTab "%s";'%shelfName)
    else:
        # If it exists, make it empty
        __emptyShelf(shelfName)

    # Create shelf buttons
    __populateShelf(shelfName)    

# __name__ is a variable that all python modules have when executed
# When a python module is executed directly (pasting it on script editor,
# charcoal or through vsCode), the name is "__main__"
# When a python module is imported, the name is the name of the .py file
# or the alias assigned to it with "as" keyword
# This line specifies that createShelf() function should only get called
# when running this module directly and not trough imports
if __name__ == '__main__': createShelf()