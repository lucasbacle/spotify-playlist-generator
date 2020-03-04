from threading import Timer
from PyQt5.QtCore import pyqtSignal, QObject


class Player(QObject):
    "This class represents our custom player for spotify"

    update_signal = pyqtSignal(int)
    play_signal = pyqtSignal()
    pause_signal = pyqtSignal()

    def __init__(self, sm):
        QObject.__init__(self)

        self.playlist = []
        self.playlist_index = 0
        self.spotify_manager = sm
        self.tim = None
        self.time_left = -1

    # Playlist-related stuff

    def set_playlist(self, tracks_uri):
        self.playlist = tracks_uri
        self.playlist_index = 0

    def get_playlist(self):
        return self.playlist

    def get_track(self, track_number):
        return self.playlist[track_number]

    # Playback-related stuff

    def start_playback(self, track_number=0):
        self.playlist_index = track_number
        self._play()

    def pause_resume_playback(self):
        if self.spotify_manager.is_playing():
            # save track position
            self.time_left = self.spotify_manager.song_remaining_duration()/1000

            # pause playback
            if self.tim is not None:
                self.tim.cancel()

            self.spotify_manager.pause_playback()
            self.pause_signal.emit()

        else:
            self.tim = Timer(self.time_left, self._next)
            self.spotify_manager.start_playback()
            self.tim.start()
            self.play_signal.emit()

    def next_track(self):
        self.playlist_index += 1

        playlist_size = len(self.playlist)
        if self.playlist_index >= playlist_size:
            self.playlist_index = playlist_size - 1
        else:
            self._play()

    def previous_track(self):
        self.playlist_index -= 1

        if self.playlist_index < 0:
            self.playlist_index = 0
        else:
            self._play()

    # Private stuff

    def _get_current_track(self):
        return self.playlist[self.playlist_index]

    def _next(self):
        if self.spotify_manager.is_playing():
            self.next_track()

    def _play(self):
        # Stop timer if any is running
        if self.tim is not None:
            self.tim.cancel()

        # Set timer to automatically pass to the next song
        song_length = self.spotify_manager.get_length(
            self._get_current_track())
        song_length /= 1000  # to sec
        self.tim = Timer(song_length, self._next)

        # Start the song
        self.spotify_manager.play_track(self._get_current_track())
        self.tim.start()

        # Emit signals
        self.update_signal.emit(self.playlist_index)
        self.play_signal.emit()
