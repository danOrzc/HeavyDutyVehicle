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

def makeArmWindow(*args):
    import ArmMaker
    if logger.level == logging.DEBUG:
        reload(ArmMaker)

    ArmMaker.makeWindow()

def emptyShelf(shelf):
    buttonList = cmds.shelfLayout(shelf, query=True, childArray=True)
    
    if buttonList:
        for i in xrange(len(buttonList)):
            cmds.deleteUI(buttonList[i])

        del buttonList[:]

def populateShelf(shelf):
    cmds.setParent(shelf)

    cmds.shelfButton(annotation='Create Full Vehicle',
        image='mayaIcon.png',
        command=makeAutoriggingWindow,
        parent=shelf 
        )
    cmds.shelfButton(annotation='Create Wheel Rig',
        image='mayaIcon.png', 
        command=makeWheelWindow,
        style='iconAndTextVertical',
        sic=True,
        parent=shelf 
        )
    cmds.shelfButton(annotation='Create Thread mesh and rig',
        image='mayaIcon.png',
        command=makeThreadWindow,
        parent=shelf 
        )
    cmds.shelfButton(annotation='Create Arm Rig',
        image='mayaIcon.png',
        command=makeArmWindow,
        parent=shelf 
        )

def createShelf():
    shelfName='HD_Vehicle'
    mel.eval('global string $gShelfTopLevel;')
    mainShelfLayout=mel.eval('$tmp=$gShelfTopLevel;')

    if not cmds.shelfLayout(shelfName,query=True, exists=True):
        createdShelf=mel.eval('addNewShelfTab "%s";'%shelfName)
    else:
        emptyShelf(shelfName)

    populateShelf(shelfName)    

if __name__ == '__main__': createShelf()