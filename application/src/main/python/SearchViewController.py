from PyQt5.QtWidgets import QAction
import math
import SearchView

class SearchViewController(QAction):
    def __init__(self, view):
        self.view = view

    def searchHandler(self):
        values = [self.view.slider1.value(), self.view.slider2.value(),
                  self.view.slider3.value()]
        values[0] /= 100
        values[1] /= 100
        values[2] = (values[2] * 2.3) + 30

        print(values)

        # TODO : app.search

    def _sliderToRgb(self, slider, rgb1, rgb2):
        t = slider.value()/100
        r = math.sqrt((1 - t) * rgb1[0]**2 + t * rgb2[0]**2)
        g = math.sqrt((1 - t) * rgb1[1]**2 + t * rgb2[1]**2)
        b = math.sqrt((1 - t) * rgb1[2]**2 + t * rgb2[2]**2)
        return (r, g, b)

    def sliderHandler(self):
        rgb1 = self._sliderToRgb(
            self.view.slider1, SearchView.RGB_SAD, SearchView.RGB_HAPPY)
        rgb2 = self._sliderToRgb(
            self.view.slider2, SearchView.RGB_CALM, SearchView.RGB_EXCITED)
        rgb3 = self._sliderToRgb(
            self.view.slider3, SearchView.RGB_SLOW, SearchView.RGB_FAST)
        (r_f, g_f, b_f) = self._mean(rgb1, rgb2, rgb3)
        self.view.parent().setStyleSheet("background-color: rgb(" +
                                         str(r_f) + ", " + str(g_f) + ", " + str(b_f) + ")")

    def _mean(self, rgb1, rgb2, rgb3):
        r = (rgb1[0]+rgb2[0]+rgb3[0])/3
        g = (rgb1[1]+rgb2[1]+rgb3[1])/3
        b = (rgb1[2]+rgb2[2]+rgb3[2])/3
        return (r, g, b)

    def _additive(self, rgb1, rgb2, rgb3):
        r = min(rgb1[0]+rgb2[0]+rgb3[0], 255)
        g = min(rgb1[1]+rgb2[1]+rgb3[1], 255)
        b = min(rgb1[2]+rgb2[2]+rgb3[2], 255)
        return (r, g, b)

    def _blend(self, rgb1, rgb2, rgb3, t):
        r = math.sqrt((1 - t) * rgb1[0]**2 + t * rgb2[0]**2)
        g = math.sqrt((1 - t) * rgb1[1]**2 + t * rgb2[1]**2)
        b = math.sqrt((1 - t) * rgb1[2]**2 + t * rgb2[2]**2)
        return (r, g, b)

    def _multiply(self, rgb1, rgb2, rgb3):
        r = (rgb1[0] * rgb2[0] * rgb3[0])/(255**2)
        g = (rgb1[1] * rgb2[1] * rgb3[1])/(255**2)
        b = (rgb1[2] * rgb2[2] * rgb3[2])/(255**2)
        return (r, g, b)
