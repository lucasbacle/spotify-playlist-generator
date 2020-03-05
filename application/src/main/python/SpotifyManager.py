import heapq
from datetime import date
import requests
import spotipy
import spotipy.util as util

from SpotifyOAuth import SpotifyCodeFlowManager


class SpotifyManager:

    client_id = '2ad3077e3bae46dca57d12a9eefd7239'
    client_secret = 'e4fc9fefe8cc4d918e80da6fc62b0fc3'
    redirect_uri = "http://localhost:8000/"

    scopes = ("user-read-private "
              "user-read-email "
              "playlist-modify-private "
              "user-top-read "
              "user-read-playback-state "
              "user-modify-playback-state")

    def __init__(self):
        self.spotify_object = None
        self.current_user = None
        self.spotify_oauth_manager = None

    # Auth-related stuff

    def authorize(self, username):
        self.spotify_oauth_manager = SpotifyCodeFlowManager(
            client_id=SpotifyManager.client_id,
            client_secret=SpotifyManager.client_secret,
            redirect_uri=SpotifyManager.redirect_uri,
            scope=SpotifyManager.scopes,
            username=username
        )

        token = util.prompt_for_user_token(
            username=username,
            oauth_manager=self.spotify_oauth_manager
        )

        self.spotify_object = spotipy.Spotify(auth=token)
        self.current_user = self.spotify_object.me()

    def is_authorized(self):
        return self.spotify_object is not None

    # User-related stuff

    def get_current_user_name(self):
        return self.current_user['display_name']

    def get_current_user_pic(self):
        pic_url = self.current_user['images'][0]['url']

        response = requests.get(
            pic_url,
            stream=True
        )

        if response.status_code == 200:
            return response.content
        else:
            return None

    def get_top_tracks(self):
        "Return current user's top 5 favourite tracks id"

        result = []

        fav_tracks = self.spotify_object.current_user_top_tracks(limit=5)[
            "items"]
        for track in fav_tracks:
            result.append(track["id"])

        return result

    def get_top_artists(self):
        "Return current user's top 5 favourite artists id"

        result = []

        fav_artists = self.spotify_object.current_user_top_artists(limit=5)[
            "items"]
        for artist in fav_artists:
            result.append(artist["id"])

        return result

    def get_top_genres(self):
        "Return current user's top 5 genres"

        genres = {}

        for i in range(0, 5):
            artists = []

            fav_tracks = self.spotify_object.current_user_top_tracks(
                limit=20, offset=(i*20))['items']
            for track in fav_tracks:
                artists.append(track['artists'][0]['id'])

            if len(artists) > 0:
                artists = self.spotify_object.artists(artists)['artists']
                for artist in artists:
                    for genre in artist['genres']:
                        genres.setdefault(genre, 0)
                        genres[genre] += 1

        # Sort genres by occurence (simple heap-sort)
        heap = []
        for key in genres:
            heapq.heappush(heap, (-(genres[key]), key))  # - for max heap

        result = []
        for j in range(0, 5):
            result.append(heapq.heappop(heap)[1])

        return result

    def save_playlist(self, uris):
        d = date.today()

        user_id = self.spotify_object.current_user()['id']

        self.playlist_id = self.spotify_object.user_playlist_create(
            user_id,
            "experience_" + str(d.day) + "_" +
            str(d.month) + "_" + str(d.year),
            public=False
        )['id']

        self.spotify_object.user_playlist_add_tracks(
            user_id, self.playlist_id, uris)

    # Data-related stuff

    def get_tracks(self, tracks_uri):
        tracks = self.spotify_object.tracks(tracks_uri)['tracks']
        return tracks

    def get_similar_tracks(self):
        "Return a list of related tracks uri"

    def get_audio_features(self, tracks_uri):
        audio_features = self.spotify_object.audio_features(tracks_uri)
        return audio_features

    def get_cover(self, track_uri):
        track = self.spotify_object.track(track_uri)

        response = requests.get(
            track['album']['images'][-1]['url'],
            stream=True
        )

        if response.status_code == 200:
            return response.content
        else:
            return None

    def get_title(self, track_uri):
        track = self.spotify_object.track(track_uri)
        return track['name']

    def get_artist(self, track_uri):
        track = self.spotify_object.track(track_uri)
        return track['artists'][0]['name']

    def get_similar_artists(self, a_id):
        "Return a list of related artists uri"

        related = self.spotify_object.artist_related_artists(artist_id=a_id)
        result = []

        for artist in related['artists']:
            result += artist['uri']

        return result

    def get_length(self, track_uri):
        track = self.spotify_object.track(track_uri)
        return int(track['duration_ms'])

    # Browsing-related stuff

    def get_recommendations(self, seed, valence, danceability, tempo):
        result = self.spotify_object.recommendations(
            seed_artists=seed['artists'],
            seed_genres=seed['genres'],
            seed_tracks=seed['tracks'],
            limit=50,
            country=self.current_user['country'],
            target_valence=valence,
            target_danceability=danceability,
            target_tempo=tempo
        )

        return result

    # Player-related stuff

    def get_devices_id(self):
        devices = self.spotify_object.devices()
        return devices['devices'][0]['id']

    def get_track_playing(self):
        track = self.spotify_object.current_user_playing_track()
        return track

    def is_playing(self):
        playback_state = self.spotify_object.current_playback()
        return bool(playback_state['is_playing'])

    def song_remaining_duration(self):
        "return the remaining song duration in ms"

        current_playing_track = self.spotify_object.current_user_playing_track()
        position = int(current_playing_track['progress_ms'])
        length = int(current_playing_track['item']['duration_ms'])

        return (length - position)

    def start_playback(self):
        self.spotify_object.start_playback()

    def pause_playback(self):
        self.spotify_object.pause_playback()

    def play_track(self, track_uri):
        self.spotify_object.start_playback(uris=[track_uri])
