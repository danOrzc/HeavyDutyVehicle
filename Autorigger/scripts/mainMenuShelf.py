from maya import mel
from maya import cmds

def createShelf():
    shelfName='MPYR'
    mel.eval('global string $gShelfTopLevel;')
    mainShelfLayout=mel.eval('$tmp=$gShelfTopLevel;')
    if cmds.shelfLayout(shelfName,exists=True):
        return
    #add new tab
    createdShelf=mel.eval('addNewShelfTab "%s";'%shelfName)
    cmds.shelfButton(annotation='Snap/Reset/Key Tools',
        image1='humanIK_CharCtrl.png',
        command='import mpyr.tools.rigTools;reload(mpyr.tools.rigTools);mpyr.tools.rigTools.RigTools()',
        parent=createdShelf 
        )
    cmds.shelfButton(annotation='Joint Orient Tool',
        image='kinInsert.png', 
        command='import mpyr.tools.jointTools;reload(mpyr.tools.jointTools);mpyr.tools.jointTools.JointOrientTool()',
        style='iconAndTextVertical',
        sic=True,
        parent=createdShelf 
        )
    cmds.shelfButton(annotation='Ctrl Appearance Editor',
        image='polyMoveVertex.png',#'HIKCharacter.png', 
        command='import mpyr.tools.ctrlShape;reload(mpyr.tools.ctrlShape);mpyr.tools.ctrlShape.SaveLoadCtrlShape()',
        parent=createdShelf 
        ) 
        
if __name__ == '__main__': createShelf()