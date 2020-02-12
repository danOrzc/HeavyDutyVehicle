from maya import cmds

# This function sets up Maya's UI at launch
def start():
    import mainMenuTab
    mainMenuTab.createTab()
    import mainMenuShelf
    mainMenuShelf.createShelf()

# Call the function once Maya finished loading everything
cmds.evalDeferred(start, lowestPriority=True)