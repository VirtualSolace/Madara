from http.server import HTTPServer, BaseHTTPRequestHandler
# from http.cookies
from json import dump
from datetime import datetime

class OtsukaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/2002":
            self.path == "/index.html"
            
        try:
            with open(self.path.lstrip("/"), "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_error(404, "File Not Found")
        else:
            self.send_response(302)  # change later to 301 or 308
            self.send_header("Location", "https://www.google.com")
            self.end_headers()
    def do_POST(self):
        pass

def run(host="localhost", port=8080):
    server_info = (host, port)
    server = HTTPServer(server_info, OtsukaHandler)
    server.serve_forever()

if __name__ == "__main__":
    run()

