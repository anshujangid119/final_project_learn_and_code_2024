from user_entities.user import User
from user_entities.utils import send_message
from user_entities.design_literals import admin_literal
import os
import time

class Admin(User):
    def perform_actions(self,user_id):
        os.system('cls')
        print(f"{'*' * 10} welcome {self.username} {'*' * 10}")
        while True:
            action = input(admin_literal)
            if action == '1':
                new_username = input("New username: ")
                new_password = input("New password: ")
                new_role = input("New role (admin/chef/employee): ")
                try:
                    add_user_response = send_message(self.client_socket, 'ADD_USER', {'username': new_username, 'password': new_password, 'role': new_role})
                    print(add_user_response['data'])
                except ValueError as e:
                    print(e)
            elif action == '2':
                meal_name = input("Enter Dish name: ")
                meal_type = input("Enter Dish Type:  1. For Breakfast 2. For Lunch 3. For Dinner")
                availability = input("is available yes/no")
                if availability == "yes":
                    availability = 1
                else:
                    availability = 0
                if meal_type == '1':
                    meal_type = "breakfast"
                elif meal_type == '2':
                    meal_type = "lunch"
                else:
                    meal_type = "dinner"
                try:
                    add_dish_response = send_message(self.client_socket, 'ADD_DISH', {'meal_name': meal_name, 'meal_type': meal_type, 'availability': availability})
                    print(add_dish_response)
                except ValueError as e:
                    print(e)
            elif action == '3':
                try:
                    view_meal = send_message(self.client_socket, 'VIEW_MEAL', {})
                    print(f"{'ID':<15} {'NAME':<15} {'MEAL TYPE':<15} {'AVAILABILITY':<15}")
                    for i in view_meal['data']:
                        availability = "Available" if i[3] == 1 else "Not Available"
                        print(f"{i[0]:<15} {i[1]:<15} {i[2]:<15} {availability:<15}")
                except ValueError as e:
                    print(e)
            if action == '4':
                meal_id = int(input("Enter meal id "))
                availability = int(input("Enter availability status"))
                try:
                    update_meal_response = send_message(self.client_socket, 'UPDATE_MEAL', {'meal_id': meal_id, 'availability': availability})
                    print(update_meal_response)
                except ValueError as e:
                    print(e)

            if action == '5':
                meal_id = int(input("Enter meal id "))
                try:
                    delete_meal_response = send_message(self.client_socket, 'DELETE_MEAL', {'meal_id': meal_id})
                    print(delete_meal_response)
                except ValueError as e:
                    print(e)


            elif action == '6':
                self.close()
                time.sleep(2)
                os.system('cls')
                time.sleep(2)
                print("Logout Successfully")
                return
