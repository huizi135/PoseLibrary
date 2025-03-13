from PySide2.QtCore import QObject, Signal, Slot
from PySide2.QtWidgets import QWidget, QPushButton, QApplication, QVBoxLayout

def custom_slot(message):
    print(f"Received message: {message}")
    
class MyWidget(QWidget):
    my_signal = Signal(str)
    
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button = QPushButton("demo")
        
        self.button.clicked.connect(self.on_button_clicked)
        self.my_signal.connect(custom_slot)
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.addWidget(self.button)
        
    @Slot()
    def on_button_clicked(self):
        print("Button clicked")
        self.my_signal.emit("hello, this is a signal from widget")
        
if __name__ == "__main__":
    app =QApplication([])
    window = MyWidget()
    window.show()
    app.exec_()
    
    