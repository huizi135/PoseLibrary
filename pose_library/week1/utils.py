import os
import math
import pose_library.week1.config as config
from datetime import datetime  # This is the correct import

def create_folder_structure(base_path, folder_dict):
    for category, items in folder_dict.items():
        category_path = os.path.join(base_path, category)
        os.makedirs(category_path, exist_ok = True)
        for item in items:
            item_path = os.path.join(category_path, item)
            os.makedirs(item_path, exist_ok = True)
            
def folder_structure_to_dictionary(base_dir = config.PROJECT_ROOT):
    folder_dict = {}
    sub_dirnames = os.listdir(base_dir)
    for sub_dirname in sub_dirnames:
        directory = os.path.join(base_dir, sub_dirname)
        folder_dict[sub_dirname] = os.listdir(directory)
    return folder_dict

def getValidPoseFiles(poseDirFiles):
    validPoseFiles = list()
    for fileExtension in config.VALID_EXTENSIONS['File']:
        for poseFile in poseDirFiles:
            if poseFile.endswith(fileExtension):
                validPoseFiles.append(poseFile)
    return validPoseFiles

def getPoseType(poseName):
    #use posename to determine the type
    if poseName.startswith("Hand"):
        return "Hand"
    elif poseName.startswith("Face"):
        return "Face"
    else:
        return "Body"
    
def getIconImage(poseFile):
    image = ""
    fileExtension = os.path.splitext(poseFile)[1]
    if fileExtension in config.VALID_EXTENSIONS['File']:
        for imageExtension in config.VALID_EXTENSIONS['Img']:
            imageFile = poseFile.replace(fileExtension, imageExtension)
            if os.path.exists(imageFile):
                image = imageFile
    return image
    
def getPoseFileInformation(poseFilePath):
    """
    store pose information in a dictionary to save state and sorting info
    :param poseFilePath: Full path to the pose file
    :return: Dictionary with pose information
    """
    poseName = os.path.splitext(os.path.basename(poseFilePath))[0]
    poseType = getPoseType(poseName)
    createdTime = os.path.getctime(poseFilePath)
    formattedCreatedTime = datetime.utcfromtimestamp(createdTime).strftime('%m-%d-%Y %I:%M %p')
    
    modifiedTime = os.path.getmtime(poseFilePath)
    formattedModifiedTime = datetime.fromtimestamp(modifiedTime).strftime('%m-%d-%Y %I:%M %p')
    
    # Improved file size formatting
    fileSize = os.path.getsize(poseFilePath)
    if fileSize < 1024:
        fileSizeStr = "{0} B".format(fileSize)
    elif fileSize < 1024 * 1024:
        fileSizeStr = "{0:.2f} KB".format(fileSize / 1024.0)
    else:
        fileSizeStr = "{0:.2f} MB".format(fileSize / (1024.0 * 1024.0))
    
    selectedCharPoseInfo = {
        'poseName': poseName,
        'poseType': poseType,
        'fullPath': poseFilePath,
        'imgFile': getIconImage(poseFilePath),
        'cDate': formattedCreatedTime,
        'mDate': formattedModifiedTime,
        'size': fileSizeStr,
        'objectCount': 0
    }
    
    return selectedCharPoseInfo
    
if __name__ == "__main__":
    folder_structure_to_dictionary(config.PROJECT_ROOT, config.FOLDER_DICT)