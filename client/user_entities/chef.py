from user_entities.user import User
from user_entities.utils import send_message, logout
from user_entities.design_literals import chef_literal
import handlers.chef_input_handler as input_handler_chef
import time
import os

class Chef(User):
    def perform_actions(self, user_id):
        while True:
            action = input(chef_literal)
            if action == '1':
                self.view_meal()
            elif action == '2':
                self.rollout_menu()
            elif action == '3':
                self.get_feedback()
            elif action == '4':
                self.select_next_day_meals()
            elif action == '5':
                self.generate_discard_menu()
            elif action == '6':
                self.get_discard_feedback()
            elif action == '7':
                logout(self)
                return

    def get_discard_feedback(self):
        response = send_message(self.client_socket, 'GET_DISCARD_FEEDBACK', {})
        print(f"{'FOOD ID':<5} {'FOOD NAME':<20} {'LIKED':<40} {'DISLIKED':<40} {'RECPIE':<40}")
        for item in response['data']:
            print(f"{item[1]:<5} {item[2]:<20} {item[4]:<40} {item[5]:<40} {item[6]:<40}")

    def generate_discard_menu(self):
        response = send_message(self.client_socket, 'GENERATE_DISCARD_MENU', {})
        discard_items = response['data']
        self.display_discard_menu(discard_items)

    def display_discard_menu(self, discard_items):
        # Print discard menu items
        print("Discard Menu Items:")
        print(f"{'FOOD ID':<5} {'FOOD NAME':<30}")
        menu_id_list = []
        for item in discard_items:
            menu_id_list.append(item[1])
            print(f"{item[1]:<15} {item[2]:<30}")

        while True:
            print("\nOptions:")
            print("1) Remove a Food Item from Menu List")
            print("2) Get Detailed Feedback")

            choice = input("Enter your choice (1 or 2): ").strip()
            if choice == '1':
                id = int(input("Enter ID of the food item you want to discard (one at a time): ").strip())
                if id in menu_id_list:
                    self.remove_food_item(id)
                    break
                else:
                    print("Invalid ID. Please enter a valid food ID from the discard menu.")
            elif choice == '2':
                id = int(input("Enter ID of the food item for which you want detailed feedback: ").strip())
                if id in menu_id_list:
                    self.get_detailed_feedback(id)
                    break
                else:
                    print("Invalid ID. Please enter a valid food ID from the discard menu.")
            else:
                print("Invalid choice. Please select 1 or 2.")

    def remove_food_item(self, id):
        response = send_message(self.client_socket, 'DELETE_MEAL', {'id':id})
        print(response)

    def get_detailed_feedback(self,id):
        response = send_message(self.client_socket, 'GET_DETAILED_FEEDBACK', {'id': id})
        print(response)

    def view_meal(self):
        try:
            view_meal = send_message(self.client_socket, 'VIEW_MEAL', {})
            print(f"{'ID':<5} {'NAME':<20} {'MEAL TYPE':<20} {'AVAILABILITY':<20} {'PRICE':<20} {'spice_level':<20} {'region':<20} {'vegetarian_status':<20}  ")
            for i in view_meal['data']:
                availability = "Available" if i['availability'] == 1 else "Not Available"
                print(f"{i['food_id']:<5} {i['food_name']:<20} {i['meal_type']:<20} {availability:<20} {i['price']:<20} {i['spice_level']:<20} {i['region']:<20} {i['vegetarian_status']:<20}")
        except ValueError as e:
            print(e)

    def rollout_menu(self):
        try:
            meal_number = input_handler_chef.get_meal_number()
            recommended_meals = send_message(self.client_socket, 'RECOMMEND_MEAL', {'meal_number': meal_number})

            breakfast_meals = recommended_meals['data']['breakfast']
            lunch_meals = recommended_meals['data']['lunch']
            dinner_meals = recommended_meals['data']['dinner']

            print("********* For Breakfast ***********")
            print(f"{'ID':<15}{'NAME':<15}{'AVG Rating':<15}{'AVG Composite Score':<15}")
            for i in breakfast_meals:
                print(f"{i['food_id']:<15}{i['food_name']:<15}{i['avg_rating']:<15}{i['avg_composite_score']:<15}")

            print("********* For Lunch ***********")
            print(f"{'ID':<15}{'NAME':<15}{'AVG Rating':<15}{'AVG Composite Score':<15}")
            for i in lunch_meals:
                print(f"{i['food_id']:<15}{i['food_name']:<15}{i['avg_rating']:<15}{i['avg_composite_score']:<15}")

            print("********* For Dinner ***********")
            print(f"{'ID':<15}{'NAME':<15}{'AVG Rating':<15}{'AVG Composite Score':<15}")
            for i in dinner_meals:
                print(f"{i['food_id']:<15}{i['food_name']:<15}{i['avg_rating']:<15}{i['avg_composite_score']:<15}")

            choice = input_handler_chef.confirm_choice("Do you want to see the available meals also? Press yes/no: ")
            if choice == 'yes':
                availability = 1
                view_meal = send_message(self.client_socket, 'VIEW_AVAILABLE_MEAL', {'availability': availability})
                print("These are the total meals that are available:")
                print(f"{'ID':<15}{'NAME':<15}{'MEAL TYPE':<15}{'AVAILABILITY':<15}")
                for i in view_meal['data']:
                    availability = "Available" if i[3] == 1 else "Not Available"
                    print(f"{i[0]:<15}{i[1]:<15}{i[2]:<15}{availability:<15}")

            meal_list = input_handler_chef.get_meal_list()
            roll_out_menu = send_message(self.client_socket, 'ROLL_OUT', {'meal_list': meal_list})
            print(roll_out_menu)

        except ValueError as e:
            print(e)

    def get_feedback(self):
        try:
            print("Following are the meals present in the database:")
            view_meal = send_message(self.client_socket, 'VIEW_MEAL', {})
            print(f"{'ID':<5} {'NAME':<20} {'MEAL TYPE':<20} {'AVAILABILITY':<20} {'PRICE':<20} {'spice_level':<20} {'region':<20} {'vegetarian_status':<20}  ")
            for i in view_meal['data']:
                availability = "Available" if i['availability'] == 1 else "Not Available"
                print(
                    f"{i['food_id']:<5} {i['food_name']:<20} {i['meal_type']:<20} {availability:<20} {i['price']:<20} {i['spice_level']:<20} {i['region']:<20} {i['vegetarian_status']:<20}")

            meal_ids = input_handler_chef.get_feedback_meal_ids()
            feedback_response = send_message(self.client_socket, 'RECIEVE_FEEDBACK', {'meal_ids': meal_ids})
            print(feedback_response)
        except ValueError as e:
            print(e)

    def select_next_day_meals(self):
        try:
            print("Following are the meals with employee votes. Now you have to select for tomorrow:")
            view_meal = send_message(self.client_socket, 'VIEW_USER_VOTES', {})
            print(f"{'ID':<15}{'NAME':<15}{'VOTE':<15}")
            meal_ids = []
            for i in view_meal['data']:
                meal_ids.append(i[0])
                print(f"{i[0]:<15}{i[1]:<15}{i[2]:<15}")

            choice = input_handler_chef.confirm_choice("Do you want to select now or wait for more votes? Press yes/no: ")
            if choice == 'yes':
                meal_ids = input_handler_chef.get_next_day_meal_ids(meal_ids)
                feedback_response = send_message(self.client_socket, 'NEXT_DAY_MEAL', {'meal_ids': meal_ids})
                print(feedback_response)
        except ValueError as e:
            print(e)



