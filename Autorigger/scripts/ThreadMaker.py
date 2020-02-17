"""This tool creates a window that allows the user to create a thank tread

"""

from maya import cmds
import dataNodeManager
reload(dataNodeManager)

class TreadData:
    def __init__(self):
        self.firstLocator = ""
        self.secondLocator = ""
        self.curveRadius = 0.0
        self.treadCircle = ""
        self.treadBaseWire = ""
        self.treadMesh = ""
        self.mainController = ""

    def writeToNode(self):
        dataNodeManager.saveData(attributeName="treadControllers", value=self.mainController)
    
data = TreadData()

# Function to create the main window UI
def makeWindow():
    """This function creates and displays a window"""

    winName = "TreadMaker"
    
    # Check if the window is already open
    if cmds.window(winName, query=True, exists=True):
        cmds.deleteUI(winName)
    # If it was closed, reset its prefs so it appears on default location
    elif cmds.windowPref(winName, exists=True):
        cmds.windowPref(winName, remove=True)
    
    # If it doesn't exist, make it    
    cmds.window(winName, title="Tread Maker and Rigger")
    cmds.window(winName, edit=True, width=500)
    cmds.window(winName, edit=True, topLeftCorner=[0,0])
    
    populateWindow()

    cmds.showWindow()

def populateWindow():
    """This function add the UI elements to the window"""

    # Main layout for UI
    mainLayout = cmds.columnLayout()
     
    '''
    ----------------------------------- Locator Creation -----------------------------------------
    '''
    
    cmds.frameLayout(label="Locators")
    cmds.text(label="This is the very first step on the process")
    cmds.gridLayout(numberOfColumns=1, cellWidth=500)
    
    cmds.button(label="Initialize", command=initFunc)
    
    cmds.separator(h=5)
    cmds.setParent('..')
    cmds.setParent('..')
    
    
    '''
    ----------------------------------- Circle Creation -----------------------------------------
    '''
    
    cmds.frameLayout(label="Curve")
    cmds.text(label="This is the second step on the process")
    cmds.gridLayout(numberOfColumns=1, cellWidth=500)
    cmds.intSliderGrp("curveQuality", l="Curve quality", f=True, v=6, minValue=6, maxValue=20)
    cmds.button(label="Make Curve", c=makeTread)
    
    cmds.separator(h=5)
    cmds.setParent('..')
    cmds.setParent('..')
    
    '''
    ----------------------------------- Tread Creation -----------------------------------------
    '''
    
    cmds.frameLayout(label="Making Tread")
    cmds.text(label="Now create the tread")
    
    def updateUI(value):
        """Nested function that updates the UI depending on the creation method"""

        # Update elements
        cmds.checkBox("useProxy",e=True, en=not value)
        cmds.checkBox("bboxCheck",e=True, en=not value)
        cmds.intSliderGrp("treadAmount",e=True, en=not value)
        
        # Make sure the text Field is enable when using the premade geo method
        if not value:
            proxyGeo = cmds.checkBox("useProxy", query=True, value=True)
            cmds.textFieldButtonGrp("treadName",e=True, en=not proxyGeo)
            usebbox = cmds.checkBox("bboxCheck", query=True, value=True)
            cmds.intSliderGrp("treadAmount",e=True, en=not usebbox)
        else:
            cmds.textFieldButtonGrp("treadName",e=True, en=value)
    
    # Radio Buttons for choosing between piece or whole mesh
    cmds.gridLayout(numberOfColumns=2, cellWidth=250)
    cmds.radioCollection()
    cmds.radioButton("premadeGeo", label="Previously created geometry", cc= lambda value: updateUI(value))
    cmds.radioButton(label="Make tread from a piece", select=True)
    cmds.setParent('..')
    
    # Layout for creation methods
    cmds.gridLayout("treadGridLO", numberOfColumns=1, cellWidth=500)
    cmds.checkBox("useProxy", label="Create Proxy Geo", cc= lambda value: cmds.textFieldButtonGrp("treadName",e=True, en=not value))
    cmds.textFieldButtonGrp("treadName", buttonLabel="Pick Selected", bc=pickingObj, placeholderText="Selected Mesh")
    cmds.checkBox("bboxCheck", label="Use piece's bounding box", cc= lambda value: cmds.intSliderGrp("treadAmount",e=True, en=not value))
    cmds.intSliderGrp("treadAmount", l="Amount of treads", f=True, v=20, minValue=1, maxValue=500, cc=RemakeTread)
    cmds.button(label="Make Tread", c=makeTreadObj)
    
    cmds.setParent('..')
    cmds.separator(h=5)
    cmds.text(label="Finalize before modifying the curve points")
    cmds.button(l="Finalize", c=finalizeTread)
    
    cmds.setParent('..')
    cmds.setParent('..')

    return mainLayout

