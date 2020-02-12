from maya import cmds

def populateWindow():
    mainLayout = cmds.columnLayout()

    cmds.textFieldButtonGrp("threadName", buttonLabel="Select Body Mesh", bc=pickingObj, placeholderText="Selected Mesh")

    cmds.button(label="Finalize Rig", command=finalizeRig, 
                statusBarMessage="Select all the wheels in one set. Then click the button", 
                annotation="Apply controls to selected wheel set")

    cmds.setParent("..")

    return mainLayout

def pickingObj(*args):
    selectedObj=cmds.ls(selection=True, objectsOnly=True)[0]
    cmds.textFieldButtonGrp("threadName", edit=True, text=selectedObj)

def finalizeRig(*args):
    # Create main controller
    mainCtrl = cmds.circle(name="MainController", normal=(0,1,0), radius=10)[0]
    # Create group for all controllers
    mainGrp = cmds.group(name="ControllerGroup")
    # Select groups of wheels
    cmds.select("WheelCTSet*", mainGrp)
    # Parent to main group
    cmds.parent()

    bodyMesh = cmds.textFieldButtonGrp("threadName", query=True, text=True)

    # Create circle for body
    bodyCtrl = cmds.circle(name="BodyController", normal=(0,1,0), radius=5)[0]
    cmds.select(bodyCtrl, bodyMesh)
    cmds.MatchTranslation(mo=True)
    cmds.FreezeTransformations()

    cmds.select("armCtrl", bodyCtrl)
    cmds.parent()

    cmds.select("ArmJnt1", bodyCtrl)
    cmds.parent()

    cmds.select(bodyCtrl, bodyMesh)
    cmds.parentConstraint()

    # Select groups of wheels
    cmds.select(bodyCtrl, mainCtrl)
    # Parent to main group
    cmds.parent()

    # Select groups of wheels
    cmds.select("ClusterControlGroup*", mainCtrl)
    # Parent to main group
    cmds.parent()
