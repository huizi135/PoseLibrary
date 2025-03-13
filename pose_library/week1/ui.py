import os
import importlib
from collections import defaultdict

from PySide2.QtWidgets import (
    QWidget, QMainWindow, QHBoxLayout, QVBoxLayout, QSplitter, QLabel, QFrame, QListWidget,
    QGroupBox, QRadioButton, QCheckBox, QLineEdit, QPushButton, QSlider, QScrollArea, QToolButton, 
    QButtonGroup, QTableWidget, QTreeWidgetItem, QAbstractItemView, QAbstractScrollArea,
    QTableWidgetItem, QHeaderView, QTabWidget, QComboBox, QListWidgetItem, QMenu, QMessageBox,
    QInputDialog
)
from PySide2.QtCore import Qt, QSize, QSettings, QPoint
from PySide2.QtGui import QIcon


#maya package
import maya.cmds as mc
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance

from . import widgets
from . import utils
from . import config
from . import lib

reload(widgets)
reload(utils)
reload(config)
reload(lib)

def getMayaMainWindow():
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mayaMainWindowPtr), QWidget)

class PoseLibraryUI(QMainWindow):
    def __init__(self):
        super(PoseLibraryUI, self).__init__(parent = getMayaMainWindow())
        self.initData()
        self.initUI()
        self.initUIFunctions()
        self.readSettings()
        
    def initData(self):
        self.nameCompany = "Huizi"
        self.nameProduct = "Pose Library"
        settingsPath = os.path.join(config.DOCUMENT_DIR, self.nameProduct, "settings.ini")
        self.generalSettings = QSettings(self.nameCompany, self.nameProduct)
        self.userSettings = QSettings(settingsPath, QSettings.IniFormat)
        self.charDict = utils.folder_structure_to_dictionary()
        
    def initSize(self):
        self.charSelectionWidgetWidth = 150
        self.manipulatedPoseSetWidgetWidth = 300
        self.poseIconSize = QSize(256, 256)
        
    def initUI(self):
        self.setCentralWidget(QWidget())
        self.setWindowTitle("Pose Library")
        self.mainLayout = QHBoxLayout()
        self.centralWidget().setLayout(self.mainLayout)
        
        self.mainSplitter = QSplitter(Qt.Horizontal)
        self.mainLayout.addWidget(self.mainSplitter)
        
        #characters
        self.charSelectionWidget = QWidget(self.mainSplitter)
        self.charSelectionVLayout = QVBoxLayout()
        self.charSelectionWidget.setLayout(self.charSelectionVLayout)
        self.charSelectionVLayout.setContentsMargins(0,0,0,0)
        
        self.charSelectionLabel = QLabel("Characters")
        self.charSelectionLabel.setFrameStyle(QFrame.Shape.StyledPanel)
        self.charSelectionVLayout.addWidget(self.charSelectionLabel)
        self.charSelectionVLayout.setAlignment(Qt.AlignTop)
        
        self.charSelectionTreeWidget = widgets.SearchableTreeWidget(data=self.charDict)
        self.charSelectionVLayout.addWidget(self.charSelectionTreeWidget)
        
        #saved pose data
        self.savedPoseDataWidget = QWidget(self.mainSplitter)
        self.savedPoseDataVLayout = QVBoxLayout()
        self.savedPoseDataWidget.setLayout(self.savedPoseDataVLayout)
        self.savedPoseDataVLayout.setContentsMargins(0, 0, 0, 0)
        
        self.savedPoseLabel = QLabel("Saved Pose")
        self.savedPoseLabel.setFrameStyle(QFrame.Shape.StyledPanel)
        self.savedPoseDataVLayout.addWidget(self.savedPoseLabel)
        self.savedPoseLabel.setAlignment(Qt.AlignTop)
        
        self.poseList = QListWidget()
        self.savedPoseDataVLayout.addWidget(self.poseList)
        
        """#fliter view layout"""
        self.filterViewOptionsHLayout = QHBoxLayout()
        self.filterViewOptionsHLayout.setContentsMargins(0,0,0,0)
        self.savedPoseDataVLayout.addLayout(self.filterViewOptionsHLayout)
        self.filterViewOptionsHLayout.setAlignment(Qt.AlignTop)

        self.filtersGroupBox = QGroupBox()
        self.filtersGroupBox.setTitle("Filter By")
        self.filterOptionsHLayout = QHBoxLayout()
        self.filterOptionsHLayout.setContentsMargins(0,0,0,0)
        self.filtersGroupBox.setLayout(self.filterOptionsHLayout)
        self.filterOptionsHLayout.setAlignment(Qt.AlignLeft)
        self.filterOptionsHLayout.setSpacing(5)
        
        #self.filterViewOptionsHLayout.addWidget(self.filtersGroupBox)
        
        def createToolButton(iconPath="", text="", parentLayout=None):
            toolButton = QToolButton()
            icon = QIcon(iconPath)
            toolButton.setIcon(icon)
            toolButton.setIconSize(QSize(40,40))
            toolButton.setFixedWidth(80)
            toolButton.setAutoRaise(True)
            toolButton.setCheckable(True)
            toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
            toolButton.setText(text)
            return toolButton
        
        self.favouritesToolButton = createToolButton(os.path.join(config.ICON_DIR, "Fav.png"), "Favourites", parentLayout= self.filterOptionsHLayout)
        self.bodyPoseToolButton = createToolButton(os.path.join(config.ICON_DIR, "Body.png"), "Body", parentLayout = self.filterOptionsHLayout)
        self.handPoseToolButton = createToolButton(os.path.join(config.ICON_DIR, "Hands.png"), "Hand", parentLayout = self.filterOptionsHLayout)
        self.facePoseToolButton = createToolButton(os.path.join(config.ICON_DIR, "Face.png"), "Face", parentLayout = self.filterOptionsHLayout)
        
        self.filterOptionsHLayout.addWidget(self.favouritesToolButton)
        self.filterOptionsHLayout.addWidget(self.bodyPoseToolButton)
        self.filterOptionsHLayout.addWidget(self.handPoseToolButton)
        self.filterOptionsHLayout.addWidget(self.facePoseToolButton)
        
        self.filterViewOptionsHLayout.addWidget(self.filtersGroupBox)
        
        #view mode group
        self.viewModeGroupBox = QGroupBox()
        self.viewModeGroupBox.setTitle("View Mode")
        self.filterViewOptionsHLayout.addWidget(self.viewModeGroupBox)
        self.viewModeHLayout = QHBoxLayout()
        self.viewModeGroupBox.setLayout(self.viewModeHLayout)
        self.viewModeHLayout.setContentsMargins(0,0,0,0)
        self.viewModeButtonGroup = QButtonGroup()
        self.listViewToolButton = createToolButton(os.path.join(config.ICON_DIR, "ListView.png"), "ListView")
        self.iconViewToolButton = createToolButton(os.path.join(config.ICON_DIR, "IconView.png"), "IconView")
        # make two buttons exclusive to each other
        self.viewModeButtonGroup.addButton(self.listViewToolButton)
        self.viewModeButtonGroup.addButton(self.iconViewToolButton)
        self.listViewToolButton.setChecked(True)
        
        self.viewModeHLayout.addWidget(self.listViewToolButton)
        self.viewModeHLayout.addWidget(self.iconViewToolButton)
        
        #list view
        self.listViewFrame = QFrame()
        self.listViewHLayout = QHBoxLayout()
        self.listViewFrame.setLayout(self.listViewHLayout)
        
        self.poseListTableWidget = QTableWidget()
        self.listViewHLayout.addWidget(self.poseListTableWidget)
        self.poseListTableWidget.setColumnCount(5)
        poseListTableHeaders = ["Name", "Type", "Object Count", "Size", "Data Modified"]
        self.poseListTableWidget.setHorizontalHeaderLabels(poseListTableHeaders)
        self.poseListTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        # self.poseListTableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.poseListTableWidget.horizontalHeader().setStretchLastSection(True)
        # self.poseListTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        # self.poseListTableWidget.horizontalHeader().setMinimumSectionSize(300)
        
        #selectons utils
        self.poseListTableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.poseListTableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.poseListTableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.poseListTableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.poseListTableWidget.setSortingEnabled(True)
        self.listViewHLayout.addWidget(self.poseListTableWidget)
    
        #Icon view tab
        self.iconViewFrame = QFrame()
        self.iconViewVLayout = QVBoxLayout()
        self.iconViewVLayout.setContentsMargins(0,0,0,0)
        self.iconViewFrame.setLayout(self.iconViewVLayout)
        
        self.sortOptionsHLayout = QHBoxLayout()
        self.sortOptionsHLayout.setContentsMargins(0,0,0,0)
        self.iconViewVLayout.addLayout(self.sortOptionsHLayout)
        
        self.sortByLabel = QLabel('Sort by:')
        self.sortOptionsHLayout.addWidget(self.sortByLabel)
        
        self.sortOptionsComboBox = QComboBox()
        self.sortOptionsComboBox.addItems(config.SORTING_OPTIONS)
        self.sortOptionsHLayout.addWidget(self.sortOptionsComboBox)
        
        self.poseIconsListWidget = widgets.IconViewListWidget()
        self.iconViewVLayout.addWidget(self.poseIconsListWidget)
        self.savedPoseDataVLayout.addWidget(self.iconViewFrame)
        
        #set the layout to list view by default
        self.iconViewFrame.hide()
        
        self.savedPoseDataVLayout.addWidget(self.listViewFrame)
        
        #pose management
        self.manipulatedPoseOption = QWidget(self.mainSplitter)
        self.manipulatedPoseOptionVLayout = QVBoxLayout()
        self.manipulatedPoseOption.setLayout(self.manipulatedPoseOptionVLayout)
        self.manipulatedPoseOptionVLayout.setContentsMargins(0,0,0,0)
        
        self.manipulatedPoseLabel = QLabel("Pose Management")
        self.manipulatedPoseLabel.setFrameStyle(QFrame.Shape.StyledPanel)
        self.manipulatedPoseOptionVLayout.addWidget(self.manipulatedPoseLabel)
        self.manipulatedPoseOptionVLayout.setAlignment(Qt.AlignTop)
        
        """scroll area"""
        self.poseOptionsScrollArea = QScrollArea()
        self.poseOptionsScrollArea.setWidgetResizable(True)
        self.manipulatedPoseOptionVLayout.addWidget(self.poseOptionsScrollArea)
        self.poseOptionContentsWidget = QWidget()
        self.poseOptionsScrollArea.setWidget(self.poseOptionContentsWidget)
        self.poseOptionContentsVLayout = QVBoxLayout(self.poseOptionContentsWidget)
        self.poseOptionContentsVLayout.setContentsMargins(0,0,0,0)
        self.poseOptionContentsVLayout.setAlignment(Qt.AlignTop)
        
        #create overwrite group box
        self.poseOptionsGroupBox = QGroupBox()
        self.poseOptionsGroupBox.setTitle("Create / Overwrite Options")
        self.poseOptionsGroupBoxVLayout = QVBoxLayout()
        self.poseOptionsGroupBox.setLayout(self.poseOptionsGroupBoxVLayout)
        self.poseOptionsGroupBoxVLayout.setAlignment(Qt.AlignTop)
        self.poseOptionContentsVLayout.addWidget(self.poseOptionsGroupBox)
        
        #what to save sections
        self.whatToSaveOptionsVLayout = QVBoxLayout()
        self.whatToSaveOptionsLabel = QLabel("Save:")
        self.whatToSaveOptionsVLayout.addWidget(self.whatToSaveOptionsLabel)
        self.saveAllControlsRadioBtn = QRadioButton("All Controls")
        self.whatToSaveOptionsVLayout.addWidget(self.saveAllControlsRadioBtn)
        self.saveSelectedControlsRadioBtn = QRadioButton("Selected Controls")
        self.whatToSaveOptionsVLayout.addWidget(self.saveSelectedControlsRadioBtn)
        self.saveAllControlsRadioBtn.setChecked(True)
        
        self.poseOptionsGroupBoxVLayout.addLayout(self.whatToSaveOptionsVLayout)
        
        #check box section
        self.checkBoxVLayout = QVBoxLayout()
        self.createThumbnailCheckBox = QCheckBox("Use current view for pose thumbnails")
        self.checkBoxVLayout.addWidget(self.createThumbnailCheckBox)
        self.poseOptionsGroupBoxVLayout.addLayout(self.checkBoxVLayout)
        
        #pose name section
        self.poseNameVLayout = QVBoxLayout()
        self.poseNameLabel = QLabel("Pose Name")
        self.poseNameVLayout.addWidget(self.poseNameLabel)
        self.poseNameLineEdit = QLineEdit()
        self.poseNameVLayout.addWidget(self.poseNameLineEdit)
        self.createOverwritePushButton = QPushButton("Create/overwrite")
        self.poseNameVLayout.addWidget(self.createOverwritePushButton)
        
        self.poseOptionsGroupBoxVLayout.addLayout(self.poseNameVLayout)
        
        self.manipulatedPoseOptionVLayout.addLayout(self.poseOptionsGroupBoxVLayout)
        
        #apply options
        self.applyOptionsGroupBox = QGroupBox()
        self.applyOptionsGroupBox.setTitle("Apply Options")
        self.poseOptionContentsVLayout.addWidget(self.applyOptionsGroupBox)
        self.applyOptionsGroupBoxVLayout = QVBoxLayout()
        self.applyOptionsGroupBox.setLayout(self.applyOptionsGroupBoxVLayout)
        self.applyOptionsGroupBoxVLayout.setAlignment(Qt.AlignTop)
        
        #what to choose
        self.whatToChooseVLayout = QVBoxLayout()
        self.chooseAllControlsRadioBtn = QRadioButton("All Controls")
        self.chooseAllControlsRadioBtn.setChecked(True)
        self.whatToChooseVLayout.addWidget(self.chooseAllControlsRadioBtn)
        self.chooseSelectedControlsRadioBtn = QRadioButton("Selected Controls")
        self.whatToChooseVLayout.addWidget(self.chooseSelectedControlsRadioBtn)
        self.applyOptionsGroupBoxVLayout.addLayout(self.whatToChooseVLayout)
        
        #checkbox section
        self.controlsCheckBoxVLayout = QVBoxLayout()
        self.excludeRootAndMainControlsCheckBox = QCheckBox("Exclude Root and Main Controls")
        self.controlsCheckBoxVLayout.addWidget(self.excludeRootAndMainControlsCheckBox)
        self.keyPoseControlsCheckBox = QCheckBox("Key Pose Controls")
        self.controlsCheckBoxVLayout.addWidget(self.keyPoseControlsCheckBox)
        #self.applyOptionsGroupBoxVLayout.addLayout(self.controlsCheckBoxVLayout)
        
        #interactive blend
        self.interactiveBlendVLayout = QVBoxLayout()
        self.interactiveBlendLabel = QLabel("Interactive Blend")
        self.interactiveBlendVLayout.addWidget(self.interactiveBlendLabel)
        self.interactiveBlendSlider = QSlider(Qt.Horizontal)
        self.interactiveBlendVLayout.addWidget(self.interactiveBlendSlider)
        self.applyPushButton = QPushButton("Apply")
        self.interactiveBlendVLayout.addWidget(self.applyPushButton)
        #self.applyOptionsGroupBoxVLayout.addLayout(self.interactiveBlendVLayout)
        
        self.manipulatedPoseOptionVLayout.addLayout(self.applyOptionsGroupBoxVLayout)
        
    # button function apply on UI
    def initUIFunctions(self):
        self.charSelectionTreeWidget.itemClicked.connect(self.updatePoseView)
        self.viewModeButtonGroup.buttonClicked.connect(self.switchViewMode)
        self.sortOptionsComboBox.currentIndexChanged.connect(self.updatePoseView)
        # this is to config the char data, utils _getValidPoseFile, config_VALID EXTENSIONS
        self.poseListTableWidget.itemSelectionChanged.connect(self.onPoseSelectionChanged)
        self.createOverwritePushButton.clicked.connect(self.createOverwritePose)
        self.applyPushButton.clicked.connect(self.applyPose)
        self.poseListTableWidget.doubleClicked.connect(self.applyPose)
    
    # when we select a char in tree widget, we get the data in the charDirectory
    def getSelectedCharDirectory(self):
        selectedItem = self.charSelectionTreeWidget.getSelected()
        if not selectedItem:
            return None
        
        selectedChar = selectedItem[0].text(0)
        parent = selectedItem[0].parent()
        if not parent:
            return None
        
        #parent = selectedItem[0].parent().text(0)
        parentText = parent.text(0)
        charDirectory = os.path.join(config.PROJECT_ROOT, parentText, selectedChar)
        return charDirectory
    
    def switchViewMode(self, button):
        self.updatePoseView()
    
    def updatePoseView(self, *args):
        charDirectory = self.getSelectedCharDirectory()
        if not charDirectory:
            return
    
        if not os.path.exists(charDirectory):
            mc.warning("Directory does not exist: {}".format(charDirectory))
            return
        validPoseFiles = utils.getValidPoseFiles(os.listdir(charDirectory))
        poseDataDict = {}
        #get pose information
        for file in validPoseFiles:
            fullPosePath = os.path.join(charDirectory, file)
            poseFileInfo = utils.getPoseFileInformation(fullPosePath)
            poseName = poseFileInfo.get("poseName")
            
            # Read the actual pose data to get control count
            try:
                poseData = lib.readPoseData(fullPosePath)
                controlCount = len(poseData) if poseData else 0
                print("Pose '{}' has {} controls".format(poseName, controlCount))  # Debug print
                poseFileInfo["objectCount"] = controlCount
            except Exception as e:
                print("Error reading pose data for {}: {}".format(poseName, e))
                poseFileInfo["objectCount"] = 0
            
            poseDataDict[poseName] = poseFileInfo
        
        if self.listViewToolButton.isChecked():
            self.iconViewFrame.hide()
            self.listViewFrame.show()
            self.populateListView(poseDataDict)
        elif self.iconViewToolButton.isChecked():
            self.iconViewFrame.show()
            self.listViewFrame.hide()
            self.populateIconView(poseDataDict)
            
        # self.populateListView(poseDataDict)
        
    def filterPoseView(self):
        selectedChar = self.charTreeWidget.getSelectedText()
        favouriteChecked = self.favouritesToolButton.isChecked()
        handChecked = self.handPoseToolButton.isChecked()
        bodyChecked = self.bodyPoseToolButton.isChecked()
        faceChecked = self.facePoseToolButton.isChecked()
        
        favouritePoses = self.favouritePosesDict.get(selectedChar, [])
        posesDataDict = self.masterPosesDataDict.get(selectedChar)
        
        #update icon view
        if self.iconViewToolButton.isChecked():
            itemCount = self.poseIconsListWidget.count()
            for index in range(itemCount):
                item = self.poseIconsListWidget.item(index)
                widget = self.poseIconsListWidget.itemWidget(item)
                poseType = posesDataDict.get(widget.poseName).get("poseType")
                isFavourite = widget.poseName in favouritePoses
                
                #visibility logic
                showItem = True
                if favouriteChecked and not isFavourite:
                    showItem = False
                if bodyChecked and poseType != "Body":
                    showItem = False
                if handChecked and poseType != "Hand":
                    showItem = False
                if faceChecked and poseType != "Face":
                    showItem = False
                
                item.setHidden(not showItem)
        
        if self.listViewToolButton.isChecked():
            #update list view
            itemCount = self.poseListTableWidget.rowCount()
            for index in range(itemCount):
                item = self.poseListTableWidget.item(index, 0)
                poseType = posesDataDict.get(item.text()).get("poseType")
                isFavourite = item.text() in favouritePoses
                #visibility logic
                showRow = True
                if favouriteChecked and not isFavourite:
                    showRow = False
                if bodyChecked and poseType != "Body":
                    showRow = False
                if handChecked and poseType != "Hand":
                    showRow = False
                if faceChecked and poseType != "Face":
                    showRow = False
                
                if showRow:
                    self.poseListTableWidget.showRow(index)
                else:
                    self.poseListTableWidget.hideRow(index)
    
    def showPoseView(self):
        item = self.poseIconsListWidget.itemAt(position)
        if item:
            menu = QMenu()
            revealAction = menu.addAction("Reveal in Explorer")
            menu.addSeparator()
            renameAction = menu.addAction("Rename Pose")
            menu.addSeparator()
            deleteAction = menu.addAction("Delete Pose")
            action = menu.exec_(self.poseIconsListWidget.viewport().mapToGlobal(position))
            if action == deleteAction:
                self.deletePose(item)
            elif action == renameAction:
                self.renamePose(item)
            elif action == revealAction:
                self.revealPose(item)
                
    def deletePose(self, item):
        widget = self.poseIconsListWidget.itemWidget(item)
        poseData = widget.poseData
        poseName = widget.poseName
        # confirmation dialing
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete '{}' ?".format(poseName),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            filePath = poseData.get("fullPath")
            imgPath = poseData.get("imgFile")
            if filePath:
                utils.deleteFile(filePath)
            if imgPath:
                utils.deleteFile(imgPath)
        
        self.updatePoseView()
        
    def renamePose(self, item):
        widget = self.poseIconsListWidget.itemWidget(item)
        poseData = wdiget.poseData
        poseName = widget.poseName
        #get all the poses
        allPosesName = list(self.masterPosesDataDict.get(self.charTreeWidget.getSelectedText()).keys())
        newName, ok = QInputDialog.getText(self, "Rename Item", "Enter new name", text="")
        #ignore cases: windows explorer is not case-senstive
        if newName.lower() in (name.lower() for name in allPosesName):
            mc.warning("A pose with the name '{}' already exists".format(newName))
            return
        
        if ok and newName:
            filePath = poseData.get("fullPath")
            imgPath = poseData.get("imgFile")
            if filePath:
                utils.renameFile(filePath, newName)
            if imgPath:
                utils.renameFile(imgPath, newName)
            widget.poseLabel.setText(newName)
            #update favourite poses
            favouritePoses = self.favouritePosesDict.get(self.charTreeWidget.getSelectedText(), [])
            if poseName in favouritePoses:
                # Find the index of the pose to replace
                index = favouritePoses.index(poseName)
                favouritePoses[index] = newName
        self.updatePoseView()
    
    def revealPose(self, item):
        widget = self.poseIconsListWidget.itemWidget(item)
        poseData = widget.poseData
        filePath = poseData.get("fullPath", "")
        utils.revealFile(filePath)
        
    def populateListView(self, posesDataDict, selectedPoseName=None):
        allPoses = list(posesDataDict.keys())
        rowCount = len(allPoses)
        self.poseListTableWidget.setRowCount(rowCount)
        """
        If you want to set several items of a particular row (say, by calling in a loop),
        you may want to turn off sorting before doing so, and turn it back on afterwards;
        this will allow you to use the same row argument for all items in the same row (i.e. will not move the row).
        https://doc.qt.io/qtforpython-5/PySide2/QtWidgets/QTableWidget.html#PySide2.QtWidgets.PySide2.QtWidgets.QTableWidget.setItem
        """
        self.poseListTableWidget.setSortingEnabled(False)
        for poseName, poseInfo in posesDataDict.items():
            rowPosition = allPoses.index(poseName)
            #fill pose name
            poseNameItem = QTableWidgetItem(poseName)
            self.poseListTableWidget.setItem(rowPosition, 0, poseNameItem)
            
            #fill pose type
            poseTypeItem = QTableWidgetItem(poseInfo["poseType"])
            poseTypeItem.setTextAlignment(Qt.AlignCenter)
            self.poseListTableWidget.setItem(rowPosition, 1, poseTypeItem)
            
            #fill pose object count
            objectCountItem = QTableWidgetItem(str(poseInfo["objectCount"]))
            objectCountItem.setTextAlignment(Qt.AlignCenter)
            self.poseListTableWidget.setItem(rowPosition, 2, objectCountItem)
            
            #fill file size
            sizeItem = QTableWidgetItem(poseInfo["size"])
            sizeItem.setTextAlignment(Qt.AlignCenter)
            self.poseListTableWidget.setItem(rowPosition, 3, sizeItem)
            
            #fill modified time
            dateModifiedItem = QTableWidgetItem(poseInfo["mDate"])
            dateModifiedItem.setTextAlignment(Qt.AlignCenter)
            self.poseListTableWidget.setItem(rowPosition, 4, dateModifiedItem)
            
        #sort
        self.poseListTableWidget.setSortingEnabled(True)
        
        #resize contents to fit horizontal header
        self.poseListTableWidget.horizontalHeader().resizeSections(QHeaderView.ResizeToContents)
    
    def populateIconView(self, posesDataDict):
        #hide the widget so it avoids flicker
        self.poseIconsListWidget.hide()
        self.poseIconsListWidget.clear()
        sortedPosesDataDict = self.sortPoses(posesDataDict)
        for poseName, poseInfo in sortedPosesDataDict.items():
            item = QListWidgetItem(self.poseIconsListWidget)
            customWidget= widgets.IconViewListWidgetItem(poseName, poseInfo)
            item.setSizeHint(self.poseIconSize)
            self.poseIconsListWidget.addItem(item)
            self.poseIconsListWidget.setItemWidget(item, customWidget)
            
        self.poseIconsListWidget.show()
        
    def switchViewMode(self):
        self.updatePoseView()
    
    def sortPoses(self, posesDataDict):
        idx = self.sortOptionsComboBox.currentIndex()
        #Reorder dictionary based on keys in descending alphabetical order
        if idx == 0:
            # A -> Z
            sortedPosesDataDict = {k: posesDataDict[k] for k in sorted(posesDataDict.keys(), reverse = False)}
        elif idx == 1:
            # Z -> A
            sortedPosesDataDict = {k: posesDataDict[k] for k in sorted(posesDataDict.keys(), reverse = True)}
        elif idx == 2:
            #cDate ascending
            sortedPosesDataDict = {
                k: v for k, v in sorted(posesDataDict.items(), key=lambda item: item[1].get("cDate", ""), reverse = False)
            }
        elif idx == 3:
            #cDate descending
            sortedPosesDataDict = {
                k: v for k, v in sorted(posesDataDict.items(), key = lambda item: item[1].get("cDate", ""), reverse = True)
            }
        elif idx ==4:
            #mDate ascending
            sortedPosesDataDict = {
                k: v for k, v in sorted(posesDataDict.items(), key=lambda item: item[1].get("mDate", ""), reverse=False)
            }
        elif idx == 5:
            sortedPosesDataDict = {
                k: v for k, v in sorted(posesDataDict.items(), key=lambda item: item[1].get("mDate", ""), reverse=True)
            }
        else:
            sortedPosesDataDict = posesDataDict
        return sortedPosesDataDict
    
    def onPoseSelectionChanged(self):
        self.poseNameLineEdit.setText(self.getSelectedPoseName())
    
    def getSelectedPoseName(self):
        selectedPoseItem = self.poseListTableWidget.selectedItems()
        if selectedPoseItem:
            return selectedPoseItem[0].text()
        else:
            return ""
        
    def createOverwritePose(self):
        if not self.getSelectedCharDirectory():
            mc.warning("Please specify a character in the tree view for the pose!")
            return
        controls = []
        if self.saveAllControlsRadioBtn.isChecked():
            controls = lib.getControls(selection=False)
        elif self.saveSelectedControlsRadioBtn.isChecked():
            controls = lib.getControls(selection=True)
        if not controls:
            mc.warning("There are no controls specified for the pose!")
            return
        
        poseData = lib.getPoseData(controls=controls)
        poseName = self.poseNameLineEdit.text()
        if not poseName:
            mc.warning("Please provide a name for the pose!")
            return
        filepath = os.path.join(self.getSelectedCharDirectory(), "{}.pose".format(poseName))
        lib.writePoseData(filepath, poseData)
        print("Save '{}' pose data to {} with {} controls".format(poseName, filepath, len(poseData)))
        
        if self.createThumbnailCheckBox.isChecked():
            lib.createThumbnailFromCurrentView(poseName, self.getSelectedCharDirectory(), fileType="png")

        # Add confirmation if file exists
        filepath = os.path.join(charDirectory, "{}.pose".format(poseName))
        if os.path.exists(filepath):
            # Add confirmation dialog here
            pass

        self.updatePoseView()
        
    def applyPose(self):
        poseName = self.poseNameLineEdit.text()
        if not poseName:
            return
        filepath = os.path.join(self.getSelectedCharDirectory(), "{}.pose".format(poseName))
        poseData = lib.readPoseData(filepath)
        
        if self.chooseSelectedControlsRadioBtn.isChecked():
            controls = lib.getControls(selection=True)
        else:
            #apply to all
            controls = None
        excludeRootAndMainControls = self.excludeRootAndMainControlsCheckBox.isChecked()
        keyControls = self.keyPoseControlsCheckBox.isChecked()
        lib.applyPose(
            poseData,
            selectedControls = controls,
            excludeRootAndMainControls = self.excludeRootAndMainControlsCheckBox.isChecked(),
            keyControls = self.keyPoseControlsCheckBox.isChecked()
        )
    
    def readSettings(self):
        try:
            # Read position
            pos = self.generalSettings.value("win_pos", QPoint(200, 200))
            
            # Read and convert size
            default_size = QSize(1200, 750)
            width = self.generalSettings.value("win_width", 1200, type = int)
            height = self.generalSettings.value("win_height", 750, type = int)
            
            # Read splitter sizes
            default_splitter_sizes = [150, 750, 350]
            splitterSizes = self.generalSettings.value("splitter_sizes", default_splitter_sizes)
            if splitterSizes:
                try:
                    splitterSizes = [int(size) for size in splitterSizes]
                except (TypeError, ValueError):
                    splitterSizes = default_splitter_sizes

            # Apply settings
            self.mainSplitter.setSizes(splitterSizes)
            self.move(pos)
            self.resize(width, height)
            
            self.userSettings.beginGroup("Characters")
            selectedChar = self.userSettings.value("selectedChar", defaultValue = "", type = str)
            self.charSelectionTreeWidget.setSelectedItem(selectedChar)
            
            self.userSettings.endGroup()
            self.userSettings.sync()
            
            self.updatePoseView()
        except Exception as e:
            mc.warning("Error reading settings: {}".format(e))
               
    def writeSettings(self):
        self.generalSettings.setValue("splitter_sizes", self.mainSplitter.sizes())
        self.generalSettings.setValue("win_pos", self.pos())
        # Save size as separate width and height
        self.generalSettings.setValue("win_width", self.width())
        self.generalSettings.setValue("win_height", self.height())
        
        #clear previous settings
        self.userSettings.clear()
        #writes any unsaved changes to permanent storage,
        #and reloads any settings that have been changed in the meantime by another application.
        #self.userSettings.sync()
        
        self.userSettings.beginGroup("Characters")
        selectedItem = self.charTreeWidget.getSelected()
        selectedChar = selectedItem[0].text(0) if selectedItem else ""
        self.userSettings.setValue("selectedCharacter", selectedChar)
        self.userSettings.endGroup()
        
        self.userSettings.beginGroup("FilterViewOptions")
        self.userSettings.setValue("listView", self.listViewToolButton.isChecked())
        self.userSettings.setValue("iconView", self.ionViewToolButton.isChecked())
        self.userSettings.endGroup()
        
        self.userSettings.beginGroup("Favourite")
        for character, favouritePoses in self.favouritePosesDict.items():
            self.userSettings.setValue("{}".format(character), favouritePoses)
        self.userSettings.endGroup()
        self.userSettings.sync()
        
    def closeEvent(self, event):
        super().closeEvent(event)
        self.writeSettings()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        