from client.user_entities.user import User
from client.user_entities.utils import send_message
from client.user_entities.design_literals import admin_literal

class Admin(User):
    def perform_actions(self):
        while True:
            action = input(admin_literal)
            if action == 'ADD_USER':
                new_username = input("New username: ")
                new_password = input("New password: ")
                new_role = input("New role (admin/chef/employee): ")
                try:
                    add_user_response = send_message(self.client_socket, 'ADD_USER', {'username': new_username, 'password': new_password, 'role': new_role})
                    print(add_user_response)
                except ValueError as e:
                    print(e)
            elif action == 'LOGOUT':
                send_message(self.client_socket, 'LOGOUT', {})
                break
