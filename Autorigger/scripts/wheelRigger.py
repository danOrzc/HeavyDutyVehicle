from maya import cmds

locatorScale = 4.0

def makeWindow():
    windowName = "WheelMaker"
    if cmds.window(windowName, query=True, exists=True):
        cmds.deleteUI(windowName)
    cmds.window(windowName, title="Wheel Maker")
    cmds.window(windowName, edit=True, height=300, width=500)
    
    populateWindow()

    cmds.showWindow(windowName)

def populateWindow():
    mainLayout = cmds.columnLayout()

    makeWindow.RotSpeed = cmds.floatSliderGrp(field=True, value=1)
    
    cmds.button(label="Wheel Controls", command="wheelSelection()", 
                statusBarMessage="Select all the wheels in one set. Then click the button", 
                annotation="Apply controls to selected wheel set")

    cmds.button(label="Finalize", command="finale()")

    cmds.setParent("..")

    return mainLayout

def wheelSelection():
    print("Wheel Selection called")

    # Get the list of selected objects
    wheelSet = cmds.ls(selection=True)
    print(wheelSet)
    # Group the selected objects
    cmds.group(name="WheelsGroup")
    # Create locator controller
    locatorController = cmds.spaceLocator(name="WheelsCtrl")
    cmds.scale(locatorScale,locatorScale,locatorScale)
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
    
    rotationSpeed = cmds.floatSliderGrp(makeWindow.RotSpeed, q=True, v=True)

    for wheel in wheelSet:
        myExpression = cmds.expression(name="WheelSetRotation", string="{}.rotateX = WheelsCtrl.translateZ*{}".format(wheel, rotationSpeed))
        cmds.parentConstraint("WheelsCtrl", wheel, maintainOffset=True, skipRotate="x")
        print(wheel)

    renamingAssets()

def finale():
    cmds.circle(name="MainCT", radius=10, normal=(0,1,0))

    cmds.select("WheelCTSet*")
    theControllers = cmds.ls(sl=True, transforms=True)

    for controller in theControllers:
        cmds.parentConstraint("MainCT", controller, maintainOffset=True)

def renamingAssets():
    cmds.rename("WheelsCtrl", "WheelCTSet1")
    cmds.rename("WheelsGroup", "WheelG1")

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