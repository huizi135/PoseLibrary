from PySide2.QtWidgets import QTreeWidget, QApplication, QTreeWidgetItem, QAbstractItemView, QLineEdit, QWidget, \
    QVBoxLayout, QTreeWidgetItemIterator, QListWidget, QListView, QListWidgetItem, QCheckBox, QHBoxLayout, QLabel, QHeaderView
from PySide2.QtGui import QFont, QImage, QPixmap, QColor
from PySide2.QtCore import Qt, Signal, QSize, QRect
from . import config
from . import utils
import os

# #TreeWidgetExample
# class TreeWidgetExample(QWidget):
#     def __init__(self):
#         super(TreeWidgetExample, self).__init__()
#
#         #create tree widget
#         self.tree = QTreeWidget()
#         self.tree.setColumnCount(1)
#         self.tree.setHeaderLabel(["Item"])
#
#         #add root items
#         root1 = QTreeWidgetItem(self.tree, ["Root 1"])
#         child1 = QTreeWidgetItem(root1, ["Child 1"])
#         child2 = QTreeWidgetItem(root1, ["Child 2"])
#
#         root2 = QTreeWidgetItem(self.tree, ["Root 2"])
#         child3 = QTreeWidgetItem(root2, ["Child 3"])
#         child4 = QTreeWidgetItem(root2, ["Child 4"])
#
#         self.tree.addTopLevelItem(root1)
#         self.tree.addTopLevelItem(root2)
#
#         # Expand all by default
#         self.tree.expandAll()
#
#         #connect selection change signal
#         self.tree.itemClicked.connect(self.on_item_clicked)
#
#         # Layout Setup
#         layout = QVBoxLayout()
#         layout.addWidget(self.tree)
#         self.setLayout(layout)
#
#     def on_item_clicked(self, item, column):
#         print("Current selected item is {}". format(item.text(column)))

class TreeWidget(QTreeWidget):
    def __init__(self, data, expandedCategory = None, parent=None):
        """Initialize the TreeWidget

        Args:
            data (dict): Tree data structure
            singleSelection (bool): Whether to allow single or multiple selection
            expandedCategory (str): Category to expand by default
            parent (QWidget): Parent widget
        """
        super(TreeWidget, self).__init__(parent = parent)
        self.data = data
        self.expandedCategory = expandedCategory or None
        
        
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.headerItem().setHidden(True)
        self.setMinimumSize(150, 350)
        
        self.populateTree()
        #connect itemCollapsed signal to the collapseAllCategories
        self.itemCollapsed.connect(self.collapseAllCategories)
        self.itemExpanded.connect(self.expandAllCategories)
        #connect itemClicked signal to the onItemClicked method
        self.itemClicked.connect(self.onItemClicked)
        
    def populateTree(self):
        """populate tree widget with the global dictionary"""
        self.clear()
        
        categories = sorted(self.data.keys())
        for category in categories:
            categoryItem = QTreeWidgetItem(self.invisibleRootItem())
            categoryItem.setText(0, category)
            
            #get characters from category
            chars = sorted(self.data[category], key=lambda name: name.lower())
            
            for char in chars:
                characterItem = QTreeWidgetItem(categoryItem)
                characterItem.setText(0, char)
                
            if category == self.expandedCategory:
                categoryItem.setExpanded(True)
            else:
                categoryItem.setExpanded(False)
                
    def collapseAllCategories(self):
        """collapse all the categories by shift click"""
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            self.collapseAll()
            
    def expandAllCategories(self):
        """expand all the categories by shift click"""
        if QApplication.keyboardModifiers() == Qt.ShiftModifier:
            root == self.invisibleRootItem()
            for i in range(root.childCount()):
                root.child(i).setExpanded(True)
            
    def onItemClicked(self, item, column):
        print("Current selected item is {}". format(item.text(column)))

class QSearchLineEdit(QLineEdit):
    def __init__(self, treeWidget, parent=None):
        """
        create a QLineEdit that finds matches over items in a QTreeWidget
        :param treeWidget: QTreeWidget
        :param resetExpandedStateAfterSearch: bool
        """
        super(QSearchLineEdit, self).__init__(parent=parent)
        self.setTreeWidget(treeWidget)
        self.setPlaceholderText("Search")
        self.textChanged.connect(self.search)
        
    def setTreeWidget(self, treeWidget):
        self.treeWidget = treeWidget
        
    def search(self, searchText):
        """string match, fuzzy search
        :param searchText: str
        """
        iterator = QTreeWidgetItemIterator(self.treeWidget, flags= QTreeWidgetItemIterator.Selectable)
        if searchText:
            while iterator.value():
                item = iterator.value()
                if searchText.lower() in item.text(0).lower():
                    item.setHidden(False)
                    parentItem = item.parent()
                    if parentItem:
                        parentItem.setHidden(False)
                        parentItem.setExpanded(True)
                else:
                    item.setHidden(True)
                iterator += 1
        else:
            for item in iterator:
                item.value().setHidden(False)
            
            self.treeWidget.collapseAll()
    
