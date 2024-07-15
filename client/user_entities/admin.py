from user_entities.user import User
from user_entities.utils import send_message, logout
from user_entities.design_literals import admin_literal
import handlers.admin_input_handler as input_handler_admin


class Admin(User):
    def perform_actions(self, user_id):
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
                logout(self)
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
        meal_name, meal_type, availability, price, spice_level, region, vegetarian_status = input_handler_admin.get_new_dish_details()
        try:
            add_dish_response = send_message(self.client_socket, 'ADD_DISH', {
                'meal_name': meal_name,
                'meal_type': meal_type,
                'availability': availability,
                'price': price,
                'spice_level':spice_level,
                'region':region,
                'vegetarian_status':vegetarian_status
            })
            print(add_dish_response['data'])
        except ValueError as e:
            print(e)

    def view_meal(self):
        try:
            view_meal = send_message(self.client_socket, 'VIEW_MEAL', {})
            print(f"{'ID':<5} {'NAME':<20} {'MEAL TYPE':<20} {'AVAILABILITY':<20} {'PRICE':<20} {'spice_level':<20} {'region':<20} {'vegetarian_status':<20}  ")
            for i in view_meal['data']:
                availability = "Available" if i['availability'] == 1 else "Not Available"
                print(f"{i['food_id']:<5} {i['food_name']:<20} {i['meal_type']:<20} {availability:<20} {i['price']:<20} {i['spice_level']:<20} {i['region']:<20} {i['vegetarian_status']:<20}")
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