def initFunc(*args):
    """This function creates the locators"""

    # Get user's selection
    selection = cmds.ls(selection=True, transforms=True)

    # Create and scale locators
    data.firstLocator = cmds.spaceLocator(name="CircleLocator001")[0]
    cmds.scale(4,4,4)
    data.secondLocator = cmds.spaceLocator(name="CircleLocator002")[0]
    cmds.scale(4,4,4)
    
    # If there was a selection, use it as bounding box for locators
    if selection:
        # Get dimensions
        # exactWorldBoundingBox command returns a list of values representing the limits of the object
        # [minXCoordinate, minYCoordinate, minZCoordinate, maxXCoordinate, maxYCoordinate, maxZCoordinate]
        selectionBbox = cmds.exactWorldBoundingBox(selection)

        # Using both x's to calculate the middle point
        midX = (selectionBbox[3]+selectionBbox[0])/2.0

        # Using both y's to calculate the middle point
        midY = (selectionBbox[4]+selectionBbox[1])/2.0

        # Select and move first locator to minimum Z on bounding box
        cmds.select(data.firstLocator)
        cmds.move(midX,midY,selectionBbox[2])

        # Select and move first locator to maximum Z on bounding box
        cmds.select(data.secondLocator)
        cmds.move(midX,midY,selectionBbox[5])

def makeProxyGeo():
    """This function creates a default proxy geo if the user does not provides one """

    # Create a cube
    geo = cmds.polyCube(name="TreadProxyGeo", width=5, height=.5, depth=1, sx=5)[0]
    faces = [0,2,4,11,13]
    cmds.select(clear=True)
    
    # Select specific faces to make desired shape
    for f in faces:
        cmds.select("%s.f[%s]"%(geo,f), add=True)

    # Extrude those faces 
    cmds.polyExtrudeFacet(thickness=.5, offset=.1)

    # Select the geo itself
    cmds.select(geo, r=True)

    # Delete its history
    cmds.DeleteHistory()

    # Return reference to the geo
    return geo
    
def renamePreMade():
    """Function that renames User's geo to match our naming conventions"""

    userObj = cmds.textFieldButtonGrp("treadName", query=True, text=True)
    
    if not userObj:
        cmds.confirmDialog(t="Select a piece", m="Please choose a tread geometry")
        return
    
    cmds.select(userObj)    
    userObj = cmds.rename("TreadMesh")