class SearchableTreeWidget(QWidget):
    """
    A tree widget with search functionality.
    
    Signals:
        itemChanged (str, str): Emitted when an item is changed (item text, parent text)
        itemClicked (QTreeWidgetItem, int): Emitted when an item is clicked
    """
    #itemChanged = Signal(str, str)
    itemClicked = Signal(QTreeWidgetItem, int)    #this is a clicked signal, trigger the function, itemClicked

    def __init__(self, data, parent=None):
        super(SearchableTreeWidget, self).__init__(parent=parent)
        self.data = data if data else {}
        self.initUI()

    

    def initUI(self):
        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(mainLayout)
        
        self.treeWidget = TreeWidget(data=self.data, )
        self.searchLineEdit = QSearchLineEdit(self.treeWidget)
        mainLayout.addWidget(self.searchLineEdit)
        mainLayout.addWidget(self.treeWidget)
        
        #self.treeWidget.currentItemChanged.connect(self.treeWidgetItemChanged)
        self.treeWidget.itemClicked.connect(self.treeWidgetItemClicked)

    # def treeWidgetItemChanged(self, current, previous):
    #     if current:
    #         currentText = current.text(0)
    #         currentParentText = current.parent().text(0) if current.parent() else ""
    #         self.itemChanged.emit(currentText, currentParentText)

    def treeWidgetItemClicked(self, item, column):
        #column = item.treeWidget().currentColumn()
        self.itemClicked.emit(item, column)

    def getSelected(self):
        return self.treeWidget.selectedItems()

    def getSelectedText(self):
        # single selection
        if self.getSelected():
            return self.getSelected()[0].text(0)
        else:
            return str()

    def setSelectedItem(self, itemText):
        items = self.treeWidget.findItems(itemText, Qt.MatchExactly | Qt.MatchRecursive)
        if items:
            item = items[0]
            # expand parent item if necessary
            parent = item.parent()
            while parent:
                self.treeWidget.expandItem(parent)
                parent = parent.parent()
            self.treeWidget.setCurrentItem(item)


