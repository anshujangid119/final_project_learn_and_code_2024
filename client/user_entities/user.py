import socket
import json
from client.user_entities.utils import send_message

class User:
    def __init__(self, username, password, host='127.0.0.1', port=9999):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        if not self.connected:
            self.client_socket.connect((self.host, self.port))
            self.connected = True
        auth_prompt = self.client_socket.recv(1024).decode()
        print(auth_prompt)

        auth_response = send_message(self.client_socket, 'AUTH', {'username': self.username, 'password': self.password})
        print(auth_response)

        if auth_response['command'] == 'AUTH_SUCCESS':
            role = auth_response['data']['role']
            print(f"Logged in as {role}")
            return role
        else:
            print("Authentication failed")
            self.close()
            return None

    def close(self):
        if self.connected:
            self.client_socket.close()
            self.connected = False

    def perform_actions(self):
        raise NotImplementedError("Subclasses must implement this method")
