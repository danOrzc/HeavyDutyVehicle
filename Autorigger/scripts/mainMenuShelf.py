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
import os
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
    """This function deletes all the buttons inside the shelf
    
        Parameters
        ----------
        shelf : str
            The name of the shelf to empty
    """

    # Get a list of the buttons that are children of the shelf
    buttonList = cmds.shelfLayout(shelf, query=True, childArray=True)
    
    # If the list is valis (not empty), delete each button from it
    if buttonList:
        for i in xrange(len(buttonList)):
            cmds.deleteUI(buttonList[i])

        # Empty the list of buttons
        del buttonList[:]

def __populateShelf(shelf):
    """This function creates the buttons on the shelf
    
        Parameters
        ----------
        shelf : str
            The name of the shelf to add buttons to
    """

    # Creating a path to our icons folder
    # __file__ saves the path where the .py file is saved
    # using split function separates the path in two indexex
    # [0] is the start of the path and [1] is the last element (e.g. the deepest folder or the name of the file)
    # In this case, we are eliminating the name of the file
    iconPath = os.path.split(__file__)[0]

    # Get the top folder by deleting the last part of the path
    iconPath = os.path.split(iconPath)[0]

    # From that folder, append the icons folder
    iconPath = os.path.join(iconPath, "icons")

    # Append the name of the icon
    vehicleIcon = os.path.join(iconPath, "backhoeShelf.png")

    # Shelf button for full vehicle rigging
    cmds.shelfButton(annotation='Create Full Vehicle',
        image=vehicleIcon,
        command=__makeAutoriggingWindow,
        parent=shelf 
        )
    
    # Append the name of the icon
    wheelIcon = os.path.join(iconPath, "wheelShelf.png")

    # Shelf button for wheel rig
    cmds.shelfButton(annotation='Create Wheel Rig',
        image=wheelIcon, 
        command=__makeWheelWindow,
        style='iconAndTextVertical',
        sic=True,
        parent=shelf 
        )

    # Append the name of the icon
    treadIcon = os.path.join(iconPath, "treadShelf.png")
    
    # Shelf button for thread creation
    cmds.shelfButton(annotation='Create Thread mesh and rig',
        image=treadIcon,
        command=__makeThreadWindow,
        parent=shelf 
        )

    # Append the name of the icon
    armIcon = os.path.join(iconPath, "armShelf.png")
    
    # Shelf button for arm rig
    cmds.shelfButton(annotation='Create Arm Rig',
        image=armIcon,
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