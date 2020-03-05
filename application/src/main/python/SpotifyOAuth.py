from spotipy.oauth2 import SpotifyOAuth
from HttpServer import HttpServer


class SpotifyCodeFlowManager(SpotifyOAuth):

    def __init__(self, client_id, client_secret, redirect_uri, scope, username):

        SpotifyOAuth.__init__(
            self,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            scope=scope,
            username=username
        )

        self.http_server = HttpServer('localhost', 8000)

    def get_auth_response(self):

        auth_url = self.get_authorize_url()

        try:
            import webbrowser
            webbrowser.open(auth_url)
            print("Opened %s in your browser \n" % auth_url)
        except BaseException:
            print("Please navigate here: %s \n" % auth_url)

        while not self.http_server.code_received():
            pass

        response = self.http_server.read_code()

        return response
