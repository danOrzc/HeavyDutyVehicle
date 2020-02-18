"""Script for creating a wheel rig

This tool takes a number of shapes and add a rig for them to
act as a wheel.

"""

from maya import cmds
import dataNodeManager
reload(dataNodeManager)

class WheelData(dataNodeManager.NodeData):
    """A class to save information for this rigging process.

    This class inherits from NodeData in dataNodeManager.py so we can access the node managing functions.

    Attributes
    ----------
    wheelGroup : str
        The name of the group that contains the wheel meshes
    mainController : str
        The name of the main nurbs curve that controls the rig
    mainControllerGroup : str
        The name of the group where the mainController is
    controllerAttributeName : str
        The name of the type of rig that is saved (i.e. wheelControllers, treadControllers, armControllers)
    controllerGroupAttributeName : str
        The name of the type of rig GROUP that is saved (i.e. wheelControllerGroups, treadControllerGroups, armControllerGroups)

    Methods
    -------
    writeToNode() Inherited
        Takes the rigging info and stores it in a node
    
    """
    def __init__(self):
        self.wheelGroup = ""
        self.mainController = ""
        self.mainControllerGroup = ""
        self.controllerAttributeName = "wheelControllers"
        self.controllerGroupAttributeName = "wheelControllerGroups"
    
data = WheelData()

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
    mainLayout = cmds.frameLayout(label="Wheel rigger", width=500)

    # A float slider that will keep the desired speed for the rotation
    makeWindow.RotSpeed = cmds.floatSliderGrp(label="Wheel Speed", field=True, value=1)

    # Setting the columns to 3 so the buttons can be centered
    # - separator - button - separator
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(150,200,150))
    cmds.separator(width=150, style="none")
    # The button to initialize the rig process
    cmds.button(label="Wheel Controls", command=wheelSelection, 
                statusBarMessage="Select all the wheels in one set. Then click the button", 
                annotation="Apply controls to selected wheel set",
                width=200)
    cmds.separator(width=150, style="none")
    # Get out of rowLayout
    cmds.setParent("..")

    # Exit the main layout
    cmds.setParent("..")

    # Return a reference to layout to use it later
    return mainLayout

def wheelSelection(*args):
    """This functiion groups the wheels and adds a locator to control their rotation"""

    # Get the list of selected objects
    wheelSet = cmds.ls(selection=True)
    
    # Group the selected objects
    data.wheelGroup = cmds.group(name="WheelsGroup")
    # Create locator controller
    locatorName = checkDuplicatedName("WheelsController")
    data.mainController = cmds.spaceLocator(name=locatorName)[0]

    cmds.scale(4.0,4.0,4.0)

    data.mainControllerGroup = cmds.group(name="WheelsControllerGroup")
    
    # Align locator to group
    cmds.select(data.wheelGroup, add=True)
    cmds.align(xAxis="mid", yAxis="max", zAxis="mid", alignToLead=True)
    cmds.select(data.mainController)

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
        myExpression = cmds.expression(name="WheelSetRotation", string="{}.rotateX = {}.translateZ*{}".format(wheel, data.mainController, rotationSpeed))
        cmds.parentConstraint(data.mainController, wheel, maintainOffset=True, skipRotate="x")

    data.writeToNode()

def checkDuplicatedName(name):
    """This function checks if a name is duplicated in the scene, if it does, it generates a new one
    
    Parameters
    ----------
    name : str
        The name to verify in the scene
    """

    # The amount of times that we have found the name
    tries = 0

    # While there is an object with the same name
    while(cmds.objExists(name)):
        # Increment the number of tries
        tries +=1
        # Generate new name
        name = renameDuplicatedObject(name, tries)
    
    # Return the name
    return name

def renameDuplicatedObject(name, index=0):
    """This function takes a name and adds an index to it
    
    Parameters
    ----------
    name : str
        The name to append an index
    index : int
        The desired number to append to the name
    """

    # If the object exists on the scene
    if cmds.objExists(name):

        # Create a new name based on previous
        newName = name

        # Variable to save the number of digits the number should have
        lastDigits = 0

        # If we are not on index 0
        if index > 1:
            # The number of digits is based on the number of digits that the index has
            lastDigits = len(str(index))

            # Delete that number of digits from the name
            # Using [fromIndex:toIndex] allows us to create a substring out of the string
            # the parameters specify from where to where we want to sample that substring
            # as we are using negative index, we are leaving the last characters on the string
            # behind, as [-1] is the last index on a string
            newName = newName[:-lastDigits]
        
        # Append index to name
        newName += str(index)
        # Return the new name
        return newName

    # If the object does not exist on the scene, simply return the original name
    else:
        return name

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