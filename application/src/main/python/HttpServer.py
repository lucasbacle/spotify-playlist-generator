import base
import shutil
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler


class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:

            if self.path[:7] == "/?code=":
                self.server._set_code(self.path)
                path = base.context.get_resource("web/success.html")
            else:
                path = base.context.get_resource("web"+self.path)

            self.send_response(200)
            self.end_headers()

            # Send the correct ressource
            input_stream = open(path, 'rb')
            shutil.copyfileobj(input_stream, self.wfile)
            input_stream.close()

        except FileNotFoundError:
            print("Error : 404 not found")
            self.send_response(404)
            self.end_headers()

            try:
                # Send the 404 error page
                path = base.context.get_resource("web/404.html")

                input_stream = open(path, 'rb')
                shutil.copyfileobj(input_stream, self.wfile)
                input_stream.close()
            except (FileNotFoundError, IOError):
                pass

        except IOError:
            print("Error : Cannot open this file")
            self.send_response(403)
            self.end_headers()


class HttpServer(QObject, HTTPServer, Thread):

    token_received = pyqtSignal(str)

    def __init__(self, ip, port):
        super().__init__(server_address=(ip, port), RequestHandlerClass=HTTPRequestHandler)
        Thread.__init__(self)
        self.setDaemon(True)
        self.response_code = None
        self.start()

    def _set_code(self, code):
        self.response_code = code

    def code_received(self):
        return self.response_code is not None

    def read_code(self):
        result = self.response_code
        self.response_code = None
        return result

    def run(self):
        self.serve_forever()
