import os
import spotipy
import spotipy.util as util
import random

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


class SearchEngine:

    featuresDictionnary = {
        "acousticness": [],
        "danceability": [],
        "energy": [],
        "instrumentalness": [],
        "liveliness": [],
        "loudness": [],
        "speechiness": [],
        "valence": [],
        "key": [],
        "mode": [],
        "timesignature": []
    }

    """ Return a Spotify object """

    def authorizeSpotify(self, username):
        scope = 'user-read-private user-read-email user-top-read user-read-playback-state user-modify-playback-state'

        try:
            token = util.prompt_for_user_token(username, scope, client_id='2ad3077e3bae46dca57d12a9eefd7239',
                                               client_secret='e4fc9fefe8cc4d918e80da6fc62b0fc3', redirect_uri='http://localhost/')
        except (AttributeError):
            os.remove(f".cache-{username}")
            token = util.prompt_for_user_token(username, scope, client_id='2ad3077e3bae46dca57d12a9eefd7239',
                                               client_secret='e4fc9fefe8cc4d918e80da6fc62b0fc3', redirect_uri='http://localhost/')

        return spotipy.Spotify(auth=token)

    """ Convert engine parameters to features understandable by Spotify API """

    def rawToFeatures(self):
        pass

    """ Return current user's top 5 favourite tracks id """

    def getTopTracks(self):
        result = []

        favTracks = self.spotifyObject.current_user_top_tracks(limit=5)[
            "items"]
        for track in favTracks:
            result.append(track["id"])

        return result

    """ Return current user's top 5 favourite artists id """

    def getTopArtists(self):
        result = []

        favArtists = self.spotifyObject.current_user_top_artists(limit=5)[
            "items"]
        for artist in favArtists:
            result.append(artist["id"])

        return result

    """ Return a list of related tracks uri """

    def getSimilarTracks(self):

        pass

    """ Return a list of related artists uri """

    def getSimilarArtists(self, a_id):
        related = self.spotifyObject.artist_related_artists(artist_id=a_id)
        result = []

        for artist in related['artists']:
            result += artist['uri']

        return result

    def generateSeed(self):
        seed = {'artists': [], 'tracks': [], 'genres': []}

        # seed consists of :
        # - a bit of randomness
        rand = random.Random()
        rand.shuffle(self.userTopArtists)
        rand.shuffle(self.userTopTracks)

        # - user preferences        
        seed['artists'].append(self.userTopArtists[0])
        seed['tracks'].append(self.userTopArtists[0])

        # - developer preferences
        # TODO

        # - engine parameters to mix
        # TODO

        return seed

    def getTracksByFeatures(self):
        seed = self.generateSeed()
        tracks = self.spotifyObject.recommendations(
            seed_artists=seed['artists'],
            seed_genres=seed['genres'],
            seed_tracks=seed['tracks'],
            limit=50,
            country=self.user['country']
        )

        result = []
        for track in tracks['tracks']:
            print(track['artists'][0]['name'] + " - " + track['name'])
            result.append(track['uri'])
        return result

    def create_playlist(self, song_list):
        pass

    def __init__(self, username):
        self.spotifyObject = self.authorizeSpotify(username)
        self.user = self.spotifyObject.current_user()
        self.userTopArtists = self.getTopArtists()
        self.userTopTracks = self.getTopTracks()

        # Test code
        query = ""
        while not (query == "stop"):
            query = input("Que recherches-tu ? ")

            if (query == "recommandations"):
                self.getTracksByFeatures()

            elif (query != ""):
                track = self.spotifyObject.search(query, limit=1, type='track')[
                    'tracks']['items'][0]

                artist = track['artists'][0]['name']
                title = track['name']
                print("Spotify > " + artist + " - " + title)
                print("Spotify > Enjoy :)")

                uri = track['uri']
                self.spotifyObject.start_playback(uris=[uri])
