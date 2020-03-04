import base
from PyQt5.QtGui import QPixmap, QIcon


class PlayerViewController():
    "Controller class for the player page"

    def __init__(self, v, sm, p):
        self.view = v
        self.spotify_manager = sm
        self.player = p

        self.pause_button_ico = QIcon(QPixmap(base.context.get_resource("images/pause.png")))
        self.play_button_ico = QIcon(QPixmap(base.context.get_resource("images/play.png")))

        self.player.update_signal.connect(self._update)
        self.player.pause_signal.connect(self._pausing)
        self.player.play_signal.connect(self._playing)

    def play_pause(self):
        self.player.pause_resume_playback()

    def next(self):
        self.player.next_track()

    def previous(self):
        self.player.previous_track()

    def play_track(self, track_number):
        # Start playback
        self.player.start_playback(track_number)

    def save_playlist(self):
        self.spotify_manager.save_playlist(self.player.get_playlist())

    # Private stuff

    def _playing(self):
        self.view.playButton.setIcon(self.pause_button_ico)

    def _pausing(self):
        self.view.playButton.setIcon(self.play_button_ico)

    def _update(self, track_number):

        # Highlight track in the list
        self.view.listWidget.item(track_number).setSelected(True)
        
        # Display track in the player
        self.view.songLabel.setText(
            self.spotify_manager.get_title(self.player.get_track(track_number)))
        self.view.artistLabel.setText(
            self.spotify_manager.get_artist(self.player.get_track(track_number)))

        raw_cover = self.spotify_manager.get_cover(self.player.get_track(track_number))
        pix = QPixmap()
        if raw_cover is not None:
            pix.loadFromData(raw_cover)

        self.view.coverLabel.setPixmap(pix.scaledToHeight(40))
