from maya import cmds
import autoriggingWindow
import ThreadMaker
import wheelRigger

from autoriggingWindow import makeWindow as autoRigWindow
from ThreadMaker import makeWindow as threadWindow
from wheelRigger import makeWindow as wheelWindow

def createTab():
    cmds.menu( label='Heavy Duty Vehicle', tearOff=True, parent="MayaWindow" )
    cmds.menuItem( divider=True, dividerLabel='Full veehicle Rig' )
    cmds.menuItem( label='Vehicle Rigger', command="autoRigWindow()")
    cmds.menuItem( divider=True, dividerLabel='Bottom Rigging' )
    cmds.menuItem( label="Wheel Rigger", command="wheelWindow()")
    cmds.menuItem( label="Thread Maker", command="threadWindow()")


    '''
    cmds.menuItem( subMenu=True, label='Colors' )
    cmds.menuItem( label='Blue' )
    cmds.menuItem( label='Green' )
    cmds.menuItem( label='Yellow' )
    cmds.setParent( '..', menu=True )
    cmds.menuItem( divider=True, dividerLabel='Section 1' )
    cmds.radioMenuItemCollection()
    cmds.menuItem( label='Yes', radioButton=False )
    cmds.menuItem( label='Maybe', radioButton=False )
    cmds.menuItem( label='No', radioButton=True )
    cmds.menuItem( divider=True, dividerLabel='Section 2' )
    cmds.menuItem( label='Top', checkBox=True )
    cmds.menuItem( label='Middle', checkBox=False )
    cmds.menuItem( label='Bottom', checkBox=True )
    cmds.menuItem( divider=True )
    cmds.menuItem( label='Option' )
    cmds.menuItem( optionBox=True )
    '''

if __name__ == '__main__': createTab()