import spotipy
import spotipy.util as util
import os
from datetime import date

"""
" Return currently playing device "
def getDevicesId():
    devices = self.spotifyObject.devices()
    return devices['devices'][0]['id']

" Return currently playing track "
def getTrackPlaying():
    track = self.spotifyObject.current_user_playing_track()
    return track
"""

class SpotifyManager:

    client_id = '2ad3077e3bae46dca57d12a9eefd7239'
    client_secret = 'e4fc9fefe8cc4d918e80da6fc62b0fc3'

    scope = 'user-read-private user-read-email playlist-modify-private user-top-read user-read-playback-state user-modify-playback-state'

    def __init__(self, username):
        self.spotifyObject = self.authorize(username)

    def authorize(self, username):
        try:
            token = util.prompt_for_user_token(
                username,
                self.scope,
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri='http://localhost:8000/'
            )

        except (AttributeError):
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(
                username,
                self.scope,
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri='http://localhost:8000/'
            )

        return spotipy.Spotify(auth=token)

    def createPlaylist(self, uris):
        d = date.today()

        user_id = self.spotifyObject.current_user()['id']

        self.playlist_id = self.spotifyObject.user_playlist_create(
            user_id,
            "experience_" + str(d.day) + "_" +
            str(d.month) + "_" + str(d.year),
            public=False
        )['id']

        self.spotifyObject.user_playlist_add_tracks(
            user_id, self.playlist_id, uris)
        self.spotifyObject.start_playback(
            context_uri="spotify:playlist:"+self.playlist_id)

    def start_playback(self):
        self.spotifyObject.start_playback()

    def pause_playback(self):
        self.spotifyObject.pause_playback()
