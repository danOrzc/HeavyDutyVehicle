from maya import cmds
import logging

# Creating a logger for debug
logger = logging.getLogger("MenuTab")
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

def createTab():
    cmds.menu( label='Heavy Duty Vehicle', tearOff=True, parent="MayaWindow" )

    cmds.menuItem( divider=True, dividerLabel='Full vehicle Rig' )
    cmds.menuItem( label='Vehicle Rigger', command=lambda x: makeAutoriggingWindow() )

    cmds.menuItem( divider=True, dividerLabel='Bottom Rigging' )
    cmds.menuItem( label="Wheel Rigger", command=lambda x: makeWheelWindow() )
    cmds.menuItem( label="Thread Maker", command=lambda x: makeThreadWindow() )

    cmds.menuItem( divider=True, dividerLabel='Arm Rigging' )
    cmds.menuItem( label='Arm Rigger', command=lambda x: makeArmWindow() )

if __name__ == '__main__': createTab()