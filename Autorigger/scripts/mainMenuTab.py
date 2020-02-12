"""Maya Window Tab Creator

This script creates a Tab that is parented to the main Maya window.
If the tab already exists, it gets deleted and a new one is created.

This tab contains buttons which open different our different windows
for the tools that we developed.

This file can also be imported as a module and contains the following
functions:

    * createTab - creates and attaches the Tab to maya's window
"""

from maya import cmds
import logging

# Creating a logger for debug
logger = logging.getLogger("MenuTab")

# Allows us to see debug messages, change to INFO to skip
logger.setLevel(logging.DEBUG)  

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

def __populateTab(menu):
    """Fills the tab with the desired buttons."""

    # Create "Full Vehicle" section in the menu
    cmds.menuItem( divider=True, dividerLabel='Full vehicle Rig' )
    cmds.menuItem( label='Vehicle Rigger', command=__makeAutoriggingWindow )

    # Create "Bottom" (wheels/thread) section in the menu
    cmds.menuItem( divider=True, dividerLabel='Bottom Rigging' )
    cmds.menuItem( label="Wheel Rigger", command=__makeWheelWindow )
    cmds.menuItem( label="Thread Maker", command=__makeThreadWindow )

    # Create "Arms" section in the menu
    cmds.menuItem( divider=True, dividerLabel='Arm Rigging' )
    cmds.menuItem( label='Arm Rigger', command=__makeArmWindow )

def createTab():
    """Creates a tab menu that is attached to the MayaWindow"""
    menuName = "HeavyDuty"

    # If the menu already exists, delete it
    if cmds.menu(menuName, query=True, exists=True):
        cmds.deleteUI(menuName)

    # Create menu attached to MayaWindow
    cmds.menu( "HeavyDuty", label='Heavy Duty Vehicle', tearOff=True, parent="MayaWindow" )
    # Create buttons on it
    __populateTab(menuName)

# __name__ is a variable that all python modules have when executed
# When a python module is executed directly (pasting it on script editor,
# charcoal or through vsCode), the name is "__main__"
# When a python module is imported, the name is the name of the .py file
# or the alias assigned to it with "as" keyword
# This line specifies that createTab() function should only get called
# when running this module directly and not trough imports
if __name__ == '__main__': createTab()