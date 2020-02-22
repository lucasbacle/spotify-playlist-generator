import os
import random

# for testing purposes only:
from SpotifyManager import SpotifyManager


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

    def __init__(self, spotifyObject):
        self.spotifyObject = spotifyObject

        self.user = self.spotifyObject.current_user()
        self.userTopArtists = self.getTopArtists()
        self.userTopTracks = self.getTopTracks()

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

    def getTracksByParameters(self, valence, danceability, tempo):

        # generate the proper seed of artists, tracks & genre
        seed = self.generateSeed()

        # process the parameters
        print("Parameters: ")
        print(valence)
        print(danceability)
        print(tempo)
        
        # query Spotify
        tracks = self.spotifyObject.recommendations(
            seed_artists=seed['artists'],
            seed_genres=seed['genres'],
            seed_tracks=seed['tracks'],
            limit=50,
            country=self.user['country'],
            target_valence=valence,
            target_danceability=danceability,
            target_tempo = tempo
        )

        # prepare a list containing the uris
        result = []
        for track in tracks['tracks']:
            result.append(track['uri'])
        return result