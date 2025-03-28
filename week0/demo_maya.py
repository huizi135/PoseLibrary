from PySide2.QtWidgets import QApplication, QWidget, QMainWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from demo_output1 import Ui_Form

# Maya package
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance

def mayaMainWindow():
    """Retrieve Maya main window as PySide6 QWidget."""
    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(mayaMainWindowPtr), QWidget)

class DemoWindow(QMainWindow):
    def __init__(self, uiFile, parent = mayaMainWindow()):
        super(DemoWindow, self).__init__(parent)
        loader = QUiLoader()
        file = QFile(uiFile)
        
        file.open(QFile.ReadOnly)
        self.widget = loader.load(file)
        file.close()
        
        # Set the loaded UI as the central widget
        self.setCentralWidget(self.widget)
        self.resize(self.widget.size())
        
        # Connect signals
        self.widget.pushButton_2.clicked.connect(self.on_button_clicked)
    
    def on_button_clicked(self):
        print("Button clicked!")

class MainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent = mayaMainWindow()):
        super().__init__(parent)
        self.setupUi(self)  # Method from Ui_MainWindow that sets up the UI




