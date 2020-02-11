from maya import mel
from maya import cmds
import logging

# Creating a logger for debug
logger = logging.getLogger("MenuShelf")
logger.setLevel(logging.DEBUG)  # Allows us to see debug messages, change to INFO to hide

def makeAutoriggingWindow(*args):
    import autoriggingWindow
    if logger.level == logging.DEBUG:
        reload(autoriggingWindow)

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

def createShelf():
    shelfName='HD_Vehicle'
    mel.eval('global string $gShelfTopLevel;')
    mainShelfLayout=mel.eval('$tmp=$gShelfTopLevel;')

    if cmds.shelfLayout(shelfName,exists=True):
        #mel.eval('deleteShelfTab "%s";'%shelfName))
        return

    #add new tab
    createdShelf=mel.eval('addNewShelfTab "%s";'%shelfName)

    cmds.shelfButton(annotation='Create Full Vehicle',
        image='mayaIcon.png',
        command=makeAutoriggingWindow,
        parent=createdShelf 
        )
    cmds.shelfButton(annotation='Create Wheel Rig',
        image='mayaIcon.png', 
        command=makeWheelWindow,
        style='iconAndTextVertical',
        sic=True,
        parent=createdShelf 
        )
    cmds.shelfButton(annotation='Create Thread mesh and rig',
        image='mayaIcon.png',
        command=makeThreadWindow,
        parent=createdShelf 
        ) 
        
if __name__ == '__main__': createShelf()