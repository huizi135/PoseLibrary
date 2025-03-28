import maya.cmds as mc
import json

def getJoints():
    pass

def getControls(topNode= "controls", selection = True):
    selectedNodes = mc.ls(selection=True)
    if not selectedNodes:
        mc.warning("please select at least one node in the scene")
    return

    selectedNodes = selectedNodes[0]
    if ":" in selectedNodes:
        namespace = selectedNodes.split(":")[0]
        topNode = "{}:{}".format(namespace, topNode)
    
    if not topNode:
        return
    
    allChildren = mc.listRelatives(topNode, allDescendents = True, type= "transform") or []
    controls= [control for control in allChildren if mc.objExists(control + ".controlType")]
    
    #define selected controls
    if selection:
        selected = mc.ls(selection=True)
        controls = [control for control in controls if control in selected]
    return controls

def getPoseData(controls):
    poseData = {}
    for control in controls:
        matrix = mc.xform(control, matrix=True, objectSpace=True, worldSpace=True)
        #remove namespace if exsits
        control = control.split(":")[-1]
        poseData[control] = matrix
    return poseData

def applyPoseData(poseData, selectedControls=None, excludeRootMainControls=True, keyPoseControls=False):
    selectedNodes = mc.ls(selection=True)
    if not selectedNodes:
        mc.warning("please select at least one node in the scene")
        return
    selectedNodes = selectedNodes[0]
    if ":" in selectedNodes:
        namespace = selectedNodes.split(":")[0]
    else:
        namespace = None
    
    for control, matrix in poseData.items():
        if namespace:
            control = "{}:{}".format(namespace, control)
        if not mc.ls(control):
            continue
        
        if excludeRootMainControls:
            if "RootControl" in control or "MainControl" in control:
                continue
                
        if selectedControls is None or control in selectedControls:
            mc.xform(control, matrix=matrix, objectSpace=True)
            if keyPoseControls:
                keyableAttrs = mc.listAttr(control, keyable=True) or []
                for attr in keyableAttrs:
                    mc.setKeyframe(control, attr=attr, keyable=True)

def writePoseData(filepath, poseData):
    #ascii chinese, emoji .... can be read
    with open(filepath, "w") as fp:
        json.dump(poseData, fp, ensure_ascii=True, indent=4, sort_keys=True)

def readPoseData(filepath):
    with open(filepath) as fp:
        poseData = json.load(fp)
    return poseData