# Importing maya commands
from maya import cmds

# Declaring global variables to be used accross different functions
name = "AutoRigger"     # The name for the window
nameList = []           # List to save the different names of the locators (their numbers)
locList = []            # List to save a reference to the locators themselves
locPosList = []         # List to save each of the position of the locators
jointList = []          # List to save a reference to each joint
armsValue = 1           # Number of arms selected by the user

# Here we have the main UI for the rigger
if cmds.window(name, query=True, exists=True):
    cmds.deleteUI(name)

cmds.window(name)
# Create grid layout
cmds.gridLayout(nc=1, cw=300)
cmds.text("Arm rigging process 001: The Arm")
numArms=cmds.intSliderGrp(l="Arm pieces",min=1, max=6, v=1, f=True, cc="namingFor()")

makeBttn = cmds.button(l="Make locators", c="makeLoc()")

instText = cmds.text(l="")

resetBttn = cmds.button(l="Reset locators", c="delLoc()", enable=False)
createJntsBttn = cmds.button(l="Place joints", c="makeJnt()", enable=False)
cmds.showWindow()

# The functions
def namingFor():
    # We query the value from the int slider and save it into the variable
    armsValue = cmds.intSliderGrp(numArms, q=True, v=True)
    # We iterate over this number
    for i in range(1, armsValue+2):
        # Save the index into the name list
        nameList.append(i)

def makeLoc():
    # We query the number of arms given by the user
    armsValue = cmds.intSliderGrp(numArms, q=True, v=True)
    # We iterate over this number
    for i in range(1, armsValue+2):
        # We create a locator AND add it to the locator list
        locList.append(cmds.spaceLocator(n="ArmLocator%i"%i if i<=(armsValue) else "BucketLocator", p=(0,0,0), a=True))
        # Center locator's pivot
        cmds.CenterPivot()
        # Move locator in world space so the user does not have to deal with local space
        cmds.move(0,0,-(i-1)*5)
    
    # Modifies the UI so the buttons get enabled or disabled
    updateUI(True)

def delLoc():
    # Iterate over the list of locators
    for i in locList:
        # Try to delete the locators
        try:
            # We delete each locator from the scene
            cmds.delete(i)
        except(ValueError):
            print "Locators have been deleted"

    # Empty the lists so we don't keep their references
    del locList[:]
    del locPosList[:]
    del jointList[:]

    # Modifies the UI so the buttons get enabled or disabled
    updateUI(False)

# Function that enables and disables buttons
# hasLocators defines if the locators have been created
def updateUI(hasLocators):
    # Modify the make locators button so it is disable when there are locators
    cmds.button(makeBttn, e=True, enable=not hasLocators)

    # We enable the other buttons when we create locators
    cmds.button(resetBttn, e=True, enable=hasLocators)
    cmds.button(createJntsBttn, e=True, enable=hasLocators)

    # Write label for telling the user what to do
    if hasLocators:
        cmds.text(instText, e=True, l="Please move locators to their desired position IN ORDER")
    else:
        cmds.text(instText, e=True, l="")

def saveLoc():
    # Iterate over the list of locators
    for i in locList:
        # Save their world positions
        xPos = cmds.getAttr("%s.translateX"%i[0])
        yPos = cmds.getAttr("%s.translateY"%i[0])
        zPos = cmds.getAttr("%s.translateZ"%i[0])

        # Add them to the list
        locPosList.append((xPos, yPos, zPos))

def makeJnt():
    # Get every position of the locators
    saveLoc()
    cmds.select(cl=True)
    # Create a joint on each locator position
    for count, i in enumerate(locPosList, start=1):
        jointList.append(cmds.joint(n="ArmJnt%i"%count if count<=len(locPosList)-1 else "BucketJnt", p=i))
    
    # Select first joint on the chain
    cmds.select(jointList[0])
    # Change joint's orient
    cmds.joint(edit=True, oj="xyz", sao="yup", ch=True, zso=True)
