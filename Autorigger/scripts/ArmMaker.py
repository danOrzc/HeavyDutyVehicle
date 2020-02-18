"""Vehicle arm rigger.

This script creates a window that helps the user to rig
a mechanical arm.

"""

# Importing maya commands
from maya import cmds
import dataNodeManager
reload(dataNodeManager)

class ArmData(dataNodeManager.NodeData):
    """A class to save information for this rigging process.

    This class inherits from NodeData in dataNodeManager.py so we can access the node managing functions.

    Attributes
    ----------
    rootJoint : str
        The name of the joint on the top of the hierarchy
    rootController : str
        The name of the top controller that contains the IK Handles
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
        self.rootJoint = ""
        self.rootController = ""
        self.mainController = ""
        self.mainControllerGroup =""
        self.controllerAttributeName = "armControllers"
        self.controllerGroupAttributeName = "armControllerGroups"

# Create object of class to access attributes
data = ArmData()

def start():
    """This function initializes and saves the needed variables"""

    start.nameList = []           # List to save the different names of the locators (their numbers)
    start.locList = []            # List to save a reference to the locators themselves
    start.locPosList = []         # List to save each of the position of the locators
    start.jointList = []          # List to save a reference to each joint
    start.armsValue = 1           # Number of arms selected by the user

def makeWindow():
    """This function creates and displays the window"""

    name = "AutoRigger"     # The name for the window

    # Here we have the main UI for the rigger
    if cmds.window(name, query=True, exists=True):
        cmds.deleteUI(name)

    cmds.window(name)
   
    # Create UI elements
    populateWindow()

    cmds.showWindow()

def populateWindow():
    """This function creates the UI elements"""
    
    # Initialize variables
    start()

    # Create main grid layout
    mainLayout = cmds.gridLayout(numberOfColumns=1, cellWidth=500)

    cmds.text(align="left", font="boldLabelFont", label="Create locators to set the location of the joints")
    start.numArms=cmds.intSliderGrp(l="Arm pieces",min=1, max=6, v=4, f=True, cc=namingFor,
                                    statusBarMessage="The number of arm pieces. 1 for only a scoop. 3 for just arm. 4 for arm AND body", 
                                    annotation="The number of arm pieces. 1 for only a scoop. 3 for just arm. 4 for arm AND body")

    start.makeBttn = cmds.button(l="Make locators", c=makeLoc,
                                statusBarMessage="Create locators to choose the location of the joints", 
                                annotation="Create locators to choose the location of the joints")

    start.instText = cmds.text(align="left", font="boldLabelFont", l="")

    cmds.text(align="left", font="boldLabelFont", label="You can reset the locators positions")
    start.resetBttn = cmds.button(l="Reset locators", c=delLoc, enable=False)

    cmds.text(align="left", font="boldLabelFont", label="Click to place joints on locators")
    start.createJntsBttn = cmds.button(l="Place joints", c=makeJnt, enable=False)

    cmds.text(align="left", font="boldLabelFont", label="Select the mesh pieces from the body to the bucket")
    cmds.text(label="Please select each piece in order.")
    cmds.button(label="Assign Geometry", command=assignGeometry,
                statusBarMessage="Assign selected geometries to the joints", 
                annotation="Assign selected geometries to the joints")

    cmds.setParent( '..' )
    return mainLayout

def namingFor(*args):
    """This function queries the number of arms needed and uses it to save the names that the locators and joints will have"""

    # We query the value from the int slider and save it into the variable
    start.armsValue = cmds.intSliderGrp(start.numArms, q=True, v=True)
    # We iterate over this number
    for i in range(1, start.armsValue+2):
        # Save the index into the name list
        start.nameList.append(i)

def makeLoc(*args):
    """This function creates locators based on the number specified by the user"""

    # We query the number of arms given by the user
    start.armsValue = cmds.intSliderGrp(start.numArms, q=True, v=True)
    # We iterate over this number
    for i in range(1, start.armsValue+2):
        # We create a locator AND add it to the locator list
        start.locList.append(cmds.spaceLocator(n="ArmLocator%i"%i if i<=(start.armsValue) else "BucketLocator", p=(0,0,0), a=True))
        # Center locator's pivot
        cmds.CenterPivot()
        # Move locator in world space so the user does not have to deal with local space
        cmds.move(0,0,(i-1)*5)
    
    # Modifies the UI so the buttons get enabled or disabled
    updateUI(True)

def delLoc(*args):
    """This function deletes the locators and restarts the lists to redo the process"""

    # Iterate over the list of locators
    for i in start.locList:
        # Try to delete the locators
        try:
            # We delete each locator from the scene
            cmds.delete(i)
        except(ValueError):
            print "Locators have been deleted"

    # Empty the lists so we don't keep their references
    del start.locList[:]
    del start.locPosList[:]
    #del start.jointList[:]

    # Modifies the UI so the buttons get enabled or disabled
    updateUI(False)

def updateUI(hasLocators):
    """This function enables or disable buttons based on the existance of locators"""

    # Modify the make locators button so it is disable when there are locators
    cmds.button(start.makeBttn, e=True, enable=not hasLocators)

    # We enable the other buttons when we create locators
    cmds.button(start.resetBttn, e=True, enable=hasLocators)
    cmds.button(start.createJntsBttn, e=True, enable=hasLocators)

    # Write label for telling the user what to do
    if hasLocators:
        cmds.text(start.instText, e=True, l="Please move locators to their desired position IN ORDER")
    else:
        cmds.text(start.instText, e=True, l="")

def saveLoc():
    """This function saves the location of the locators"""
    # Iterate over the list of locators
    for i in start.locList:
        # Save their world positions
        xPos = cmds.getAttr("%s.translateX"%i[0])
        yPos = cmds.getAttr("%s.translateY"%i[0])
        zPos = cmds.getAttr("%s.translateZ"%i[0])

        # Add them to the list
        start.locPosList.append((xPos, yPos, zPos))

def makeJnt(*args):
    """This function creates a joint for each locator that was created"""

    # Get every position of the locators
    saveLoc()
    cmds.select(cl=True)
    # Create a joint on each locator position
    for count, i in enumerate(start.locPosList, start=1):
        jointName = "ArmJnt%i"%count if count<=len(start.locPosList)-1 else "BucketJnt"
        jointName = checkDuplicatedName(jointName)
        start.jointList.append(cmds.joint(n=jointName, p=i))
    
    # Select first joint on the chain
    cmds.select(start.jointList[0])
    data.rootJoint = start.jointList[0]

    # Change joint's orient
    cmds.joint(edit=True, oj="xyz", sao="yup", ch=True, zso=True)

    # Create IK handles on joints
    makeIK()

    # Delete list references
    delLoc()

    # Create a main controller
    makeMainController()

    # Save info to node
    data.writeToNode()

def makeIK(*args):
    """This function creates IK handles on the joints that were created"""

    # Create the IK handle that controls the bucket of the arm and save it to variable
    # We use SingleChaing solveer as we are creating IK on two joints only
    bucketIK = cmds.ikHandle(startJoint=start.jointList[-2], endEffector=start.jointList[-1], solver="ikSCsolver", sticky="sticky")[0]

    # Check if there is a controller with the same name, 
    # if there is, this function with generate a new one
    bucketName = checkDuplicatedName("bucketCtrl")

    # Create controller
    bucketCtrl = cmds.circle(name=bucketName, radius=2)[0]

    # Select both controller and IK
    cmds.select(bucketCtrl, bucketIK)

    # Move controller to IK
    cmds.MatchTranslation()

    # Select them reversed
    cmds.select(bucketIK, bucketCtrl)

    # Parent IK to bucker
    cmds.parent()

    # Save the name of the controller on data object
    data.rootController = bucketCtrl

    # If there are more than two arm pieces, we can create a second IK just for the arm
    if  start.armsValue > 2:

        # Create arm IK handle on the joint three indices from the last [-4] and the previous to last [-2]
        # In python [-1] represents the last index on a list
        # We use Rotate plane solver as we have a chain of three joints
        armIK = cmds.ikHandle(startJoint=start.jointList[-4], endEffector=start.jointList[-2], solver="ikRPsolver")[0]

        # Check if there is a controller with the same name, 
        # if there is, this function with generate a new one
        armName = checkDuplicatedName("armCtrl")

        # Create controller for this IK
        armCtrl = cmds.circle(name=armName, radius=2)[0]

        # Move controller to IK and parent them correctly
        cmds.select(armCtrl, armIK)
        cmds.MatchTranslation()
        cmds.select(armIK, armCtrl)
        cmds.parent()

        # Parent previous IK to this one
        cmds.select(bucketCtrl, armCtrl)
        cmds.parent()

        # Add reference to data object
        data.rootController = armCtrl

def makeMainController():
    """This function creates a MainController to drive the entire arm"""

    # Check if there is a controller with the same name, 
    # if there is, this function with generate a new one
    mainName = checkDuplicatedName("ArmMainController")

    # Create controller
    data.mainController = cmds.circle(name=mainName, radius=3, normal=(0,1,0))[0]

    # Create offset group
    data.mainControllerGroup = cmds.group(name="ArmMainControllerGroup")

    # Move group to root joint
    cmds.select(data.mainControllerGroup, data.rootJoint)
    cmds.MatchTranslation()

    # Parent joint and controller to this new MainController
    cmds.select(data.rootController, data.rootJoint, data.mainController)
    cmds.parent()
    

def assignGeometry(*args):
    """This function creates a parent contraint so the joints can control the geometry"""

    # List of selected transform objects
    pieces = cmds.ls(selection=True, transforms=True)

    # Iterate on the list of selected pieces
    # enumerate(list) returns both the index of the piece and the piece name itself
    # that's why we have two variables on the beginning of the loop,
    # one to save the index and other for the meshes
    for index, mesh in enumerate(pieces):

        # Select the joint that shares the same index as the mesh piece
        cmds.select(start.jointList[index], mesh)
        # Apply parent contraing between them
        cmds.parentConstraint(maintainOffset=True)

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