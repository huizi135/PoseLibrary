from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from demo_output1 import Ui_Form

class DemoWindow(QMainWindow):
    def __init__(self, uiFile):
        super().__init__()
        loader = QUiLoader()
        file = QFile(uiFile)
        file.open(QFile.ReadOnly)
        self.widget = loader.load(file)
        
        file.close()
        self.setCentralWidget(self.widget)
        self.resize(self.widget.size())
        #self.widget.pushButton_2.clicked.connect(lambda x: print("Button clicked"))

class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    win = DemoWindow(uiFile = "demo.ui")
    win.show()
    
    sys.exit(app.exec_())
    
    