class IconViewListWidgetItem(QWidget):
    favouriteChecked = Signal(str, bool)
    
    def __init__(self, poseName, poseData, width = 256, height = 256):
        super(IconViewListWidgetItem, self).__init__()
        self.initData(poseName, poseData)
        self.initAsset()
        self.initSize(width, height)
        self.initUI()
    
    def initData(self, poseName, poseData):
        self.poseName = poseName
        self.poseData = poseData
        imageFile = self.poseData.get("imgFile")
        self.imagePath = imageFile if os.path.exists(imageFile) else os.path.join(config.ICON_DIR, "noImage.png")
        self.isPoseFavourite = self.poseData.get("favourite", False)
    
    def initAsset(self):
        self.image = QImage(QImage(self.imagePath))
    
    def initSize(self, width, height):
        self.width = width
        self.height = height
        self.marginWidth = 0
        self.favoritesCheckBoxHeight = int(width * 0.1)
        self.poseLabelHeight = int(height * 0.1)
        self.imageWidth = self.width
        self.imageHeight = self.height - self.poseLabelHeight - self.favoritesCheckBoxHeight
    
    def initUI(self):
        self.overallLayout = QVBoxLayout()
        self.overallLayout.setContentsMargins(0, self.marginWidth, 0, self.marginWidth)
        self.overallLayout.setSpacing(0)
        self.overallLayout.setAlignment(Qt.AlignTop)
        
        self.iconsHorizontalLayout = QHBoxLayout()
        self.favoritesCheckBox = QCheckBox()
        self.favoritesCheckBox.setChecked(self.isPoseFavourite)
        self.favoritesCheckBox.stateChanged.connect(self.onFavouriteChecked)
        # if poseData.get('inFavorites'):
        #     self.favoritesCheckBox.setChecked(True)
        self.favoritesCheckBox.setLayoutDirection(Qt.RightToLeft)
        self.iconsHorizontalLayout.setAlignment(Qt.AlignVCenter)
        self.iconsHorizontalLayout.addWidget(self.favoritesCheckBox)
        self.overallLayout.addLayout(self.iconsHorizontalLayout)
        # self.favoritesCheckBox.setStyleSheet("background-color: blue;")
        
        self.poseImageLabel = QLabel(self)
        self.poseImageLabel.setMinimumSize(self.imageWidth, self.imageHeight)
        self.setImage()
        # self.poseImageLabel.setStyleSheet("background-color: yellow;")
        self.overallLayout.addWidget(self.poseImageLabel)
        
        self.poseInfoVerticalLayout = QVBoxLayout()
        self.poseLabel = QLabel(self.poseName)
        self.poseLabel.setAlignment(Qt.AlignCenter)
        self.poseLabel.setWordWrap(True)
        labelFont = QFont()
        labelFont.setBold(True)
        self.poseLabel.setFont(labelFont)
        self.poseLabel.setFixedHeight(self.poseLabelHeight)
        
        # self.poseLabel.setStyleSheet("background-color: blue;")
        self.poseInfoVerticalLayout.addWidget(self.poseLabel)
        
        self.overallLayout.addLayout(self.poseInfoVerticalLayout)
        
        self.loadStyleSheet()
        self.setLayout(self.overallLayout)
    
    def loadStyleSheet(self):
        checked = os.path.join(config.ICON_DIR, "like_checked.png").replace("\\", "/")
        unchecked = os.path.join(config.ICON_DIR, "like_unchecked.png").replace("\\", "/")
        
        style_sheet = (
            'QCheckBox::indicator {{ width: {}px; height: {}px; }}'
            'QCheckBox::indicator:checked {{image: url("{}"); }}'
            'QCheckBox::indicator:unchecked {{image: url("{}"); }}'
        ).format(self.favoritesCheckBoxHeight, self.favoritesCheckBoxHeight, checked, unchecked)
        
        self.favoritesCheckBox.setStyleSheet(style_sheet)
        # self.setStyleSheet("background-color: red;")
    
    def setImage(self):
        # Calculate the scale factor
        scale_factor = max(self.imageWidth / self.image.width(), self.imageHeight / self.image.height())
        # print(scale_factor)
        # print(self.image.width())
        # print(self.image.height())
        # print(self.imageWidth)
        # print(self.imageHeight)
        # Calculate the new size of the image
        new_width = int(self.image.width() * scale_factor)
        new_height = int(self.image.height() * scale_factor)
        
        # Scale the image
        scaled_image = self.image.scaled(new_width, new_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        
        # Calculate the rectangle for cropping the image
        crop_x = (new_width - self.imageWidth) // 2
        crop_y = (new_height - self.imageHeight) // 2
        crop_rect = QRect(crop_x, crop_y, self.imageWidth, self.imageHeight)
        # Crop the image
        cropped_image = scaled_image.copy(crop_rect)
        # Convert the cropped image to QPixmap and set it to QLabel
        pixmap = QPixmap.fromImage(cropped_image)
        self.poseImageLabel.setPixmap(pixmap)
        return cropped_image
    
    def resizeEvent(self, event):
        # perform custom actions when the widget is resized
        new_size = event.size()
        self.initSize(new_size.width(), new_size.height())
        #self.favoritesCheckBox.setFixedHeight(self.favoritesCheckBoxHeight)
        self.poseLabel.setFixedHeight(self.poseLabelHeight)
        self.loadStyleSheet()
        self.setImage()
        # Call the base class implementation
        super(self.__class__, self).resizeEvent(event)
    
    def onFavouriteChecked(self, *args):
        checked = self.favoritesCheckBox.isChecked()
        self.favouriteChecked.emit(self.poseName, checked)
    
    def isFavourite(self):
        return self.favoritesCheckBox.isChecked()
    
    def setFavourite(self, state):
        self.favoritesCheckBox.setChecked(state)
        
class IconViewListWidget(QListWidget):
    def __init__(self):
        super(IconViewListWidget, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setStyleSheet("""
            QListWidget::item {
                background-color: #5c5c5c;
                border-width: 2px;
                border-color: #eeeee4;
                border-style: solid;
            }
            QListWidget::item:selected {
                background-color: #1e81b0;
            }
        """)
        self.setWrapping(True)
        self.setViewMode(QListView.IconMode)
        self.setFlow(QListView.LeftToRight)
        self.setResizeMode(QListView.Adjust)
        
        # Improving Performance
        self.setUniformItemSizes(True)
        self.setDragEnabled(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setSpacing(2)
       
    def wheelEvent(self, event):
        if event.modifiers() & Qt.ControlModifier:
            angle = event.angleDelta().y()
            scaleFactor = angle / 120.0
            self.scaleItem(1 + scaleFactor * 0.1)
            event.accept()
        else:
            super(self.__class__, self).wheelEvent(event)
    
    def scaleItem(self, scaleFactor):
        # get all the list item
        for index in range(self.count()):
            item = self.item(index)
            # get current item size hint
            currentSize = item.sizeHint()
            # print(currentSize)
            newSize = [int(currentSize.width() * scaleFactor), int(currentSize.height() * scaleFactor)]
            minIconSize = [32, 32]
            if newSize < minIconSize:
                newSize = minIconSize
            
            item.setSizeHint(QSize(newSize[0], newSize[1]))
        self.doItemsLayout()
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    data = utils.folder_structure_to_dictionary()
    X = TreeWidget(data)
    # A = IconViewListWidgetItem(poseName="", poseData={
    #     "imgFile": ""})
    # B = IconViewListWidgetItem(poseName = "", poseData = {
    #     "imgFile": ""})
    
#     item1 = QListWidgetItem(X)
#     item1.setSizeHint(QSize(256, 256))
#     X.addItem(item1)
#     X.setItemWidget(item1, A)
#
#     item2 = QListWidgetItem(X)
#     item2.setSizeHint(QSize(256, 256))
#     X.addItem(item2)
#     X.setItemWidget(item2, B)
#
    X.show()
    # # Run the application event loop
    sys.exit(app.exec_())

        