import math
import base

from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QPixmap, QIcon


def _average(feature_name, result_features):
    count = 0
    sigma = 0.0
    for res_af in result_features:
        count += 1
        sigma += float(res_af[feature_name])

    result = sigma/count
    print("Average ", feature_name, " : ", str(result))


def _blend(blend_factor, rgb1, rgb2):
    r = math.sqrt((1 - blend_factor) * rgb1[0]**2 + blend_factor * rgb2[0]**2)
    g = math.sqrt((1 - blend_factor) * rgb1[1]**2 + blend_factor * rgb2[1]**2)
    b = math.sqrt((1 - blend_factor) * rgb1[2]**2 + blend_factor * rgb2[2]**2)
    return (r, g, b)


def _mean(*rgbs):
    r, g, b = 0, 0, 0
    count = 0
    for rgb in rgbs:
        count += 1
        r += rgb[0]
        g += rgb[1]
        b += rgb[2]

    return (r/count, g/count, b/count)


class SearchViewController():
    "Controller class for the search page"

    def __init__(self, v, sm, se, p):
        self.view = v
        self.spotify_manager = sm
        self.search_engine = se
        self.player = p

    def slider_handler(self, slider1, slider2, slider3, frame):
        rgb1 = _blend(slider1.value()/100,
                      base.RGB_SAD, base.RGB_HAPPY)
        rgb2 = _blend(slider2.value()/100, base.RGB_CALM,
                      base.RGB_EXCITED)
        rgb3 = _blend(slider3.value()/100,
                      base.RGB_SLOW, base.RGB_FAST)

        (r_f, g_f, b_f) = _mean(rgb1, rgb2, rgb3)

        frame.setStyleSheet(
            "background-color: rgb(" + str(r_f) + ", " + str(g_f) + ", " + str(b_f) + ")")

    def _verify_search(self, result):
        result_features = self.spotify_manager.get_audio_features(result)
        _average("valence", result_features)
        _average("danceability", result_features)
        _average("tempo", result_features)

    def search(self, slider1, slider2, slider3):

        result = self.search_engine.get_tracks_by_parameters(
            slider1.value()/100, slider2.value()/100, 30 + (slider3.value()*2.3)
        )

        # TODO: TO BE ERASED
        self._verify_search(result)

        if len(result) >= base.MIN_TRACKS_NUMBER:

            # Load the playlist in our player
            self.player.set_playlist(result)

            # Empty the list
            self.view.listWidget.clear()

            # Switch to the player view
            self.view.stackedWidget.setCurrentIndex(base.PLAYER_PAGE)

            # Add all the playlist to the listWidget
            playlist = self.spotify_manager.get_tracks(result)

            for track in playlist:
                track_str = track['artists'][0]['name'] + " - " + track['name']

                pixmap = QPixmap()
                content = self.spotify_manager.get_cover(track['uri'])
                if content is not None:
                    pixmap.loadFromData(content)

                self.view.listWidget.addItem(
                    QListWidgetItem(QIcon(pixmap), track_str))

            self.player.start_playback()
