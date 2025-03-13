import json
import os
import maya.cmds as mc
from . import config

def getJoints():
    return

def getControls(topNode = "ctrl_GRP", selection=False):
    """
    Get control objects from the rig
    Args:
        topNode (str): Top node of the rig
        selection (bool): If True, only return selected controls. If False, return all controls
    Returns:
        list: List of control names
    """
    # Get selected control
    selectedNodes = mc.ls(selection = True)
    if not selectedNodes:
        mc.warning("Please select at least one control in the scene.")
        return []
    
    selectedNode = selectedNodes[0]
    selectedShortName = selectedNode.split("|")[-1]  # Get short name of selected control
    
    # Handle namespace
    if ":" in selectedNode:
        namespace = selectedNode.split(":")[0]
        topNode = "{}:{}".format(namespace, topNode)
    
    # Get the top node with full path
    matching_nodes = mc.ls(topNode, long = True)
    if not matching_nodes:
        mc.warning("Could not find top node: {}".format(topNode))
        return []
    
    topNode = matching_nodes[0]
    allTransforms = mc.listRelatives(topNode, allDescendents = True, type = "transform", fullPath = True) or []
    print("Found {} transforms".format(len(allTransforms)))
    
    # Get only the selected control
    controls = []
    for ctrl in allTransforms:
        shortName = ctrl.split("|")[-1]
        if shortName == selectedShortName:
            if (mc.attributeQuery("translate", node = ctrl, exists = True) and
                    mc.listRelatives(ctrl, shapes = True)):
                controls.append(shortName)
                break  # Found our control, no need to continue
    
    print("Found {} controls matching selection".format(len(controls)))
    return controls

# def getControls(topNode= "controls", selection = True):
#     selectedNodes = mc.ls(selection = True)
#     if not selectedNodes:
#         mc.warning("please select at least one control in the scene.")
#         return
#
#     selectedNode = selectedNodes[0]
#     if ":" in selectedNode:
#         namespace = selectedNode.split(":")[0]
#         topNode = "{}:{}".format(namespace, topNode)
#
#     if not selection:
#         return
#     #how to select: select all children, and get the controls
#     allChildren = mc.listRelatives(topNode, allDescendents = True, type = "transform", fullPath = True) or []
#     controls = [control for control in allChildren if mc.objExists(control + ".controlType")]
#
#     #define selected node
#     if selection:
#         selected = mc.ls(selection=True, long = True)
#         controls = [control for control in controls if control in selected]
#     return controls
    

# def getPoseData(controls):
#     poseData = {}
#     for control in controls:
#         matrix = mc.xform(control, matrix=True, objectSpace=True, query=True)
#         #remove namespace if exists
#         control = control.split(":")[-1]
#         poseData[control] = matrix
#     return poseData

def getPoseData(controls = None):
    """
    Get the pose data for the specified controls
    Args:
        controls (list): List of controls to get data from
    Returns:
        dict: Dictionary of control data
    """
    if not controls:
        return {}
    
    poseData = {}
    for ctrl in controls:
        # Get all keyable attributes
        attrs = mc.listAttr(ctrl, keyable = True) or []
        if not attrs:
            continue
        
        ctrlData = {}  # Dictionary to store attr:value pairs
        for attr in attrs:
            try:
                attrPath = "{}.{}".format(ctrl, attr)
                if mc.objExists(attrPath):
                    value = mc.getAttr(attrPath)
                    # Handle array attributes (like translate, rotate, scale)
                    if isinstance(value, tuple):
                        value = list(value[0])  # Convert tuple to list
                        # Store each component separately
                        if len(value) == 3:  # For translate, rotate, scale
                            ctrlData[attr + "X"] = value[0]
                            ctrlData[attr + "Y"] = value[1]
                            ctrlData[attr + "Z"] = value[2]
                    else:
                        ctrlData[attr] = value
            except Exception as e:
                print("Could not get value for {}.{}: {}".format(ctrl, attr, e))
                continue
        
        if ctrlData:  # Only add if we got some attribute data
            poseData[ctrl] = ctrlData
            print("Saved data for {}: {}".format(ctrl, ctrlData))  # Debug print
    
    return poseData

# def applyPoseData(poseData, selectedControls=None, excludeRootAndMainControls=True, keyPoseControls= False):
#
#     selectedNodes = mc.ls(selection=True)
#     if not selectedNodes:
#         mc.warning("Please select at least one control in the scene.")
#         return
#     selectedNode = selectedNodes[0]
#     if ":" in selectedNode:
#         namespace = selectedNode.split(":")[0]
#     else:
#         namespace = None
#
#     for control, matrix in poseData.items():
#         if namespace:
#             control = "{}:{}".format(namespace, control)
#         if not mc.ls(control):
#             continue
#
#         if excludeRootAndMainControls:
#             if "RootControl1" in control or "MainControl" in control:
#                 continue
#
#         if selectedControls is None or control in selectedControls:
#             mc.xform(control, matrix=matrix, objectSpace=True)
#             if keyPoseControls:
#                 keyableAttrs = mc.listAttr(control, keyable=True) or []
#                 for attr in keyableAttrs:
#                     mc.setKeyframe(control, attr=attr)

