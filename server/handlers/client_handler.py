import threading
import json
from databases.user_database import UserDatabase
from databases.dish_database import DishDatabase
from handlers.admin_command_handler import AdminCommandHandler
from handlers.chef_command_handler import ChefCommandHandler
from handlers.employee_command_handler import EmployeeCommandHandler
from handlers.default_command_handler import DefaultCommandHandler

class ClientHandler(threading.Thread):
    def __init__(self, client_socket, client_address):
        super().__init__()
        self.client_socket = client_socket
        self.client_address = client_address
        self.user_db = UserDatabase()
        self.dish_db = DishDatabase()

    def run(self):
        print(f"New connection from {self.client_address}")

        self.client_socket.send(self.create_message('AUTH', 'Please authenticate').encode())
        auth_message = self.client_socket.recv(1024).decode()
        print(f"Received authentication message: {auth_message}")
        parsed_auth_message = self.parse_message(auth_message)
        
        if parsed_auth_message is None:
            self.client_socket.send(self.create_message('AUTH_FAILURE', 'Invalid authentication message format').encode())
            self.client_socket.close()
            return

        username = parsed_auth_message['data']['username']
        password = parsed_auth_message['data']['password']
        print(f"Authenticating user: {username}")

        user_role = self.user_db.get_user_role(username, password)
        if user_role:
            self.client_socket.send(self.create_message('AUTH_SUCCESS', {'role': user_role}).encode())
        else:
            self.client_socket.send(self.create_message('AUTH_FAILURE', 'Invalid credentials').encode())
            self.client_socket.close()
            return

        handler = self.get_command_handler(user_role)
        handler.handle_commands()

        print(f"Connection from {self.client_address} closed")
        self.client_socket.close()

    def create_message(self, command, data):
        return json.dumps({'command': command, 'data': data})

    def parse_message(self, message):
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            return None

    def get_command_handler(self, user_role):
        if user_role == 'admin':
            return AdminCommandHandler(self.client_socket, self.user_db, self.dish_db)
        elif user_role == 'chef':
            return ChefCommandHandler(self.client_socket, self.dish_db)
        elif user_role == 'employee':
            return EmployeeCommandHandler(self.client_socket, self.dish_db)
        else:
            return DefaultCommandHandler(self.client_socket)
