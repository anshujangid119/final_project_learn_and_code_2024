import socket
import json
from user_entities.utils import send_message
import os

class User:
    def __init__(self, username, password, host='127.0.0.1', port=9998,):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        try:
            if not self.connected:
                self.client_socket.connect((self.host, self.port))
                self.connected = True
            auth_prompt = self.client_socket.recv(1024).decode()
            auth_response = send_message(self.client_socket, 'AUTH', {'username': self.username, 'password': self.password})
            if auth_response['command'] == 'AUTH_SUCCESS':
                user_id = auth_response['data']['id']
                role = auth_response['data']['role']
                print("="*10, f"Welcome {self.username}",f"({role}) Your Operations Are", "="*10)
                return role,user_id
            else:
                print("Authentication failed")
                self.close()
                return None
        except socket.error as e:
            print(f"Socket error: {e}")
            self.close()
            return None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            self.close()
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.close()
            return None

    def close(self):
        try:
            self.client_socket.close()
            self.connected = False
            print("logging out ......")
        except socket.error as e:
            print(f"Socket error during close: {e}")
        except Exception as e:
            print(f"Unexpected error during close: {e}")

    def perform_actions(self):
        raise NotImplementedError("Subclasses must implement this method")

