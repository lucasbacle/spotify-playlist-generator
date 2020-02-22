from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QIcon, QBrush, QImage, QPainter, QWindow
from PyQt5.QtWidgets import QListWidgetItem, QVBoxLayout, QWidget

from SearchEngine import SearchEngine
from SpotifyManager import SpotifyManager

import math
import requests

LOGIN_PAGE = 1
SEARCH_PAGE = 2
PLAYER_PAGE = 3

MIN_TRACKS_NUMBER = 5

#RGB_SAD = (38, 70, 83)
RGB_SAD = (255, 0, 255)
#RGB_HAPPY = (237, 106, 90)
RGB_HAPPY = (20, 255, 255)
RGB_CALM = (0, 255, 197)
RGB_EXCITED = (250, 243, 62)
RGB_SLOW = (144, 190, 109)
RGB_FAST = (232, 226, 136)


class MyApp(QtWidgets.QMainWindow):

    spotifyManager = None
    spotifyObject = None
    searchEngine = None

    def __init__(self, ui, parent=None):
        super().__init__(parent)
        uic.loadUi(ui, self)

        self.setLoginHandler()
        self.setSearchHandler()
        self.setPlayerHandler()

    def setLoginHandler(self):
        self.loginButton.clicked.connect(
            lambda: self._login(self.usernameLineEdit.text()))

    def setSearchHandler(self):
        self.slider1.valueChanged.connect(lambda: self._sliderHandler(
            self.slider1, self.slider2, self.slider3, self.searchFrame
        ))
        self.slider2.valueChanged.connect(lambda: self._sliderHandler(
            self.slider1, self.slider2, self.slider3, self.searchFrame
        ))
        self.slider3.valueChanged.connect(lambda: self._sliderHandler(
            self.slider1, self.slider2, self.slider3, self.searchFrame
        ))

        self.searchButton.clicked.connect(
            lambda: self._search(self.slider1, self.slider2, self.slider3))

    def setPlayerHandler(self):
        self.newSearchButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(1))
        self.logoutButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(0))

        # TODO: Play clicked song
        self.listWidget.itemClicked.connect(lambda:print(self.playlist[self.listWidget.currentRow()]['name']))

    # Login-view controller:

    def mask_image(self, imgdata, imgtype='jpg', size=128):
        """Return a ``QPixmap`` from *imgdata* masked with a smooth circle.

        *imgdata* are the raw image bytes, *imgtype* denotes the image type.

        The returned image will have a size of *size* × *size* pixels.

        """
        # Load image and convert to 32-bit ARGB (adds an alpha channel):
        image = QImage.fromData(imgdata, imgtype)
        image.convertToFormat(QImage.Format_ARGB32)

        # Crop image to a square:
        imgsize = min(image.width(), image.height())
        rect = QRect(
            (image.width() - imgsize) / 2,
            (image.height() - imgsize) / 2,
            imgsize,
            imgsize,
        )
        image = image.copy(rect)

        # Create the output image with the same dimensions and an alpha channel
        # and make it completely transparent:
        out_img = QImage(imgsize, imgsize, QImage.Format_ARGB32)
        out_img.fill(Qt.transparent)

        # Create a texture brush and paint a circle with the original image onto
        # the output image:
        brush = QBrush(image)        # Create texture brush
        painter = QPainter(out_img)  # Paint the output image
        painter.setBrush(brush)      # Use the image texture brush
        painter.setPen(Qt.NoPen)     # Don't draw an outline
        painter.setRenderHint(QPainter.Antialiasing, True)  # Use AA
        painter.drawEllipse(0, 0, imgsize, imgsize)  # Actually draw the circle
        painter.end()                # We are done (segfault if you forget this)

        # Convert the image to a pixmap and rescale it.  Take pixel ratio into
        # account to get a sharp image on retina displays:
        pr = QWindow().devicePixelRatio()
        pm = QPixmap.fromImage(out_img)
        pm.setDevicePixelRatio(pr)
        size *= pr
        pm = pm.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        return pm

    def _login(self, username):
        if username != "":
            self.spotifyManager = SpotifyManager(username)
            self.spotifyObject = self.spotifyManager.spotifyObject
            if self.spotifyObject != None:

                if self.searchEngine == None:
                    self.searchEngine = SearchEngine(self.spotifyObject)

                # Set user profile
                user = self.spotifyObject.current_user()
                
                # Set user picture
                r = requests.get(user['images'][0]['url'], stream=True)
                if r.status_code == 200:
                    pixmap = self.mask_image(r.content)
                    self.pictureLabel.setPixmap(pixmap)

                # Set user name
                self.usernameLabel.setText(user['display_name'])

                self.stackedWidget.setCurrentIndex(1)

    # Search-view controller:

    def _search(self, slider1, slider2, slider3):

        result = self.searchEngine.getTracksByParameters(
            slider1.value()/100, slider2.value()/100, 30 + (slider3.value()*2.3)
        )

        if len(result) >= MIN_TRACKS_NUMBER:

            # Add all the playlist to the listWidget
            for uri in result:
                track = self.spotifyObject.track(uri)

                self.playlist.append(track)

                trackStr = track['artists'][0]['name'] + " - " + track['name']
                pixmap = QPixmap()
                r = requests.get(track['album']['images'][2]['url'], stream=True)
                if r.status_code == 200:
                    pixmap.loadFromData(r.content)
                    self.listWidget.addItem(QListWidgetItem(QIcon(pixmap), trackStr))
                    self.coverLabel.setPixmap(pixmap.scaledToHeight(40))
                #self.listWidget.addItem(track)
            
            # Select first song
            firstTrack = self.spotifyObject.track(uri)
            self._playTrack(firstTrack)

            # Start playing
            self.playlistIndex = 0
            self.stackedWidget.setCurrentIndex(2)

    def _valueToRgb(self, sliderValue, rgb1, rgb2):
        t = sliderValue/100
        r = math.sqrt((1 - t) * rgb1[0]**2 + t * rgb2[0]**2)
        g = math.sqrt((1 - t) * rgb1[1]**2 + t * rgb2[1]**2)
        b = math.sqrt((1 - t) * rgb1[2]**2 + t * rgb2[2]**2)
        return (r, g, b)

    def _mean(self, rgb1, rgb2, rgb3):
        r = (rgb1[0]+rgb2[0]+rgb3[0])/3
        g = (rgb1[1]+rgb2[1]+rgb3[1])/3
        b = (rgb1[2]+rgb2[2]+rgb3[2])/3
        return (r, g, b)

    def _sliderHandler(self, slider1, slider2, slider3, frame):
        rgb1 = self._valueToRgb(slider1.value(), RGB_SAD, RGB_HAPPY)
        rgb2 = self._valueToRgb(slider2.value(), RGB_CALM, RGB_EXCITED)
        rgb3 = self._valueToRgb(slider3.value(), RGB_SLOW, RGB_FAST)

        (r_f, g_f, b_f) = self._mean(rgb1, rgb2, rgb3)

        frame.setStyleSheet(
            "background-color: rgb(" + str(r_f) + ", " + str(g_f) + ", " + str(b_f) + ")")

    # Player-view controller:
    playlistIndex = 0
    playlist = []

    def _play(self):
        self.spotifyManager.start_playback()
    
    def _playTrack(self, track):
        self.songLabel.setText(track['name'])
        self.artistLabel.setText(track['artists'][0]['name'])
        self.spotifyObject.start_playback(uris=[track['uri']])
        self._play()