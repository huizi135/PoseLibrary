import os

#update the project root
PROJECT_ROOT = os.path.join(os.path.dirname(os.path.normpath(__file__)), "HUIZI")
ICON_DIR = os.path.join(os.path.dirname(os.path.normpath(__file__)), "icons")
DOCUMENT_DIR = os.path.join(os.environ['USERPROFILE'], 'Documents')

FOLDER_DICT = {
    "A": ["a", "b", "c"],
    "B": ["d", "e", "f"],
    "C": ["g", "h", "i"]
}

VALID_EXTENSIONS = {
    'File': ['.pose', '.jason'],
    'Img': ['.tga', '.jpg', '.jpeg', '.gif', '.png']
}

THUMBNAIL_VIEWPORT_FLAGS = {
    'nurbsCurves': False,
    'nurbsSurfaces':False,
    'polymeshes':False,
    'subdivSurfaces':False,
    'planes':False,
    'lights':False,
    'cameras':False,
    'controlVertices':False,
    'hulls':False,
    'joints':False,
    'ikHandles':False,
    'deformers':False,
    'dynamics':False,
    'fluids':False,
    'hairSystems':False,
    'follicles':False,
    'nCloths':False,
    'nParticles':False,
    'nRigids':False,
    'dynamicConstraints':False,
    'locators':False,
    'manipulators':False,
    'dimensions':False,
    'handles':False,
    'pivots':False,
    'textures':False,
    'strokes':False,
    'pluginShapes':False,
    'grid':False,
    'displayTextures':False
}

RENDERING_GLOBALS = {
    'hardwareRenderingGlobals.ssaoEnable': False,
    'hardwareRenderingGlobals.multiSampleEnable':False,
    'hardwareRenderingGlobals.multiSampleCount':8
}

# SORTING_OPTIONS = {
#     'Name (A-Z)': {'key': 'name', 'reverse': False},
#     'Name (Z-A)': {'key': 'name', 'reverse': True},
#     'Date Created (oldest first)': {'key': 'cDate', 'reverse': False},
#     'Date Created (newest first)': {'key': 'cDate', 'reverse': True},
#     'Date Modified (oldest first)': {'key': 'mDate', 'reverse': False},
#     'Date Modified (newest first)': {'key': 'mDate', 'reverse': True}
# }


# In config.py
SORTING_OPTIONS = [
    "Name (A to Z)",
    "Name (Z to A)",
    "Date Created (Oldest)",
    "Date Created (Newest)",
    "Date Modified (Oldest)",
    "Date Modified (Newest)"
]

# If you need to map display names to values
SORTING_VALUES = {
    "Name (A to Z)": 0,
    "Name (Z to A)": 1,
    "Date Created (Oldest)": 2,
    "Date Created (Newest)": 3,
    "Date Modified (Oldest)": 4,
    "Date Modified (Newest)": 5
}











