from PyQt5.QtWidgets import *
from MainView import *
import sys


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.setUI()

        layout = QGridLayout()

        mainView = MainView()
        layout.addWidget(mainView, 0, 0)

        self.setLayout(layout)
        self.show()

    def setUI(self):
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip("Quitter l'application")
        exitAction.triggered.connect(qApp.exit)

        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle('Fenêtre principale')


if __name__ == '__main__':
    monApp = QApplication([])
    fenetre = Window()
    monApp.exec_()
    print("J'ai fini")
