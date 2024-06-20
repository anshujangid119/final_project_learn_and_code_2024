from user_entities.user import User
from user_entities.utils import send_message

class Employee(User):
    def perform_actions(self):
        while True:
            action = input("Enter command (LOGOUT): ")
            if action == 'LOGOUT':
                send_message(self.client_socket, 'LOGOUT', {})
                break