import socket
from handlers.client_handler import ClientHandler

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")

        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = ClientHandler(client_socket, client_address)
            client_handler.start()
    def close(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Closing server socket")
        server_socket.close()
        print("Closing server socket")
if __name__ == "__main__":
    server = Server('0.0.0.0', 9998)
    print(server)
    server.start()
