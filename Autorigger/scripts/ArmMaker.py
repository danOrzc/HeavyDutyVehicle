"""Vehicle arm rigger.

This script creates a window that helps the user to rig
a mechanical arm.

"""

# Importing maya commands
from maya import cmds

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
   
    populateWindow()

    cmds.showWindow()

def populateWindow():
    """This function creates the UI elements"""
    
    # Initialize variables
    start()

    # Create main grid layout
    mainLayout = cmds.gridLayout(nc=1, cw=300)

    cmds.text("Arm rigging process 001: The Arm")
    start.numArms=cmds.intSliderGrp(l="Arm pieces",min=1, max=6, v=1, f=True, cc=namingFor)

    start.makeBttn = cmds.button(l="Make locators", c=makeLoc)

    start.instText = cmds.text(l="")

    start.resetBttn = cmds.button(l="Reset locators", c=delLoc, enable=False)
    start.createJntsBttn = cmds.button(l="Place joints", c=makeJnt, enable=False)

    cmds.text(label="Select the mesh pieces from the body to the bucket")
    cmds.button(label="Assign Geometry", command=assignGeometry)

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
        cmds.move(0,0,-(i-1)*5)
    
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
        start.jointList.append(cmds.joint(n="ArmJnt%i"%count if count<=len(start.locPosList)-1 else "BucketJnt", p=i))
    
    # Select first joint on the chain
    cmds.select(start.jointList[0])
    # Change joint's orient
    cmds.joint(edit=True, oj="xyz", sao="yup", ch=True, zso=True)

    makeIK()

def makeIK(*args):
    """This function creates IK handles on the joints that were created"""

    bucketIK = cmds.ikHandle(startJoint=start.jointList[-2], endEffector=start.jointList[-1], sol="ikSCsolver", sticky="sticky")[0]
    bucketCtrl = cmds.circle(name="bucketCtrl")[0]

    cmds.select(bucketCtrl, bucketIK)
    cmds.MatchTranslation()
    cmds.select(bucketIK, bucketCtrl)
    cmds.parent()

    if  start.armsValue > 2:
        armIK = cmds.ikHandle(startJoint=start.jointList[0], endEffector=start.jointList[-2], sol="ikRPsolver")[0]
        armCtrl = cmds.circle(name="armCtrl")[0]

        cmds.select(armCtrl, armIK)
        cmds.MatchTranslation()
        cmds.select(armIK, armCtrl)
        cmds.parent()

        cmds.select(bucketCtrl, armCtrl)
        cmds.parent()

    delLoc()

def assignGeometry(*args):
    """This function creates a parent contraint so the joints can control the geometry"""
    pieces = cmds.ls(selection=True, transforms=True)

    for i,p in enumerate(pieces):
        cmds.select(start.jointList[i], p)
        cmds.parentConstraint(maintainOffset=True)
    
# __name__ is a variable that all python modules have when executed
# When a python module is executed directly (pasting it on script editor,
# charcoal or through vsCode), the name is "__main__"
# When a python module is imported, the name is the name of the .py file
# or the alias assigned to it with "as" keyword
# This line specifies that makeWindow() function should only get called
# when running this module directly and not trough imports
if __name__ == "__main__": makeWindow()