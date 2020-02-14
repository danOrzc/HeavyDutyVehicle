"""Script for creating a wheel rig

This tool takes a number of shapes and add a rig for them to
act as a wheel.

"""

from maya import cmds

def makeWindow():
    """This function creates and displays a window"""

    # The name of the window to reference it later
    windowName = "WheelMaker"

    # If it is already open, close it
    if cmds.window(windowName, query=True, exists=True):
        cmds.deleteUI(windowName)

    # Create the window
    cmds.window(windowName, title="Wheel Maker")
    cmds.window(windowName, edit=True, height=300, width=500)
    
    # Add UI elements
    populateWindow()

    # Display the window
    cmds.showWindow(windowName)

def populateWindow():
    """This function add the UI elements to the window"""

    # Reference to our mainLayout to use it later
    mainLayout = cmds.columnLayout()

    # A float slider that will keep the desired speed for the rotation
    makeWindow.RotSpeed = cmds.floatSliderGrp(field=True, value=1)
    
    # The button to initialize the rig process
    cmds.button(label="Wheel Controls", command=wheelSelection, 
                statusBarMessage="Select all the wheels in one set. Then click the button", 
                annotation="Apply controls to selected wheel set")

    #cmds.button(label="Finalize", command=finale)

    # Exit the main layout
    cmds.setParent("..")

    # Return a reference to layout to use it later
    return mainLayout

def wheelSelection(*args):
    """This functiion groups the wheels and adds a locator to control their rotation"""

    print("Wheel Selection called")

    # Get the list of selected objects
    wheelSet = cmds.ls(selection=True)
    print(wheelSet)
    # Group the selected objects
    cmds.group(name="WheelsGroup")
    # Create locator controller
    locatorController = cmds.spaceLocator(name="WheelsCtrl")
    cmds.scale(4.0,4.0,4.0)
    # Align locator to group
    cmds.select("WheelsGroup", add=True)
    cmds.align(xAxis="mid", yAxis="max", zAxis="mid", alignToLead=True)
    cmds.select(locatorController)

    # *************************** Connection editor way *********************************
    # It is not ideal because there is no way to control the rotation speed
    '''
    for wheel in wheelSet:
        cmds.connectAttr("WheelsCtrl.tz", "{}.ry".format(wheel))
        '''
    
    # Get the speed from the slider
    rotationSpeed = cmds.floatSliderGrp(makeWindow.RotSpeed, q=True, v=True)

    # Add expression to control wheels
    for wheel in wheelSet:
        myExpression = cmds.expression(name="WheelSetRotation", string="{}.rotateX = WheelsCtrl.translateZ*{}".format(wheel, rotationSpeed))
        cmds.parentConstraint("WheelsCtrl", wheel, maintainOffset=True, skipRotate="x")

    renamingAssets()

def finale(*args):
    cmds.circle(name="MainCT", radius=10, normal=(0,1,0))

    cmds.select("WheelCTSet*")
    theControllers = cmds.ls(sl=True, transforms=True)

    for controller in theControllers:
        cmds.parentConstraint("MainCT", controller, maintainOffset=True)

def renamingAssets():
    """This function renames the created controllers"""

    cmds.rename("WheelsCtrl", "WheelCTSet1")
    cmds.rename("WheelsGroup", "WheelG1")

# __name__ is a variable that all python modules have when executed
# When a python module is executed directly (pasting it on script editor,
# charcoal or through vsCode), the name is "__main__"
# When a python module is imported, the name is the name of the .py file
# or the alias assigned to it with "as" keyword
# This line specifies that makeWindow() function should only get called
# when running this module directly and not trough imports
if __name__ == "__main__": makeWindow()
    
'''
expressionString = ""
for wheel in wheelSet:
    expressionString += "{}.rotateX = WheelsCtrl.translateZ\n".format(wheel)

myExpression = cmds.expression(name="WheelSetRotation", string=expressionString)
'''
'''
float $value = pSphere1.translateZ;
vector $number = `xform -q -os -t pSphere1`; 
pSphere2.myAttr = $number.z;
pSphere2.translateY = $number.z;
'''