def makeTread(*args):
    """This function creates the circle that represent the tread"""

    # Get the position from both locators
    loc1Pos = cmds.getAttr("{}.translateZ".format(data.firstLocator))
    loc2Pos = cmds.getAttr("{}.translateZ".format(data.secondLocator))
    locDistance = abs(loc1Pos-loc2Pos)
    data.curveRadius = locDistance/2.0
    locCenter = (loc1Pos+loc2Pos)/2.0
    
    # Create the curve
    curveQuality = cmds.intSliderGrp("curveQuality", q=True, v=True)
    data.treadCircle = cmds.circle(name="TreadCurve", radius=data.curveRadius, nr=(1,0,0), sections=curveQuality)[0]
    data.treadCircle = checkDuplicatedName(data.treadCircle)
    
    # ****************************************** Here we align the circle to the locators ********************************************
    
    # Create a group containing the locators
    locatorGroup = cmds.group(data.firstLocator, data.secondLocator, n="LocGroup")

    # Select the circle
    cmds.select(data.treadCircle)

    # Select the group
    cmds.select(locatorGroup, add=True)

    # Align the circle to the group
    cmds.align(x="mid", y="mid", z="mid", alignToLead=True)

    # Unparent the locators
    cmds.parent(data.firstLocator, data.secondLocator, world=True)
    # Delete the locator group
    cmds.delete(locatorGroup)
    
    # Finish selecting the curve
    cmds.select(data.treadCircle)
    cmds.FreezeTransformations()
    cmds.DeleteHistory()
    
def makeTreadObj(*args):
    """This function makes a tread out of the selected object"""

    usePreMade = cmds.radioButton("premadeGeo", query=True, select=True)
    
    if usePreMade:
        renamePreMade()
        return
    
    useProxy = cmds.checkBox("useProxy", query=True, value=True)
    
    if useProxy:
        if cmds.objExists("TreadProxyGeo"):
            userObj = "TreadProxyGeo"
        else:
            userObj = makeProxyGeo()
    else:
        userObj = cmds.textFieldButtonGrp("treadName", query=True, text=True)
        
        if not userObj:
            cmds.confirmDialog(t="Select a piece", m="Please choose a piece to build a tread or tick proxy option")
            return
    
    cmds.select(userObj, replace=True)
    
    # Verify if we want to use the actual measures of the object
    
    useBbox = cmds.checkBox("bboxCheck", q=True, v=True)
    
    if useBbox:
    
        bbox = cmds.exactWorldBoundingBox(userObj)
        radius = data.curveRadius
        perimeter = 2*3.14159*radius
        bboxDistance = abs(bbox[2]-bbox[-1])
        bboxDistance*=.85
        amount = round(perimeter / bboxDistance)
        
    else:
        amount = cmds.intSliderGrp("treadAmount", q=True, v=True)
     
    
    cmds.select(data.treadCircle, add=True)
    pathAnimation = cmds.pathAnimation(fm=True, f=True, fa="z", ua="y", stu=1, etu=amount, wu=(0,1,0), iu=False)
    
    # Adjust animCurve
    cmds.selectKey("{}_uValue".format(pathAnimation), time=(1,amount))
    cmds.keyTangent(itt="linear", ott="linear")
    
    #Creating snapshot
    cmds.snapshot(n="TreadSnapShot", ch=False, i=1, st=1, et=amount, update="animCurve")
    cmds.DeleteMotionPaths()
    cmds.select("TreadSnapShotGroup", r=True)
    
    if not amount == 1:
        data.treadMesh = cmds.polyUnite(n="TreadMesh", ch=False)[0]
        data.treadMesh = checkDuplicatedName(data.treadMesh)
        
    else:
        piece = cmds.listRelatives(cmds.ls(selection=True))[0]
        cmds.select(piece)
        cmds.parent(world=True)
        piece = cmds.rename("TreadMesh")
        cmds.DeleteHistory()
        
    cmds.delete("TreadSnapShotGroup")
        
    cmds.select(data.treadMesh, r=True)
    cmds.CenterPivot()
    
    # Hide original geo
    cmds.setAttr("%s.visibility"%userObj, False)

    # Delete Proxy geo if used
    if cmds.objExists("TreadProxyGeo"):
        cmds.delete("TreadProxyGeo")

def RemakeTread(*args):
    """This function remakes the tread if the user changes the amount of pieces"""

    if cmds.objExists(data.treadMesh):
        cmds.select(data.treadMesh,r=True)
        cmds.delete()
        makeTreadObj()

