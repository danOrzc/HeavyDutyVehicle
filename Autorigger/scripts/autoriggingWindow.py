from maya import cmds

import ThreadMaker as TM
reload(TM)

import wheelRigger as WM
reload(WM)

def makeWindow():
    windowName="AutoRigger"
    
    if cmds.window(windowName, query=True, exists=True):
        cmds.deleteUI(windowName)
        
    cmds.window(windowName, title="Auto rigger tool for Heavy Duty Vehicle")
    
    populateWindow()
    
    cmds.showWindow(windowName)
    
def populateWindow():
    # Create main form layout that will contain every tab
    form = cmds.formLayout()
    # Add tab layout to organize each part of the process
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    
    # Child tab for bottom rigging tool
    child1 = cmds.rowColumnLayout(numberOfColumns=2)
    populateBottomTab()
    cmds.setParent( '..' )
    
    # Child tab for Arm rigging tool
    child2 = cmds.rowColumnLayout(numberOfColumns=2)
    populateThreadTab()
    cmds.setParent( '..' )
    
    # Child tab for Pistons rigging tool3
    child3 = cmds.rowColumnLayout(numberOfColumns=2)
    cmds.setParent( '..' )
    
    # Child tab for Finalizing
    child4 = cmds.rowColumnLayout(numberOfColumns=2)
    cmds.setParent( '..' )
    
    # Modify tab layout to add labels to each individual tab
    cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Bottom'), (child2, 'Arm'), (child3, 'Pistons'), (child4, 'Finalize')) )
    
def populateBottomTab():
    # Add collection for radio buttons so only one option is selected at any time
    cmds.radioCollection()

    cmds.radioButton(label="Tread", select=True, changeCommand=lambda value: changeThreadLayout(value))
    cmds.radioButton(label="Wheels", changeCommand=lambda value: changeWheelLayout(value))
    
    def changeThreadLayout(value):
        cmds.columnLayout(threadLayout, edit=True, enable=value)
        
    def changeWheelLayout(value):
        cmds.columnLayout(wheelLayout, edit=True, enable=value)
        
    threadLayout = TM.populateWindow()
    wheelLayout = WM.populateWindow()
    changeWheelLayout(False)
    
def populateThreadTab():
    pass

# Chech if we are running this script from this same module
if __name__ == "__main__": makeWindow()