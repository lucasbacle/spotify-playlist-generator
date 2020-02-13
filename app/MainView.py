from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainView(QWidget):

    def __init__(self):
        super().__init__()
        self.setView()

    def setView(self): 

        centerlayout = QGridLayout(self)

        centerlayout.setRowStretch(0,0)
        centerlayout.setRowStretch(6,0)

        centerlayout.setColumnMinimumWidth(0,10)
        centerlayout.setColumnMinimumWidth(2,10)

        slider1 = QSlider(Qt.Orientation.Horizontal)
        centerlayout.addWidget(slider1,1,1)

        slider2 = QSlider(Qt.Orientation.Horizontal)
        centerlayout.addWidget(slider2,2,1)

        slider3 = QSlider(Qt.Orientation.Horizontal)
        centerlayout.addWidget(slider3,3,1)

        slider4 = QSlider(Qt.Orientation.Horizontal)
        centerlayout.addWidget(slider4,4,1)
        
        button = QPushButton("&search", self)
        centerlayout.addWidget(button,5,1)
