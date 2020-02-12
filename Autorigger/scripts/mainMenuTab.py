from maya import cmds
import logging

# Creating a logger for debug
logger = logging.getLogger("MenuTab")
logger.setLevel(logging.DEBUG)  # Allows us to see debug messages, change to INFO to hide

def makeAutoriggingWindow(*args):
    """Loads the autoriggingWindow module and creates a window out of it."""
    import autoriggingWindow

    # We can set to DEBUG to reload the module each time we run the code
    if logger.level == logging.DEBUG:
        reload(autoriggingWindow)

    # Create AutoRigging Window
    autoriggingWindow.makeWindow()

def makeWheelWindow(*args):
    import wheelRigger
    if logger.level == logging.DEBUG:
        reload(wheelRigger)

    wheelRigger.makeWindow()

def makeThreadWindow(*args):
    import ThreadMaker
    if logger.level == logging.DEBUG:
        reload(ThreadMaker)

    ThreadMaker.makeWindow()

def makeArmWindow(*args):
    import ArmMaker
    if logger.level == logging.DEBUG:
        reload(ArmMaker)

    ArmMaker.makeWindow()

def restartTab(menu):
    cmds.menu( menu, edit=True, deleteAllItems=True )

def populateTab(menu):
    cmds.menuItem( divider=True, dividerLabel='Full vehicle Rig' )
    cmds.menuItem( label='Vehicle Rigger', command=lambda x: makeAutoriggingWindow() )

    cmds.menuItem( divider=True, dividerLabel='Bottom Rigging' )
    cmds.menuItem( label="Wheel Rigger", command=lambda x: makeWheelWindow() )
    cmds.menuItem( label="Thread Maker", command=lambda x: makeThreadWindow() )

    cmds.menuItem( divider=True, dividerLabel='Arm Rigging' )
    cmds.menuItem( label='Arm Rigger', command=lambda x: makeArmWindow() )

def createTab():
    menuName = "HeavyDuty"

    if cmds.menu(menuName, query=True, exists=True):
        cmds.deleteUI(menuName)

    cmds.menu( "HeavyDuty", label='Heavy Duty Vehicle', tearOff=True, parent="MayaWindow" )
    populateTab(menuName)

if __name__ == '__main__': createTab()