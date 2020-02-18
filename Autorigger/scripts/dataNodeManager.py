"""Rigging data storing.

This script has functions that allows maya to save the rigging tool process
results inside an empty network node that doesn't have transform info.

It is in charge of creating the node and the attributes to store the data.
It can also query the data or delete the attributes.

We are using this module to save the names of the controllers across the rigging
process and the groups that contain them. This way we can get the data later
to parent them correctly to the mainController. This allows us to create multiple
rigs of the same type (multiple wheels, treads, etc) and rig creation after
parenting (add more wheels or arms)
"""

from maya import cmds

class NodeData():
    """A class used to represent a Node that saves rigging data to Maya

    It takes the name of the controllers and groups that drive the rigging processes and
    saves them into a Network node in Maya, which doesn't have transforms or any other
    kind of unnecesary data.
    

    Attributes
    ----------
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
    writeToNode()
        Takes the rigging info and stores it in a node
    """
    def __init__(self):
        """Initialize default values"""

        self.mainController = ""
        self.mainControllerGroup =""
        self.controllerAttributeName = ""
        self.controllerGroupAttributeName = ""

    def writeToNode(self):
        """Takes the rigging info and stores it in a node"""

        saveData(attributeName=self.controllerGroupAttributeName, value=self.mainControllerGroup)
        saveData(attributeName=self.controllerAttributeName, value=self.mainController)

def createDataNode(nodeName):
    """Creates a new network node if it was not previously created
        
        Parameters
        ----------
        nodeName : str
            The name of the rigging data node
    """

    # Create node if it doesn't exist
    if not cmds.objExists(nodeName):
        cmds.createNode("network", name=nodeName)
        
def createDataAttribute(nodeName, attributeName):
    """Creates new attribute on the node if it doesn't exist.

    It creates multi attributes, which are lists that can store multiple indices
    of data of the same type (i.e. multiple strings)
    
    Parameters
    ----------
    nodeName : str
        The name of the rigging data node to create a new attribute into
    attributeName : str
        The name of the desired attribute to store the info
    """

    # Create attribute if it doesn't exist on the node
    if not cmds.attributeQuery(attributeName, node=nodeName, exists=True):
        cmds.addAttr(nodeName, shortName=attributeName, dataType="string", multi=True)

def saveData(nodeName="rigDataNode", attributeName="myAttr", value=""):
    """Save data in the specified attribute on the node.

    Parameters
    ----------
    nodeName : str
        The name of the rigging data node to create a new attribute into
    attributeName : str
        The name of the desired attribute to store the info
    value : str
        The information to store (i.e. the namme of the controllers which will be used in other step)
    """

    # Try to create a new node
    createDataNode(nodeName)

    # Trye to create an attribute on that node
    createDataAttribute(nodeName, attributeName)

    # Get the first element [0] of the attribute
    theAttr = cmds.getAttr("{}.{}[0]".format(nodeName, attributeName))

    # Check if that element is valid (the attribute list has at least one attribute)
    if theAttr:
        # Get entire list of attributes
        attrList = getData(attributeName=attributeName)

        # If the value is already in the list (e.g. object was deleted and created new one with the same name)
        # exit the function
        if value in attrList:
            return

        # The index where we want to save the new value is the same as the length of the list
        # Because we want to store it in the end of the multi attribute
        elementIndex = len(attrList)

    # If the element is not valid (the list is empty),
    # we add our value to the index 0
    else:
        elementIndex = 0

    # Set the attribute value
    # Using format function to put variables inside {}'s
    # This way we build the attribute's name using the function's parameters
    # String is {nodeName}.{attributeName}{elementIndex}
    cmds.setAttr("{}.{}[{}]".format(nodeName, attributeName, elementIndex), value, type="string")
    """
    theAttr = cmds.getAttr("{}.{}[*]".format(nodeName, attributeName))

    size = cmds.getAttr("{}.{}".format(nodeName, attributeName),size=True)
    """

def getData(nodeName="rigDataNode", attributeName="myAttr"):
    """Get data from a specified attribute on the node.

    Parameters
    ----------
    nodeName : str
        The name of the node where the attribute is located
    attributeName : str
        The name of the attribute to retrieve the info from
    """

    # If the attribute doesn't exist, return an empty list
    if not cmds.attributeQuery(attributeName, node=nodeName, exists=True):
        return []

    # Get the size of the attribute
    # This is because when the attribute has only one element, it returns it as a single string
    # but when it has multiple elements, it returns it as a list
    size = cmds.getAttr("{}.{}".format(nodeName, attributeName),size=True)

    # Get the attribute information
    theAttr = cmds.getAttr("{}.{}[*]".format(nodeName, attributeName))

    # If the size is one element, save it to a list and return it
    if size == 1:
        return [theAttr]

    # Else, if the list has more than one element, return it as it is (already a list)
    elif size>1:
        return theAttr
    
    # If the attribute is empty, return empty list
    else:
        return []

def deleteValue(nodeName="rigDataNode", attributeName="myAttr", value=""):
    """Delete a specified value from the attribute list on the node.

    Parameters
    ----------
    nodeName : str
        The name of the rigging data node to delete a value from
    attributeName : str
        The name of the attribute containing that value
    value : str
        The exact value to delete from the attribute
    """

    # Exit the function if the node doesn't exist
    if not cmds.objExists(nodeName):
        return

    # Get the attribute list from the node
    dataList = getData(nodeName=nodeName, attributeName=attributeName)

    # If it is empty (or doesn't exist), exit the function
    if not dataList:
        return

    # Delete each element on the attribute using their indexes
    for index in xrange(len(dataList)):
        # removeMultiInstance removes an element by giving the name of the attribute and the index of the element
        cmds.removeMultiInstance("{}.{}[{}]".format(nodeName, attributeName, index))

    # Create a new list containing only the elements that are not value
    # This is a list comprehension. It uses a for statement to iterate over a list
    # and at the same time compares the elements with the value given to see that they are not equal
    # then every element that succeeds the verification is added to the new list
    # [] are necessary to wrap the line to specify that we are saving a list
    newList = [element for element in dataList if not element == value]

    # Save each element on the new list to the node
    for element in newList:
        saveData(nodeName=nodeName, attributeName=attributeName, value=element)

def deleteDataAttribute(nodeName="rigDataNode", attributeName="myAttr"):
    """Delete the entire attribute from the node.

    Parameters
    ----------
    nodeName : str
        The name of the node that contains the attribute
    attributeName : str
        The name of the attribute that is going to be deleted
    """
    # Exit the function if the node doesn't exist
    if not cmds.objExists(nodeName):
        return
    
    # Delete the attribute if it exists
    if cmds.attributeQuery(attributeName, node=nodeName, exists=True):
        cmds.deleteAttr(nodeName, attribute=attributeName)