def finalizeTread(*args):    
    """This function creates a wire deformer that drives the shape of the mesh with a curve"""

    # Here we make wire deformer
    def makeWire(geo, CCurve, dropOffD=10):
        theWire = cmds.wire(geo, w=CCurve, n ="inputWire")
        wireNode = theWire[0]
        data.treadBaseWire = "{}BaseWire".format(CCurve)
        data.treadBaseWire = checkDuplicatedName(data.treadBaseWire)
        
        # Change dropoff distance
        cmds.setAttr("%s.dropoffDistance[0]"%wireNode, dropOffD)
    
    makeWire(data.treadMesh, data.treadCircle, 35)
    
    cmds.select(data.treadCircle, r=True)

    # Use point on curve deformation
    locatorPoints = addPointOnCurve()

    # Use result locators to add controllers to them
    controlGroups = controlOnLocator("curvePointCtrl", *locatorPoints)

    # Group the circle and base wire for organization
    wireCurvesGroup = cmds.group(data.treadCircle, data.treadBaseWire, name="TreadWireDeform")
    
    # Create main controller
    data.mainController = makeMainController()
    data.mainController = checkDuplicatedName(data.mainController)

    mainGroup = cmds.group(data.mainController, name="TreadMainControllerGroup")

    cmds.select(mainGroup, data.treadMesh)
    # Align the circle to the mesh
    cmds.align(x="mid", z="mid", alignToLead=True)
    # Parent curve controllers to main controller
    cmds.parent(controlGroups[1], data.mainController)
    # Constraint curves and mesh to main controller to rotate properly due to wire deformer
    cmds.select(data.mainController,data.treadMesh)
    cmds.orientConstraint(maintainOffset=True)
    cmds.select(data.mainController, wireCurvesGroup)
    cmds.orientConstraint(maintainOffset=True)

    # Make the tread rotate with main controller
    rotationExpression()

    # Delete locators
    cmds.delete(data.firstLocator, data.secondLocator)

    # Save this rigging data to the rigging node
    data.writeToNode()

def makeMainController(controlName="TreadMainController"):
    """This function creates the main controller for the rig"""

    meshBounds = cmds.exactWorldBoundingBox(data.treadMesh)
    length = abs(meshBounds[5]-meshBounds[2])
    mainController = cmds.circle(name=controlName, radius=length, normal=(0,1,0))[0]

    return mainController

def rotationExpression():
    """This function adds an expression that allows the tread to rotate while moving"""

    cmds.select(data.mainController)
    cmds.addAttr(data.mainController, longName="treadSpeed", attributeType="double", defaultValue=20, keyable=True)

    cmds.expression(name="TreadRotation", string="{0}.rotateX = -{1}.translateZ*{1}.treadSpeed".format(data.treadBaseWire, data.mainController))
    
def addClusters():
    """This function adds clusters to the curve"""

    cvList = cmds.ls("{}.cv[*]".format(data.treadCircle), flatten=True)
    
    clusterList = []
    
    for cv in cvList:
        cmds.select(cv, replace=True)
        # Append clusterHandles [index 1] to list of clusters
        clusterList.append(cmds.cluster()[1])

    return clusterList

def createCubeController():
    """This function creates a controller to drive the clusters"""

    # Create list of clusters
    clusterList = addClusters()
    
    for clusterName in clusterList:
        cubeCtrl = cmds.curve(n="clusterCtrl",
                   degree=1,
                   point=[(-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5),
                          (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5),
                          (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5),
                          (-0.5, 0.5, -0.5)],
                   k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0])
    
        #clusterName = "cluster%iHandle"%(i+1)
        cmds.select(cubeCtrl, clusterName)
        cmds.MatchTransform()
        cmds.select(cubeCtrl, r=True)
        cmds.FreezeTransformations()
        cmds.select(cubeCtrl, clusterName)
        cmds.parentConstraint(mo=True, w=1)
        
    cmds.select("clusterCtrl*")
    cmds.group(name="ClusterControlGroup")

    cmds.select("cluster*Handle")
    handleGroup = cmds.group(name="ClusterHandlesGroup")
    cmds.setAttr("TreadCurve.visibility",0)
    cmds.setAttr("%s.visibility"%handleGroup,0)

