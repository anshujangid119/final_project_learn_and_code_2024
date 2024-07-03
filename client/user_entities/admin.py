from user_entities.user import User
from user_entities.utils import send_message
from user_entities.design_literals import admin_literal
import handlers.admin_input_handler as input_handler_admin
import os
import time

class Admin(User):
    def perform_actions(self, user_id):
        os.system('cls')
        print(f"{'*' * 10} welcome {self.username} {'*' * 10}")
        while True:
            action = input(admin_literal)
            if action == '1':
                self.add_user()
            elif action == '2':
                self.add_dish()
            elif action == '3':
                self.view_meal()
            elif action == '4':
                self.update_meal()
            elif action == '5':
                self.delete_meal()
            elif action == '6':
                self.logout()
                return

    def add_user(self):
        new_username, new_password, new_role = input_handler_admin.get_new_user_details()
        try:
            add_user_response = send_message(self.client_socket, 'ADD_USER', {
                'username': new_username,
                'password': new_password,
                'role': new_role
            })
            print(add_user_response['data'])
        except ValueError as e:
            print(e)

    def add_dish(self):
        meal_name, meal_type, availability = input_handler_admin.get_new_dish_details()
        try:
            add_dish_response = send_message(self.client_socket, 'ADD_DISH', {
                'meal_name': meal_name,
                'meal_type': meal_type,
                'availability': availability
            })
            print(add_dish_response)
        except ValueError as e:
            print(e)

    def view_meal(self):
        try:
            view_meal = send_message(self.client_socket, 'VIEW_MEAL', {})
            print(f"{'ID':<15} {'NAME':<15} {'MEAL TYPE':<15} {'AVAILABILITY':<15}")
            for i in view_meal['data']:
                availability = "Available" if i[3] == 1 else "Not Available"
                print(f"{i[0]:<15} {i[1]:<15} {i[2]:<15} {availability:<15}")
        except ValueError as e:
            print(e)

    def update_meal(self):
        meal_id = input_handler_admin.get_meal_id()
        availability = input_handler_admin.get_availability_status()
        try:
            update_meal_response = send_message(self.client_socket, 'UPDATE_MEAL', {
                'meal_id': meal_id,
                'availability': availability
            })
            print(update_meal_response)
        except ValueError as e:
            print(e)

    def delete_meal(self):
        meal_id = input_handler_admin.get_meal_id()
        try:
            delete_meal_response = send_message(self.client_socket, 'DELETE_MEAL', {
                'meal_id': meal_id
            })
            print(delete_meal_response)
        except ValueError as e:
            print(e)

    def logout(self):
        self.close()
        time.sleep(2)
        os.system('cls')
        time.sleep(2)
        print("Logout Successfully")
