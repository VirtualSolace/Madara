from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from json import dump
from datetime import datetime
from dotenv import load_dotenv
import os

def get_env_info():
    load_dotenv()
    PATH = os.getenv("C_PATH")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    COOKIE_VALUE = os.getenv("COOKIE_VALUE")
    return PATH, ACCESS_TOKEN, COOKIE_VALUE

class OtsukaHandler(BaseHTTPRequestHandler):
    def redirectGoogle(self, url, code=302):
        self.send_response(code)  # change later to 301 or 308
        self.send_header("Location", url)
        self.end_headers()

    def cookieInfo(self):
        cookie_header = self.headers.get("Cookie")
        cookie = SimpleCookie(cookie_header)
        correct_cookie = cookie.get("name")
        return correct_cookie.value if correct_cookie else None

    def do_GET(self):

        PATH,ACCESS_TOKEN,COOKIE_VALUE = get_env_info()
        correct_cookie = self.cookieInfo()

        if (
            self.path == PATH
            and correct_cookie == COOKIE_VALUE
            and self.headers["X-Access-Token"] == ACCESS_TOKEN
        ):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
        else:
             self.redirectGoogle("https://www.google.com")
    def do_POST(self):
        pass

def run(host="localhost", port=8080):
    server_info = (host, port)
    server = HTTPServer(server_info, OtsukaHandler)
    print(f"Starting server on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    run()