def addPointOnCurve():
    """This function adds locators that control the curve"""

    epList = cmds.ls("{}.ep[*]".format(data.treadCircle), flatten=True)
    
    locatorList = []
    
    for ep in epList:
        cmds.select(ep, replace=True)

        # Append locators generated on constraint to their list
        locatorList.append(cmds.pointCurveConstraint(constructionHistory=True, replaceOriginal=True)[0])
        cmds.CenterPivot()

    return locatorList

def controlOnLocator(controllerName="controller", *args):
    """This function adds controllers on the selected locators
    
    Parameters
    ----------
    controllerName : str
        The desired naming convention for the controllers and their group

    
    Returns
    -------
    list
        A list containing the driven group on index [0] and controller group on index [1]
    """

    controllerList = []

    for locator in args:
        # Create a curve with a cube shape
        cubeCtrl = cmds.curve(n=controllerName,
                   degree=1,
                   point=[(-0.5, 0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (-0.5, 0.5, -0.5), (-0.5, 0.5, 0.5),
                          (-0.5, -0.5, 0.5), (-0.5, -0.5, -0.5), (0.5, -0.5, -0.5), (0.5, -0.5, 0.5), (-0.5, -0.5, 0.5),
                          (0.5, -0.5, 0.5), (0.5, 0.5, 0.5), (0.5, 0.5, -0.5), (0.5, -0.5, -0.5), (-0.5, -0.5, -0.5),
                          (-0.5, 0.5, -0.5)],
                   k=[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0])

        controllerList.append(cubeCtrl)

        # Select both objects to match translation
        cmds.select(cubeCtrl, locator)
        cmds.MatchTranslation()
        cmds.select(cubeCtrl, r=True)
        cmds.FreezeTransformations()
        cmds.select(cubeCtrl, locator)
        cmds.parentConstraint(mo=True, w=1)

    cmds.select(args)
    locatorsGroup = cmds.group(name="PointLocatorsGroup")
    cmds.setAttr("{}.visibility".format(locatorsGroup), 0)

    cmds.select(controllerList)
    controllerGroup = cmds.group(name="{}Group".format(controllerName))

    return [locatorsGroup, controllerGroup]

def pickingObj(*args):
    """This function saves the name of the selected object in the field button"""

    selectedObj=cmds.ls(selection=True, objectsOnly=True)[0]
    cmds.textFieldButtonGrp("treadName", edit=True, text=selectedObj)

def checkDuplicatedName(obj):
    
    tries = 0

    while("|" in obj):
        tries +=1
        obj = renameDuplicatedObject(obj, tries)
        #duplicated = obj
    
    return obj

def renameDuplicatedObject(obj, index=0):
    
    if "|" in obj:
        newName = obj.replace("|", "")

        lastDigits = 0

        if index > 1:
            lastDigits = len(str(index))
            newName = newName[:-lastDigits]
        
        newName += str(index)
        obj = cmds.rename(obj, newName)
        return obj
    else:
        return obj
    
'''
    ----------------------------------- First Dialog and Window Creation -----------------------------------------
'''
# __name__ is a variable that all python modules have when executed
# When a python module is executed directly (pasting it on script editor,
# charcoal or through vsCode), the name is "__main__"
# When a python module is imported, the name is the name of the .py file
# or the alias assigned to it with "as" keyword
# This line specifies that the following should only get called
# when running this module directly and not trough imports
if __name__ == "__main__": 
    confirm = cmds.confirmDialog(t="Checking", m="Before proceeding, is your model placed on Z direction?", 
                                b=["Yes", "No"], db="Yes", cb="No", ds="No")
                                
    if confirm == "No":
        cmds.confirmDialog(t="Fix object", m="You MUST place the object at the origin and along the Z axis")
    else:
        makeWindow()
