"""Vehicle rig finalizer script.

This script has functions that take the results of the previous
steps of the rigging process and puts them together.

This tool makes sure that the controllers are correctly
parented in the outliner.
"""

from maya import cmds
import os
import webbrowser
import dataNodeManager
reload(dataNodeManager)

class MainControllerData:
    """A class to save information for this rigging process"""

    def __init__(self):
        """Initialize atrributes"""

        self.mainController = ""
        self.mainGroup = ""

# Create an object of MainControllerData class to access information
data = MainControllerData()

def populateWindow():
    """This function creates the UI elements for finalizing the rig"""

    # Create main grid layout
    mainLayout = cmds.gridLayout(numberOfColumns=1, cellWidth=500, cellHeight=200)

    # Setting the columns to 3 so the buttons can be centered
    # - separator - button - separator
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(100,200,200), height=200)
    cmds.separator(width=100, style="none")
    cmds.button(label="Finalize Rig", command=finalizeRig, 
                statusBarMessage="Create vehicle's Main Controller and parent previous steps to it", 
                annotation="Create vehicle's Main Controller and parent previous steps to it",
                width = 200, height = 100)
    cmds.separator(width=200, style="none")

    # Get out of rowLayout
    cmds.setParent("..")

    # Building the path to the icon's folder
    # __file__ saves the path where this .py file is saved
    # we split the path so we can get rid of the last part of the path (the file name in this case)
    iconPath = os.path.split(__file__)[0]

    # we get rid of the last part again. in this case it is the scripts folder (we go up a level)
    iconPath = os.path.split(iconPath)[0]

    # append the icons folder
    iconPath = os.path.join(iconPath, "icons")

    # append the name of the icon
    eagleIcon = os.path.join(iconPath, "mightyEagle.png")

    # Setting the columns to 3 so the buttons can be centered
    # - separator - button - separator
    cmds.rowLayout(numberOfColumns=3, columnWidth3=(200,200,100), height=200)
    cmds.separator(width=200, style="none")
    cmds.iconTextButton(image=eagleIcon, style="iconOnly", width=200, height=200, command=theEagle)
    cmds.separator(width=100, style="none")

    # Get out of rowLayout
    cmds.setParent("..")
    
    # Get out of mainLayout
    cmds.setParent("..")

    return mainLayout

def pickingObj(*args):
    """This function saves a reference to the object that will be used as the rig's body"""

    selectedObj=cmds.ls(selection=True, objectsOnly=True)[0]
    cmds.textFieldButtonGrp("bodyName", edit=True, text=selectedObj)

def finalizeRig(*args):
    """This function is in charge of putting together the previous rig parts"""

    # If the main Controller doesn't exist, create it
    if not cmds.objExists("MainController"):

        # Create main controller and save the result name to the data object
        data.mainController = cmds.circle(name="MainController", normal=(0,1,0), radius=10)[0]

        # Change Main Controller's Color
        # First we tell that we want to override the color
        cmds.setAttr("{}Shape.overrideEnabled".format(data.mainController), 1)

        # Then we change the color type to RGB, instead of using Maya's predefined indices
        cmds.setAttr("{}Shape.overrideRGBColors".format(data.mainController), 1)

        # Build the color channel by channel
        cmds.setAttr("{}Shape.overrideColorR".format(data.mainController), 1)
        cmds.setAttr("{}Shape.overrideColorG".format(data.mainController), 1)
        cmds.setAttr("{}Shape.overrideColorB".format(data.mainController), 0)

        # Create group for all controllers and save it's name to the data object
        data.mainGroup = cmds.group(name="MainControllerGroup")
    
    # If the controller already exists, save their names to the data object
    else:
        data.mainController = "MainController"
        data.mainGroup = "MainControllerGroup"

    # If there is a node with the rigging data, we use it to retrieve the previous steps
    if cmds.objExists("rigDataNode"):

        # Parent treads to main controller
        parentRigControllers("treadControllers","treadControllerGroups")

        # Parent arms to main controller
        parentRigControllers("armControllers","armControllerGroups")

        # Parent wheels to main controller
        parentRigControllers("wheelControllers", "wheelControllerGroups")


def theEagle(*args):
    # open a link
    webbrowser.open("https://www.youtube.com/watch?v=IQnsREsChWs")

def parentMesh(*args):
    """This function looks for all the meshes on the scene and groups them together"""

    # List all objects of type mesh
    mesh = cmds.ls(type="mesh")

    # We got shape nodes, so now we list their parents to get transform nodes
    transforms = cmds.listRelatives(mesh, p=True, path=True)

    # Select all the transform nodes that have meshes
    cmds.select(transforms, r=True)
    
    # If the group already exists, parent them
    if cmds.objExists("VehicleMeshGroup"):
        cmds.parent("VehicleMeshGroup")

    # Else, create and group
    else:
        cmds.group(name="VehicleMeshGroup")

def parentRigControllers(controlAttributeName, groupAttributeName):
    """Parents the previous steps of the rigging process to the MainController

    It gets the data out of the rigData node, where the name of the controllers are saved.
    Then uses those names to parent them to the main Controller.
    
    Parameters
    ----------
    controlAttributeName : str
        The name of the attribute in the node that saves all the controllers previously created
    groupAttributeName : str
        The name of the attribute in that node that contains the offset groups for the controllers
    """

    # Get a list with all the controller names
    controllerData = dataNodeManager.getData(attributeName=controlAttributeName)

    # Get a list with all the group names
    controllerEmptyGroups = dataNodeManager.getData(attributeName=groupAttributeName)

    # If there are no controllers, delete the attributes to restart the node
    if not controllerData:
        dataNodeManager.deleteDataAttribute(attributeName=controlAttributeName)
        dataNodeManager.deleteDataAttribute(attributeName=groupAttributeName)
        return

    # For each controller in the controller List
    for controller in controllerData:

        # If the object does not exist (it was deleted), skip this step of the for loop
        if not cmds.objExists(controller):
            continue
        
        # Select the vehicle's main controller and the rig part controller
        cmds.select(data.mainController, controller)

        # Add a parent constraint
        cmds.parentConstraint(mo=True)

        # Select the rig part controller and the offset group of the MainController
        cmds.select(controller, data.mainGroup)

        # Parent them
        cmds.parent()

    # Delete the data for previous controllers so we don't try to parent them again
    dataNodeManager.deleteDataAttribute(attributeName=controlAttributeName)

    # Delete all the offset groups in the scene (now they are empty as we moved the controllers that were inside)
    for group in controllerEmptyGroups:
        if not cmds.objExists(group):
            dataNodeManager.deleteValue(attributeName=groupAttributeName,value=controller)
            continue
        cmds.delete(group)

    # Delete all group data from node
    dataNodeManager.deleteDataAttribute(attributeName=groupAttributeName)