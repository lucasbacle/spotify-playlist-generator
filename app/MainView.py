from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from MainViewController import *


class MainView(QWidget):

    def __init__(self):
        super().__init__()
        self.controller = MainViewController(self)
        self.setView()

    def setView(self):

        centerlayout = QGridLayout(self)

        centerlayout.setRowStretch(0, 0)
        centerlayout.setRowStretch(6, 0)

        centerlayout.setColumnMinimumWidth(0, 10)
        centerlayout.setColumnMinimumWidth(2, 10)

        self.slider1 = QSlider(Qt.Orientation.Horizontal)
        centerlayout.addWidget(self.slider1, 1, 1)

        self.slider2 = QSlider(Qt.Orientation.Horizontal)
        centerlayout.addWidget(self.slider2, 2, 1)

        self.slider3 = QSlider(Qt.Orientation.Horizontal)
        centerlayout.addWidget(self.slider3, 3, 1)

        self.slider4 = QSlider(Qt.Orientation.Horizontal)
        centerlayout.addWidget(self.slider4, 4, 1)

        self.button = QPushButton("&search", self)
        self.button.clicked.connect(
            lambda: self.controller.searchHandler())
        centerlayout.addWidget(self.button, 5, 1)

    def getSliderValues(self):
        result = []
        result.append(self.slider1.value())
        result.append(self.slider2.value())
        result.append(self.slider3.value())
        result.append(self.slider4.value())
        return result
