from maya import cmds

"""
    This tool creates a window that allows the user to create a thank thread
    by Team Mighty Eagle and friends
    
    Laio Passos
    Ian Pease
    Daniel Orozco
"""

# Function to create the main window UI
def makeWindow():
    winName = "ThreadMaker"
    
    # Check if the window is already open
    if cmds.window(winName, query=True, exists=True):
        cmds.deleteUI(winName)
    
    # If it doesn't exist, make it    
    cmds.window(winName, t="Thread Maker")
    cmds.window(winName, e=True, w=500)
    
    # Main layout for UI
    cmds.columnLayout()
     
    '''
    ----------------------------------- Locator Creation -----------------------------------------
    '''
    
    cmds.frameLayout(label="Locators")
    cmds.text(label="This is the very first step on the process")
    cmds.gridLayout(numberOfColumns=1, cellWidth=500)
    
    cmds.button(label="Initialize", command="initFunc()")
    
    cmds.setParent('..')
    cmds.separator(h=5)
    cmds.setParent('..')
    
    '''
    ----------------------------------- Circle Creation -----------------------------------------
    '''
    
    cmds.frameLayout(label="Curve")
    cmds.text(label="This is the second step on the process")
    cmds.gridLayout(numberOfColumns=1, cellWidth=500)
    cmds.intSliderGrp("curveQuality", l="Curve quality", f=True, v=6, minValue=6, maxValue=20)
    cmds.button(label="Make Curve", c="makeThread()")
    
    cmds.setParent('..')
    cmds.separator(h=5)
    cmds.setParent('..')
    
    '''
    ----------------------------------- Thread Creation -----------------------------------------
    '''
    
    cmds.frameLayout(label="Making Thread")
    cmds.text(label="Now create the thread")
    
    # Nested function that updates the UI depending on the creation method
    def updateUI(value):
        
        # Update elements
        cmds.checkBox("useProxy",e=True, en=not value)
        cmds.checkBox("bboxCheck",e=True, en=not value)
        cmds.intSliderGrp("threadAmount",e=True, en=not value)
        
        # Make sure the text Field is enable when using the premade geo method
        if not value:
            proxyGeo = cmds.checkBox("useProxy", query=True, value=True)
            cmds.textFieldButtonGrp("threadName",e=True, en=not proxyGeo)
            usebbox = cmds.checkBox("bboxCheck", query=True, value=True)
            cmds.intSliderGrp("threadAmount",e=True, en=not usebbox)
        else:
            cmds.textFieldButtonGrp("threadName",e=True, en=value)
    
    # Radio Buttons for choosing between piece or whole mesh
    cmds.gridLayout(numberOfColumns=2, cellWidth=250)
    cmds.radioCollection()
    cmds.radioButton("premadeGeo", label="Previously created geometry", cc= lambda value: updateUI(value))
    cmds.radioButton(label="Make thread from a piece", select=True)
    cmds.setParent('..')
    
    # Layout for creation methods
    cmds.gridLayout("threadGridLO", numberOfColumns=1, cellWidth=500)
    cmds.checkBox("useProxy", label="Create Proxy Geo", cc= lambda value: cmds.textFieldButtonGrp("threadName",e=True, en=not value))
    cmds.textFieldButtonGrp("threadName", buttonLabel="Pick Selected", bc="pickingObj()", placeholderText="Selected Mesh")
    cmds.checkBox("bboxCheck", label="Use piece's bounding box", cc= lambda value: cmds.intSliderGrp("threadAmount",e=True, en=not value))
    cmds.intSliderGrp("threadAmount", l="Amount of threads", f=True, v=20, minValue=1, maxValue=500, cc="RemakeThread()")
    cmds.button(label="Make Thread", c="makeTreadObj()")
    
    cmds.setParent('..')
    cmds.separator(h=5)
    cmds.button(l="Finalize", c="finalizeThread()")
    
    cmds.setParent('..')
    cmds.showWindow()

# This function creates the locators
def initFunc():
    cmds.spaceLocator(name="CircleLocator001")
    cmds.scale(4,4,4)
    cmds.spaceLocator(name="CircleLocator002")
    cmds.scale(4,4,4)
    cmds.confirmDialog(message="Now place the locators on the two end of the wheels")

# This function creates a default proxy geo if the user does not provides one   
def makeProxyGeo():
    geo = cmds.polyCube(name="ThreadProxyGeo", width=5, height=.5, depth=1, sx=5)[0]
    faces = [0,2,4,11,13]
    cmds.select(clear=True)
    
    for f in faces:
        cmds.select("%s.f[%s]"%(geo,f), add=True)
        
    cmds.polyExtrudeFacet(thickness=.5, offset=.1)
    cmds.select(geo, r=True)
    cmds.DeleteHistory()
    return geo
    
# Function that renames User's geo to match our naming conventions
def renamePreMade():
    userObj = cmds.textFieldButtonGrp("threadName", query=True, text=True)
    
    if not userObj:
        cmds.confirmDialog(t="Select a piece", m="Please choose a thread geometry")
        return
    
    cmds.select(userObj)    
    userObj = cmds.rename("ThreadMesh")

