from PyQt5.QtWidgets import QAction

class MainViewController(QAction):
    def __init__(self, view):
        self.view = view

    def searchHandler(self):
        values = self.view.getSliderValues()
        values[0] /= 100
        values[1] /= 100
        values[2] /= 100
        values[3] *= 180

        print("coucou " + values)

        # TODO : app.search
