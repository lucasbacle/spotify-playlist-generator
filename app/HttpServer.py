from http.server import HTTPServer, BaseHTTPRequestHandler
import time

HOST_NAME = 'localhost'
PORT_NUMBER = 8000

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(b"<html><head><title>Title goes here.</title></head>")
        s.wfile.write(b"<body><p>This is a test.</p>")
        result = "<p>You accessed path: " + s.path + "</p>"
        s.wfile.write(result.encode())
        s.wfile.write(b"</body></html>")

class HttpServer:

    def __init__(self):
        server_class = HTTPServer
        httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
        print("Server Starts - " + HOST_NAME)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        print("Server Stops - " + HOST_NAME)

if __name__ == "__main__":
    HttpServer()
