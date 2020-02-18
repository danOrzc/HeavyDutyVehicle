"""Autorigging tool Window

This script opens a window with different tabs that contain different
processes of the heavy duty vehicle rigging.

It imports each different files that are needed.
"""

from maya import cmds
import os

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
    # If it was closed, reset its prefs so it appears on default location
    elif cmds.windowPref(windowName, exists=True):
        cmds.windowPref(windowName, remove=True)

    # Create the window 
    cmds.window(windowName, title="Auto rigger tool for Heavy Duty Vehicle", sizeable=False)
    cmds.window(windowName, edit=True, width=500)

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
    
    # Child tab for Finalizing
    child3 = cmds.rowColumnLayout(numberOfColumns=2)
    populateFinalize()
    cmds.setParent( '..' )
    
    # Modify tab layout to add labels to each individual tab
    cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Bottom'), (child2, 'Arm'), (child3, 'Finalize')) )
    
def populateBottomTab():
    """This function creates the content of the first tab of the window"""

    cmds.separator(height=20, style="none")

    # Row Layout for the iconButtons and labels
    # Setting the columns to 5 so the labels can be centered
    cmds.rowLayout(numberOfColumns=5, columnWidth5=(100,100,100,100,100))

    # - separator - label - separator - label - separator
    cmds.separator(width=100, style="none")
    cmds.text(label="Build tread")
    cmds.separator(width=100, style="none")
    cmds.text(label="Wheel rigger")
    cmds.separator(width=100, style="none")

    # Get out of rowLayout
    cmds.setParent("..")

    #cmds.gridLayout(theGrid, e=True, cellHeight=100)
    cmds.rowLayout(numberOfColumns=5, columnWidth5=(100,100,100,100,100))
    cmds.separator(width=100, style="none")

    # Getting the path to the icons folder
    # __file__ is a variable that saves the location of .py file on disk
    iconPath = os.path.split(__file__)[0]

    # Using split to get rid of the name of the .py file and keep only the folders
    iconPath = os.path.split(iconPath)[0]

    # Using join to append a folder path without messing with operative system individualities
    iconPath = os.path.join(iconPath, "icons")

    # Append the name of the icon file
    treadIcon = os.path.join(iconPath, "tread.png")

    # Create button with icon
    cmds.iconTextButton(image=treadIcon, style="iconOnly", width=100, height=100, command=lambda:alternateLayout(True),
                        annotation="Choose this option to change to Tread Creation panel",
                        statusBarMessage="Choose this option to change to Tread Creation panel")

    cmds.separator(width=100, style="none")
    
    # Append icon's name
    wheelIcon = os.path.join(iconPath, "wheels.png")

    # Create button with icon
    cmds.iconTextButton(image=wheelIcon, style="iconOnly", width=100, height=100, command=lambda:alternateLayout(False),
                        annotation="Choose this option to change to Wheel Rigging panel",
                        statusBarMessage="Choose this option to change to Wheel Rigging panel")

    cmds.separator(width=100, style="none")

    # Get out of tbe row layout
    cmds.setParent("..")

    def alternateLayout(value):
        """This nested function changes the visibility for the thread maker's layout
        
        Parameters
        ----------
        value : bool
            When value is True, it will display the tread Layout. When False, it will show Wheel Layout
        """

        # layout allows editing any kind of layout with knowing its exact type (grid, column, row, etc)
        cmds.layout(threadLayout, edit=True, visible=value)
        # layout allows editing any kind of layout with knowing its exact type (grid, column, row, etc)
        cmds.layout(wheelLayout, edit=True, visible=not value)
    
    # Create layout for thread maker
    threadLayout = TM.populateWindow()

    # Create layout for wheel maker
    wheelLayout = WM.populateWindow()

    # Hide wheel layout first
    alternateLayout(True)
    
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