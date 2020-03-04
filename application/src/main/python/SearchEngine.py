import random


class SearchEngine:
    "This class represent our custom spotify search-engine"

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

    def __init__(self, sm):
        self.spotify_manager = sm
        self.user_top_artists = None
        self.user_top_tracks = None
        self.user_top_genres = None

    def initialize(self):
        self.user_top_artists = self.spotify_manager.get_top_artists()
        self.user_top_tracks = self.spotify_manager.get_top_tracks()
        self.user_top_genres = self.spotify_manager.get_top_genres()

    def raw_to_features(self):
        "Convert engine parameters to features understandable by Spotify API"

    def generate_seed(self):
        "Generate a good seed to use in the following search"

        seed = {'artists': [], 'tracks': [], 'genres': []}

        # seed consists of :

        # - user preferences
        genres = self.user_top_genres
        tracks = self.user_top_tracks

        # - a bit of randomness
        rand = random.Random()
        rand.shuffle(genres)
        rand.shuffle(tracks)

        #seed['genres'].append(genres[0])
        seed['tracks'] = tracks

        # - developer preferences
        # TODO

        # - engine parameters to mix
        # TODO

        return seed

    def get_tracks_by_parameters(self, valence, danceability, tempo):
        "Returns a playlist based on the search parameters and user preferences"

        # generate the proper seed of artists, tracks & genre
        seed = self.generate_seed()

        # process the parameters
        print("Parameters: ")
        print("Valence : ", valence)
        print("Danceability : ", danceability)
        print("Tempo : ", tempo)

        # query Spotify
        tracks = self.spotify_manager.get_recommendations(seed, valence, danceability, tempo)['tracks']

        # prepare a list containing the uris
        result = []
        for track in tracks:
            result.append(track['uri'])
        return result
