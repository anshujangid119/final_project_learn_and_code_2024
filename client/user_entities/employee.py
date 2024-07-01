from user_entities.user import User
from user_entities.utils import send_message
from user_entities.design_literals import employee_literal
import time
import os


class Employee(User):
    def perform_actions(self,user_id):
        os.system('cls')
        print(f"{'*' * 10} welcome {self.username} {'*' * 10}")
        while True:
            action = input(employee_literal)
            if action == '1':
                try:
                    view_meal = send_message(self.client_socket, 'VIEW_MEAL',{})
                    print(f"{'NAME':<15} {'MEAL TYPE':<15} {'AVAILABILITY':<15}")
                    for i in view_meal['data']:
                        availability = "Available" if i[3] == 1 else "Not Available"
                        print(f"{i[1]:<15} {i[2]:<15} {availability:<15}")
                except ValueError as e:
                    print(e)

            elif action == '2':
                try:
                    view_meal = send_message(self.client_socket, 'VIEW_USER_VOTES',{})
                    print(view_meal)
                    meal_ids = input("Enter Ids that you want to vote for tomorrow").split(",")
                    vote_response = send_message(self.client_socket, 'VOTE_FOR_NEXT_DAY', {'meal_ids': meal_ids})
                    print(vote_response)
                except ValueError as e:
                    print(e)

            elif action == '3':
                try:
                    view_meal = send_message(self.client_socket, 'VIEW_FEEDBACK_DISHES',{})
                    print(view_meal)
                    meal_id = input("Enter food Id for that you want to give feedback")
                    rating = input("Enter overall rating (1-5)")
                    quantity = input("Rate your satisfaction on quantity (1-5)")
                    quantity = input("Rate your satisfaction on quantity (1-5)")
                    value_for_money = input("Is your money worthy for this meal (1-5")
                    comment = input("Provide a comment so that we can improve ourself")
                    feedback_response = send_message(self.client_socket, 'RECEIVE_FEEDBACK',{'user_id' : user_id, 'meal_id':meal_id, 'rating':rating, 'quantity': quantity, 'quality':quantity, 'value_for_money': value_for_money, 'comment': comment})
                    print(feedback_response)
                except ValueError as e:
                    print(e)

            elif action == '4':
                self.close()
                time.sleep(2)
                os.system('cls')
                time.sleep(2)
                print("Logout Successfully")
                return