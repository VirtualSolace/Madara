from http.server import HTTPServer
from MadaraHandler import MadaraHandler
import ssl

def run(host="localhost", port=8080):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(
        certfile="madara_cert.pem",
        keyfile="madara_key.pem"
    )

    server = HTTPServer((host, port), MadaraHandler)

    server.socket = context.wrap_socket(server.socket, server_side=True)

    print(f"Starting HTTPS server on port {port}")
    server.serve_forever()

if __name__ == "__main__":
    run()
