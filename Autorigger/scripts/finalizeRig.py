"""Vehicle rig finalizer script.

This script has functions that take the results of the previous
steps of the rigging process and puts them together.

This tool makes sure that the controllers are correctly
parented in the outliner.
"""

from maya import cmds
import os
import webbrowser

def populateWindow():
    """This function creates the UI elements for finalizing the rig"""

    mainLayout = cmds.columnLayout()

    # RowLayout for the icons
    iconPath = os.path.split(__file__)[0]
    iconPath = os.path.split(iconPath)[0]
    iconPath = os.path.join(iconPath, "icons")
    eagleIcon = os.path.join(iconPath, "mightyEagle.png")
    cmds.iconTextButton(image=eagleIcon, style="iconOnly", width=100, height=100, command=theEagle)

    cmds.textFieldButtonGrp("bodyName", buttonLabel="Select Body Mesh", bc=pickingObj, placeholderText="Selected Mesh")

    cmds.button(label="Finalize Rig", command=finalizeRig, 
                statusBarMessage="Select all the wheels in one set. Then click the button", 
                annotation="Apply controls to selected wheel set")

    cmds.setParent("..")

    return mainLayout

def pickingObj(*args):
    """This function saves a reference to the object that will be used as the rig's body"""

    selectedObj=cmds.ls(selection=True, objectsOnly=True)[0]
    cmds.textFieldButtonGrp("bodyName", edit=True, text=selectedObj)

def finalizeRig(*args):
    """This function is in charge of putting together the previous rig parts"""

    # Create main controller
    mainCtrl = cmds.circle(name="MainController", normal=(0,1,0), radius=10)[0]
    # Create group for all controllers
    mainGrp = cmds.group(name="ControllerGroup")
    # Select groups of wheels
    cmds.select("WheelCTSet*", mainGrp)
    # Parent to main group
    cmds.parent()
    
    cmds.select(mainCtrl, "WheelCTSet1")
    cmds.parentConstraint(mo=True)

    bodyMesh = cmds.textFieldButtonGrp("bodyName", query=True, text=True)

    # Create circle for body
    bodyCtrl = cmds.circle(name="BodyController", normal=(0,1,0), radius=5)[0]
    cmds.select(bodyCtrl, bodyMesh)
    cmds.MatchTranslation()
    cmds.FreezeTransformations()

    cmds.select("armCtrl", bodyCtrl)
    cmds.parent()

    cmds.select("ArmJnt1", bodyCtrl)
    cmds.parent()

    cmds.select(bodyCtrl, bodyMesh)
    cmds.parentConstraint(mo=True)

    # Select groups of wheels
    cmds.select(bodyCtrl, mainCtrl)
    # Parent to main group
    cmds.parent()

    # Select groups of wheels
    cmds.select("ClusterControlGroup*", mainCtrl)
    # Parent to main group
    cmds.parent()

    # Expression to drive thread with locator
    myExpression = cmds.expression(name="ThreadSetRotation", string="ThreadCurveBaseWire.rotateX = WheelCTSet1.translateZ*{}".format( -50))

def theEagle(*args):
    # open a connection to a URL using urllib2
    webbrowser.open("https://www.youtube.com/watch?v=IQnsREsChWs")