"""Maya userSetup file

This file gets executed when maya opens.

It contains a deferred evaluation with the lowest priority,
That is, it will be executed when no other idle events are scheduled.
"""

from maya import cmds

def __start():
    """This function creates the tool's tab and shelf"""
    
    import mainMenuTab
    mainMenuTab.createTab()
    import mainMenuShelf
    mainMenuShelf.createShelf()

# Call the function once Maya finished loading everything
cmds.evalDeferred(__start, lowestPriority=True)