def applyPose(poseData, selectedControls = None, excludeRootMainControls = False, keyControls = False):
    """
    Apply pose data to controls
    Args:
        poseData (dict): Pose data to apply
        selectedControls (list): List of controls to apply pose to. If None, apply to all
        excludeRootMain (bool): Whether to exclude root and main controls
        keyControls (bool): Whether to set keyframes on controls
    """
    if not poseData:
        mc.warning("No pose data to apply!")
        return
    
    # If no specific controls are selected, apply to all controls in the pose data
    controlsToProcess = selectedControls if selectedControls else poseData.keys()
    
    for ctrl in controlsToProcess:
        if ctrl not in poseData:
            continue
        
        # Skip root and main controls if specified
        if excludeRootMainControls and ("root" in ctrl.lower() or "main" in ctrl.lower()):
            continue
        
        ctrlData = poseData[ctrl]
        print("Applying data to {}: {}".format(ctrl, ctrlData))  # Debug print
        
        for attr, value in ctrlData.items():
            try:
                attrPath = "{}.{}".format(ctrl, attr)
                if mc.objExists(attrPath):
                    mc.setAttr(attrPath, value)
                    if keyControls:
                        mc.setKeyframe(attrPath)
            except Exception as e:
                print("Could not set {}.{}: {}".format(ctrl, attr, e))
                
# def writePoseData(filepath, poseData):
#     with open(filepath, "w") as fp:
#         json.dump(poseData, fp, ensure_ascii=True, indent=4, sort_keys=True)

def writePoseData(filepath, poseData):
    """
    Write pose data to file
    Args:
        filepath (str): Path to save the pose file
        poseData (dict): Pose data to save
    """
    try:
        # Verify data structure before saving
        if not isinstance(poseData, dict):
            raise ValueError("Pose data must be a dictionary")
        
        for ctrl, data in poseData.items():
            if not isinstance(data, dict):
                raise ValueError("Control data must be a dictionary for control: {}".format(ctrl))
        
        with open(filepath, 'w') as fp:
            json.dump(poseData, fp, ensure_ascii = False, indent = 4, sort_keys = True)
        print("Successfully wrote pose data with {} controls".format(len(poseData)))
    except Exception as e:
        mc.warning("Error writing pose file: {}".format(e))

def readPoseData(filepath):
    with open(filepath) as fp:
        poseData = json.load(fp)
    return poseData

def getViewportSettings():
    """Get current viewport settings

    Returns:
        tuple: (active_view, background_color)
    """
    activeView = None
    for panel in mc.getPanel(type="modelPanel"):
        if mc.modelEditor(panel, query=True, activeView=True):
            activeView = panel
            
    if mc.displayPref(query=True, displayGradient=True):
        backgroundColor = [mc.displayRGBColor("backgroundTop", query=True),
                           mc.displayRGBColor("backgroundBottom",query=True)]
    else:
        backgroundColor=[mc.displayRGBColor("background", query=True)]
    
    for flag in config.THUMBNAIL_VIEWPORT_FLAGS.keys():
        config.THUMBNAIL_VIEWPORT_FLAGS[flag] = eval('mc.modelEditor("{}", q=True, {}=True)'.format(activeView, flag))
    
    for attr in config.RENDERING_GLOBALS.keys():
        config.RENDERING_GLOBALS[attr] = mc.getAttr(attr)
    
    return activeView, backgroundColor

def restoreViewportSettings(activeView, backgroundColor, viewportFlags, renderGlobals):
    """Restore viewport display settings

    Args:
        activeView (str): Name of the active viewport panel
        backgroundColor (list): List of RGB color values
        viewportFlags (dict): Dictionary of viewport display flags
        renderGlobals (dict): Dictionary of render settings
    """
    if len(backgroundColor) > 1:
        mc.displayPref(displayGradient=True)
        mc.displayRGBColor("backgroundTop",
                           backgroundColor[0][0],
                           backgroundColor[0][1],
                           backgroundColor[0][2])
        mc.displayRGBColor("backgroundBottom",
                           backgroundColor[1][0],
                           backgroundColor[1][1],
                           backgroundColor[1][2])
    else:
        mc.displayRGBColor("background",
                           backgroundColor[0][0],
                           backgroundColor[0][1],
                           backgroundColor[0][2])
    
    modelEditorFlagArguments = ','.join('{}={}'.format(flag, state)
                                        for flag, state in config.THUMBNAIL_VIEWPORT_FLAGS.items())
    mc.modelEditor(activeView, edit=True, **viewportFlags)
    
    for attr, value in config.RENDERING_GLOBALS.items():
        mc.setAttr(attr, value)
        
def createThumbnailFromCurrentView(poseName, poseDir, fileType='png'):
    activeView, backgroundColor = getViewportSettings()
    mc.modelEditor(activeView, edit=True, allObjects=False, polymeshes=True, pluginShapes=True, grid=True,
                   displayTextures=True)
    #for antialiasing
    mc.setAttr('hardwareRenderingGlobals.ssaoEnable', True)
    mc.setAttr('hardwareRenderingGlobals.multiSampleEnable', True)
    mc.setAttr('hardwareRenderingGlobals.multiSampleCount', 8)
    mc.displayPref(displayGradient=False)
    mc.displayRGBColor("background", 0.295, 0.295, 0.295)
    thumbnailPath = os.path.join(poseDir, "{}.{}".format(poseName, fileType))
    mc.playblast(format="image", completeFilename=thumbnailPath, frame=(mc.currentTime(query=True)),
                 forceOverwrite=True, sequenceTime=False, clearCache=True, viewer=False,
                 showOrnaments=False, percent=100, compression=fileType, quality=100)
    restoreViewportSettings(activeView, backgroundColor)



































