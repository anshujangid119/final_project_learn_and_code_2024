from user_entities.user import User
from user_entities.utils import send_message, logout
from user_entities.design_literals import employee_literal
import handlers.employee_input_handler as input_handler
import time
import os

class Employee(User):
    def perform_actions(self, user_id):
        os.system('cls')
        print(f"{'*' * 10} welcome {self.username} {'*' * 10}")
        while True:
            action = input(employee_literal)
            if action == '1':
                self.view_meal()
            elif action == '2':
                self.view_user_votes(user_id)
            elif action == '3':
                self.view_feedback_dishes(user_id)
            elif action == '4':
                self.view_notification()
            elif action == '5':
                self.view_discard_menu()
            elif action == '6':
                self.update_profile(user_id)
            elif action == '7':
                logout(self)
                return

    def update_profile(self,user_id):
        response = send_message(self.client_socket, 'PROFILE_DATA', {'user_id':user_id})
        # print(response)
        print(f"your spice level is {response['data'][2]} and region is {response['data'][3]} and you are {response['data'][4]}")
        choice = input("do you want to change update this press: yes/no ")
        if choice == 'yes':
            spice_level = input("Choose your spice level from ('Mild', 'Medium', 'Hot')")
            region = input("Choose your region from ('South', 'North', 'Other')")
            vegetarian_status = input("Choose your vegetarian_status from ('Vegetarian', 'Non-Vegetarian', 'Eggetarian')")
            response = send_message(self.client_socket, 'UPDATE_PROFILE', {'spice_level': spice_level, 'region':region, 'vegetarian_status':vegetarian_status,'user_id':user_id})
            print(response)



    def view_discard_menu(self):
        try:
            response = send_message(self.client_socket, 'VIEW_DISCARD_MENU', {})
            print(f"{'ID':<15} {'NAME':<15}")
            meal_ids = []
            for data in response['data']:
                print(f"{data[1]:<15} {data[2]:<15}")
            # print(response['data'])
            if len(response['data']) > 0:
                discard_menu_id = input("enter id that you want to give feedback")
                like_text = input("what you liked about this")
                dislike_text = input("what you disliked about this")
                recipe = input("give your home recepie for this")
                feedback_response = send_message(
                    self.client_socket,
                    'DISCARD_ITEM_FEEDBACK',
                    {
                        'discard_menu_id': discard_menu_id,
                        'like_text': like_text,
                        'dislike_text': dislike_text,
                        'recipe': recipe
                    }
                )
                print(feedback_response)
            else:
                print("there is no item in discard menu for feedback.")



        except ValueError as e:
            print(e)

    def view_meal(self):
        try:
            view_meal = send_message(self.client_socket, 'VIEW_MEAL', {})
            print(f"{'NAME':<15} {'MEAL TYPE':<15} {'AVAILABILITY':<15}")
            for i in view_meal['data']:
                availability = "Available" if i[3] == 1 else "Not Available"
                print(f"{i[1]:<15} {i[2]:<15} {availability:<15}")
        except ValueError as e:
            print(e)

    def view_user_votes(self,user_id):
        try:
            response = send_message(self.client_socket, 'VIEW_ROLLOUT_MEALS', {'user_id': user_id})
            if len(response['data'][0]) > 0:
                print(f"{'ID':<15} {'Name':<15} ")
                votes_id = []
                for i in response['data'][0]:
                    print(f"{i[0]:<15} {i[1]:<15} {i[2]:<15}")
                    votes_id.append(i[0])
                if len(response['data'][1]) > 0:
                    print("You already voted. Please try tomorrow.")
                else:
                    meal_ids = input_handler.collect_votes(votes_id)
                    vote_response = send_message(self.client_socket, 'VOTE_FOR_NEXT_DAY', {'meal_ids': meal_ids, 'user_id': user_id})
                    print(vote_response)
            else:
                print("Chef has not rolled out the menu yet")
        except Exception as e:
            print(e)

    def view_feedback_dishes(self, user_id):
        try:
            response = send_message(self.client_socket, 'VIEW_FEEDBACK_DISHES', {})
            if len(response['data']) > 0:
                feedback_data = input_handler.collect_feedback(response['data'])
                feedback_response = send_message(
                    self.client_socket,
                    'RECEIVE_FEEDBACK',
                    {
                        'user_id': user_id,
                        'meal_id': feedback_data['meal_id'],
                        'rating': feedback_data['rating'],
                        'quantity': feedback_data['quantity'],
                        'quality': feedback_data['quality'],
                        'value_for_money': feedback_data['value_for_money'],
                        'comment': feedback_data['comment']
                    }
                )
                print(feedback_response)
            else:
                print("For today there is no item for feedback.")
        except ValueError as e:
            print(e)

    def view_notification(self):
        try:
            response = send_message(self.client_socket, 'VIEW_NOTIFICATION', {})
            for i in response['data']:
                print("------>" + i[0])
        except ValueError as e:
            print(e)