# This function creates the circle that represent the thread   
def makeThread():
    cmds.select("CircleLocator001")
    loc1Pos = cmds.getAttr(".translateZ")
    cmds.select("CircleLocator002")
    loc2Pos = cmds.getAttr(".translateZ")
    locDistance = abs(loc1Pos-loc2Pos)
    makeThread.curveRadius = locDistance/2.0
    locCenter = (loc1Pos+loc2Pos)/2.0
    
    # Create the curve
    curveQuality = cmds.intSliderGrp("curveQuality", q=True, v=True)
    threadCurve = cmds.circle(name="ThreadCurve", radius=makeThread.curveRadius, nr=(1,0,0), sections=curveQuality)
    cmds.move(0,0,locCenter)
    
    # Here we align the circle to the locators
    '''
    cmds.group("CircleLocator001", "CircleLocator002", n="LocGroup")
    cmds.select("ThreadCurve")
    cmds.select("LocGroup", add=True)
    cmds.align(z="mid", alignToLead=True)
    cmds.select("LocGroup")
    cmds.parent("CircleLocator001", "CircleLocator002", world=True)
    cmds.delete("LocGroup")
    '''
    
    cmds.select("ThreadCurve")
    
# This function makes a thread out of the selected object
def makeTreadObj():
    usePreMade = cmds.radioButton("premadeGeo", query=True, select=True)
    
    if usePreMade:
        renamePreMade()
        return
    
    useProxy = cmds.checkBox("useProxy", query=True, value=True)
    
    if useProxy:
        if cmds.objExists("ThreadProxyGeo"):
            userObj = "ThreadProxyGeo"
        else:
            userObj = makeProxyGeo()
    else:
        userObj = cmds.textFieldButtonGrp("threadName", query=True, text=True)
        
        if not userObj:
            cmds.confirmDialog(t="Select a piece", m="Please choose a piece to build a thread or tick proxy option")
            return
    
    cmds.select(userObj, replace=True)
    
    # Verify if we want to use the actual measures of the object
    
    useBbox = cmds.checkBox("bboxCheck", q=True, v=True)
    
    if useBbox:
    
        bbox = cmds.exactWorldBoundingBox(userObj)
        radius = makeThread.curveRadius
        perimeter = 2*3.14159*radius
        bboxDistance = abs(bbox[2]-bbox[-1])
        bboxDistance*=.85
        amount = round(perimeter / bboxDistance)
        
    else:
        amount = cmds.intSliderGrp("threadAmount", q=True, v=True)
     
    
    cmds.select("ThreadCurve",add=True)
    cmds.pathAnimation(fm=True, f=True, fa="z", ua="y", stu=1, etu=amount, wu=(0,1,0), iu=False)
    
    # Adjust animCurve
    cmds.selectKey("motionPath1_uValue", time=(1,amount))
    cmds.keyTangent(itt="linear", ott="linear")
    
    #Creating snapshot
    cmds.snapshot(n="ThreadSnapShot", ch=False, i=1, st=1, et=amount, update="animCurve")
    cmds.DeleteMotionPaths()
    cmds.select("ThreadSnapShotGroup", r=True)
    
    if not amount == 1:
        cmds.polyUnite(n="ThreadMesh", ch=False)
        
    else:
        piece = cmds.listRelatives(cmds.ls(selection=True))[0]
        cmds.select(piece)
        cmds.parent(world=True)
        piece = cmds.rename("ThreadMesh")
        cmds.DeleteHistory()
        
    cmds.delete("ThreadSnapShotGroup")
        
    cmds.select("ThreadMesh", r=True)
    cmds.CenterPivot()
    
    # Hide original geo
    cmds.setAttr("%s.visibility"%userObj, False)

def RemakeThread():
    if cmds.objExists("ThreadMesh"):
        cmds.select("ThreadMesh",r=True)
        cmds.delete()
        makeTreadObj()

def finalizeThread():    
    # Here we make wire deformer
    def makeWire(geo, CCurve, dropOffD=10):
        theWire = cmds.wire(geo, w=CCurve, n ="inputWire")
        wireNode = theWire[0]
        
        # Change dropoff distance
        cmds.setAttr("%s.dropoffDistance[0]"%wireNode, dropOffD)
    
    cmds.select("ThreadMesh", r=True)
    wireObj=cmds.ls(sl=True, o=True)[0]  
    
    cmds.select("ThreadCurve", r=True)
    wireCurve=cmds.ls(sl=True, o=True)[0]
    makeWire(wireObj, wireCurve,35)
    
    cmds.select("ThreadCurve", r=True)
    
    createCubeController()
    
def addClusters():
    cvList = cmds.ls("ThreadCurve.cv[*]", flatten=True)
    clusterList = []
    
    for cv in cvList:
        cmds.select(cv, replace=True)
        # Append clusterHandles [index 1] to list of clusters
        clusterList.append(cmds.cluster()[1])
    return clusterList

def createCubeController():
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
        
    cmds.select("clusterCtrl")


def pickingObj():
    selectedObj=cmds.ls(selection=True, objectsOnly=True)[0]
    cmds.textFieldButtonGrp("threadName", edit=True, text=selectedObj)
    
    
'''
    ----------------------------------- First Dialog and Window Creation -----------------------------------------
'''

confirm = cmds.confirmDialog(t="Checking", m="Before proceeding, is your model placed on Z direction?", 
                            b=["Yes", "No"], db="Yes", cb="No", ds="No")
                            
if confirm == "No":
    cmds.confirmDialog(t="Fix object", m="You MUST place the object at the origin and along the Z axis")
else:
    makeWindow()
    
