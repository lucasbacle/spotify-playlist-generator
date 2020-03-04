import base

from PyQt5 import QtWidgets, uic

from SpotifyManager import SpotifyManager
from SearchEngine import SearchEngine
from Player import Player
from LoginViewController import LoginViewController
from SearchViewController import SearchViewController
from PlayerViewController import PlayerViewController


class MyApp(QtWidgets.QMainWindow):
    "Qt application main window"

    def __init__(self, ui, parent=None):
        super().__init__(parent)
        uic.loadUi(ui, self)

        self.spotify_manager = SpotifyManager()
        self.search_engine = SearchEngine(self.spotify_manager)
        self.player = Player(self.spotify_manager)

        self.login_view_controller = LoginViewController(
            self, self.spotify_manager, self.search_engine)
        self.search_view_controller = SearchViewController(
            self, self.spotify_manager, self.search_engine, self.player)
        self.player_view_controller = PlayerViewController(
            self, self.spotify_manager, self.player)

        self.set_login_handlers()
        self.set_search_handlers()
        self.set_player_handlers()

    def set_login_handlers(self):
        "Connect signals to the correct slot for the login page."

        self.loginButton.clicked.connect(lambda: self.login_view_controller.login(
            self.usernameLineEdit.text()
        ))

    def set_search_handlers(self):
        "Connect signals to the correct slot for the search page."

        self.slider1.valueChanged.connect(lambda: self.search_view_controller.slider_handler(
            self.slider1, self.slider2, self.slider3, self.searchFrame
        ))
        self.slider2.valueChanged.connect(lambda: self.search_view_controller.slider_handler(
            self.slider1, self.slider2, self.slider3, self.searchFrame
        ))
        self.slider3.valueChanged.connect(lambda: self.search_view_controller.slider_handler(
            self.slider1, self.slider2, self.slider3, self.searchFrame
        ))
        self.searchButton.clicked.connect(lambda: self.search_view_controller.search(
            self.slider1, self.slider2, self.slider3
        ))

    def set_player_handlers(self):
        "Connect signals to the correct slot for the player page."

        self.newSearchButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(base.SEARCH_PAGE)
        )
        self.logoutButton.clicked.connect(
            lambda: self.stackedWidget.setCurrentIndex(base.LOGIN_PAGE)
        )
        self.saveButton.clicked.connect(
            lambda: self.player_view_controller.save_playlist()
        )
        self.playButton.clicked.connect(
            lambda: self.player_view_controller.play_pause()
        )
        self.nextButton.clicked.connect(
            lambda: self.player_view_controller.next()
        )
        self.previousButton.clicked.connect(
            lambda: self.player_view_controller.previous()
        )
        self.listWidget.itemClicked.connect(
            lambda: self.player_view_controller.play_track(
                self.listWidget.currentRow())
        )
