import sys
from SearchEngine import SearchEngine
from SpotifyManager import SpotifyManager
#from BluetoothManager import BluetoothManager
from Window import Window
from PyQt5.QtWidgets import QApplication




class App:

    def __init__(self):
        #self.bluetoothManager = BluetoothManager()

        monApp = QApplication([])
        self.window = Window()
        monApp.exec_()

        # TODO: display the login window

    def login(self, username):
        self.spotifyManager = SpotifyManager(username)
        self.searchEngine = SearchEngine(self.spotifyManager.spotifyObject)

        # TODO: display the search window

        return True

    def search(self, a, b, c, d):
        tracks_uris = self.searchEngine.getTracksByParameters(a, b, c, d)

        if len(tracks_uris) > 0:
            self.spotifyManager.createPlaylist(tracks_uris)
        else:
            print("No results")

        # TODO: display results on GUI

    def play(self):
        self.spotifyManager.start_playback()

    def pause(self):
        self.spotifyManager.pause_playback()

    def configure(self):
        # TODO
        pass


if __name__ == '__main__':
    app = App()

    if not app.login(input("Please input your Spotify username : ")):
        print("Login failed...")
        sys.exit(-1)

    fini = False
    while not fini:

        query = input("experience > ").lower()

        if (query[0:4] == "stop"):
            fini = True
        elif (query[0:6] == "search"):
            a = float(input("a (0 to 1) ?"))
            b = float(input("b (0 to 1) ?"))
            c = float(input("c (0 to 1) ?"))
            d = float(input("d (0 to 1) ?"))
            app.search(a, b, c, d)
        elif (query[0:4] == "play"):
            app.play()
        elif (query[0:5] == "pause"):
            app.pause()
        elif (query[0:9] == "configure"):
            app.configure()
        else:
            print("Need some help ? Here are the possible commands :")
            print("search energy valence mode tempo")
            print("play")
            print("pause")
            print("configure")
