"""Autorigging tool Window

This script opens a window with different tabs that contain different
processes of the heavy duty vehicle rigging.

It imports each different files that are needed.
"""

from maya import cmds

import ThreadMaker as TM
reload(TM)

import wheelRigger as WM
reload(WM)

import ArmMaker as AM
reload(AM)

import finalizeRig as FR
reload(FR)

def makeWindow():
    """This function creates and displays a window"""

    # The window name to reference it later
    windowName="AutoRigger"
    
    # Close the window if it already exists
    if cmds.window(windowName, query=True, exists=True):
        cmds.deleteUI(windowName)

    # Create the window 
    cmds.window(windowName, title="Auto rigger tool for Heavy Duty Vehicle")

    # Create the UI elements (buttons, etc)
    populateWindow()
    
    # Display the window
    cmds.showWindow(windowName)
    
def populateWindow():
    """This function creates the UI elements that go inside the window"""

    # Create main form layout that will contain every tab
    form = cmds.formLayout()
    # Add tab layout to organize each part of the process
    tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
    cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )
    
    # Child tab for bottom rigging tool
    child1 = cmds.columnLayout()
    populateBottomTab()
    cmds.setParent( '..' )
    
    # Child tab for Arm rigging tool
    child2 = cmds.rowColumnLayout(numberOfColumns=2)
    populateArmTab()
    cmds.setParent( '..' )
    
    # Child tab for Pistons rigging tool
    child3 = cmds.rowColumnLayout(numberOfColumns=2, visible=False)
    cmds.setParent( '..' )
    
    # Child tab for Finalizing
    child4 = cmds.rowColumnLayout(numberOfColumns=2)
    populateFinalize()
    cmds.setParent( '..' )
    
    # Modify tab layout to add labels to each individual tab
    cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Bottom'), (child2, 'Arm'), (child3, 'Pistons'), (child4, 'Finalize')) )
    
def populateBottomTab():
    """This function creates the content of the first tab of the window"""

    # Add collection for radio buttons so only one option is selected at any time
    cmds.radioCollection()

    # Radio button to select the thread.
    # Lambda executes the speecified function passing 
    # the current value of the button (if its selected or not)
    cmds.radioButton(label="Tread", select=True, changeCommand=lambda value: changeThreadLayout(value))

    # Radio button to select the wheels.
    cmds.radioButton(label="Wheels", changeCommand=lambda value: changeWheelLayout(value))
    
    def changeThreadLayout(value):
        """This nested function changes the visibility for the thread maker's layout"""

        # layout allows editing any kind of layout with knowing its exact type (grid, column, row, etc)
        cmds.layout(threadLayout, edit=True, visible=value)
        
    def changeWheelLayout(value):
        """This nested function changes the visibility for the wheel maker's layout"""

        # layout allows editing any kind of layout with knowing its exact type (grid, column, row, etc)
        cmds.layout(wheelLayout, edit=True, visible=value)
    
    # Create layout for thread maker
    threadLayout = TM.populateWindow()

    # Create layout for wheel maker
    wheelLayout = WM.populateWindow()

    # Hide wheel layout first
    changeWheelLayout(False)
    
def populateArmTab():
    """This function creates the content of the second tab of the window"""

    armLayout = AM.populateWindow()

def populateFinalize():
    """This function creates the content of the final tab of the window"""

    finalizeLayout = FR.populateWindow()

# __name__ is a variable that all python modules have when executed
# When a python module is executed directly (pasting it on script editor,
# charcoal or through vsCode), the name is "__main__"
# When a python module is imported, the name is the name of the .py file
# or the alias assigned to it with "as" keyword
# This line specifies that makeWindow() function should only get called
# when running this module directly and not trough imports
if __name__ == "__main__": makeWindow()