from maya import cmds

# This function sets up Maya's UI at launch
def start():
    from mainMenuTab import createTab
    from mainMenuShelf import createShelf
    createTab()
    #createShelf()

# Call the function once Maya finished loading everything
cmds.evalDeferred(start, lowestPriority=True)