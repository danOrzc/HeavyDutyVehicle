from maya import cmds

def createDataNode(nodeName):
    if not cmds.objExists(nodeName):
        cmds.createNode("network", name=nodeName)
        

def createDataAttribute(nodeName, attributeName):
    if not cmds.attributeQuery(attributeName, node=nodeName, exists=True):
        cmds.addAttr(nodeName, shortName=attributeName, dataType="string", multi=True)

def saveData(nodeName="rigDataNode", attributeName="myAttr", value=""):
    createDataNode(nodeName)
    createDataAttribute(nodeName, attributeName)
    #cmds.setAttr("{}.{}[{}]".format(nodeName, attributeName, 0), value, type="string")

    # Check if the attribute has one element
    theAttr = cmds.getAttr("{}.{}[0]".format(nodeName, attributeName))

    if theAttr:
        attrList = cmds.getAttr("{}.{}[*]".format(nodeName, attributeName))
        elementIndex = len(attrList)+1
    else:
        elementIndex = 0

    cmds.setAttr("{}.{}[{}]".format(nodeName, attributeName, elementIndex), value, type="string")
    theAttr = cmds.getAttr("{}.{}[*]".format(nodeName, attributeName))

    size = cmds.getAttr("{}.{}".format(nodeName, attributeName),size=True)
    print size
    print theAttr

def getData(nodeName="rigDataNode", attributeName="myAttr"):

    if not cmds.attributeQuery(attributeName, node=nodeName, exists=True):
        print "NO DATA"
        return

    size = cmds.getAttr("{}.{}".format(nodeName, attributeName),size=True)
    theAttr = cmds.getAttr("{}.{}[*]".format(nodeName, attributeName))

    if size == 1:
        return [theAttr]

    elif size>1:
        return theAttr
    
    else:
        return