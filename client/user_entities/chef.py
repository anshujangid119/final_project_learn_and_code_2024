from user_entities.user import User
from user_entities.utils import send_message
from user_entities.design_literals import chef_literal
import time
import os

class Chef(User):
    def perform_actions(self):
        while True:
            action = input(chef_literal)
            if action == '1':
                try:
                    view_meal = send_message(self.client_socket, 'VIEW_MEAL', {})
                    print(f"{'ID':<15} {'NAME':<15} {'MEAL TYPE':<15} {'AVAILABILITY':<15}")
                    for i in view_meal['data']:
                        availability = "Available" if i[3] == 1 else "Not Available"
                        print(f"{i[0]:<15} {i[1]:<15} {i[2]:<15} {availability:<15}")
                except ValueError as e:
                    print(e)


            elif action == '2':
                try:
                    availability = 1
                    view_meal = send_message(self.client_socket, 'VIEW_AVAILABLE_MEAL', {'availability': availability})
                    print("These are the total meals that are available for ")
                    print(f"{'ID':<15} {'NAME':<15} {'MEAL TYPE':<15} {'AVAILABILITY':<15}")
                    for i in view_meal['data']:
                        availability = "Available" if i[3] == 1 else "Not Available"
                        print(f"{i[0]:<15} {i[1]:<15} {i[2]:<15} {availability:<15}")
                    meal_list = input("Enter meal id's seprated by , :").split(",")
                    roll_out_menu = send_message(self.client_socket, 'ROLL_OUT', {'meal_list': meal_list})
                    print(roll_out_menu)

                except ValueError as e:
                    print(e)

            elif action == '3':
                try:
                    print("Followings are the meals that present in the database")
                    view_meal = send_message(self.client_socket, 'VIEW_MEAL', {})
                    print(f"{'ID':<15} {'NAME':<15} {'MEAL TYPE':<15} {'AVAILABILITY':<15}")
                    for i in view_meal['data']:
                        availability = "Available" if i[3] == 1 else "Not Available"
                        print(f"{i[0]:<15} {i[1]:<15} {i[2]:<15} {availability:<15}")
                    meal_ids = input("Enter Ids that you want to get feedback").split(",")
                    feedback_response = send_message(self.client_socket, 'RECIEVE_FEEDBACK', {'meal_ids': meal_ids})
                    print(feedback_response)
                except ValueError as e:
                    print(e)

            elif action == '4':
                try:
                    print("Followings are the meals with employee votes now you have to select for tomorrow")
                    view_meal = send_message(self.client_socket, 'VIEW_USER_VOTES', {})
                    print(view_meal)
                    meal_ids = input("Enter Ids that you want to select for tomorrow").split(",")
                    feedback_response = send_message(self.client_socket, 'NEXT_DAY_MEAL', {'meal_ids': meal_ids})
                    print(feedback_response)
                except ValueError as e:
                    print(e)

            elif action == '5':
                self.close()
                time.sleep(2)
                os.system('cls')
                time.sleep(2)
                print("Logout Successfully")
                return
