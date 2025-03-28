import os
import math
import subprocess
import time
from datetime import datetime
import functools
import pose_library.week1.config as config

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
    fileExtension = os.path.splitext(poseFile)[-1]
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
    formattedCreatedTime = datetime.fromtimestamp(createdTime).strftime('%m-%d-%Y %I:%M %p')
    
    modifiedTime = os.path.getmtime(poseFilePath)
    formattedModifiedTime = datetime.fromtimestamp(modifiedTime).strftime('%m-%d-%Y %I:%M %p')
    
    # Improved file size formatting
    fileSize = os.path.getsize(poseFilePath)
    fileSizeKb = str("{} KB".format(math.ceil(fileSize / 1024)))
    
    selectedCharPoseInfo = {
        'poseName': poseName,
        'poseType': poseType,
        'fullPath': poseFilePath,
        'imgFile': getIconImage(poseFilePath),
        'cDate': formattedCreatedTime,
        'mDate': formattedModifiedTime,
        'size': fileSizeKb
    }
    
    return selectedCharPoseInfo

def deleteFile(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
        print("{} has been deleted".format(filepath))
    else:
        print("{} does not exist".format(filepath))

def renameFile(filepath, newName):
    #check if the file exists
    if not os.path.exists(filepath):
        raise FileNotFoundError("The file '{}' does not exist".format(filepath))
    directory = os.path.dirname(filepath)
    #get the file extension
    _, extension = os.path.splitext(filepath)
    # construct the new file path
    newFilePath = os.path.join(directory, newName + extension)
    
    #check if a file with the new name already exists
    if os.path.exists(newFilePath):
        raise FileExistsError("A file with the same name '{}' already exists".format(newName + extension))
    
    os.rename(filepath, newFilePath)
    print("File '{}' has been renamed to '{}'".format(filepath, newFilePath))

def revealFile(filepath):
    absolutePath = os.path.abspath(filepath)
    # https://www.geoffchappell.com/studies/windows/shell/explorer/cmdline.htm
    # os.system(f'explorer /select,"{absolutePath}"')
    os.system('explorer /select,"{}"'.format(absolutePath))
    #subprocess.run(["explorer", "/select,", absolutePath])

def timeIt(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("{} took {:.6f} seconds to execute".format(func.__name__, end_time - start_time))
        return result

    return wrapper
    
if __name__ == "__main__":
    folder_structure_to_dictionary(config.PROJECT_ROOT, config.FOLDER_DICT)