from user_entities.user import User
from user_entities.utils import send_message, logout
from user_entities.design_literals import employee_literal
import handlers.employee_input_handler as input_handler
import time
import os

class Employee(User):

    def perform_actions(self, user_id):
        while True:
            action = input(employee_literal)
            if action == '1':
                self.view_meal()
            elif action == '2':
                self.give_vote_for_tomorrow(user_id)
            elif action == '3':
                self.view_feedback_dishes(user_id)
            elif action == '4':
                self.view_notification(user_id)
            elif action == '5':
                self.view_discard_meal_menu()
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



    def view_discard_meal_menu(self):
        try:
            response = send_message(self.client_socket, 'VIEW_DISCARD_MENU', {})
            print(f"{'ID':<15} {'NAME':<15}")
            meal_ids = []
            for data in response['data']:
                print(f"{data[0]:<15} {data[2]:<15}")
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
            print(f"{'ID':<5} {'NAME':<20} {'MEAL TYPE':<20} {'AVAILABILITY':<20} {'PRICE':<20} {'spice_level':<20} {'region':<20} {'vegetarian_status':<20}  ")
            for i in view_meal['data']:
                availability = "Available" if i['availability'] == 1 else "Not Available"
                print(f"{i['food_id']:<5} {i['food_name']:<20} {i['meal_type']:<20} {availability:<20} {i['price']:<20} {i['spice_level']:<20} {i['region']:<20} {i['vegetarian_status']:<20}")
        except ValueError as e:
            print(e)

    def give_vote_for_tomorrow(self,user_id):
        try:
            response = send_message(self.client_socket, 'VIEW_ROLLOUT_MEALS', {'user_id': user_id})
            if len(response['data'][0]) > 0:
                votes_id = []

                print(f"{'ID':<5} {'NAME':<20} {'meal_type':<20} {'PRICE':<20} {'spice_level':<20} {'region':<20} {'vegetarian_status':<20}  {'Status':<20}")
                for i in response['data'][0]:
                    status = 'Selected' if i[6] == '1' else " - "
                    print(f"{i[0]:<5} {i[1]:<20} {i[8]:<20} {i[2]:<20} {i[3]:<20} {i[4]:<20} {i[5]:<20} {status:<20}")
                    # print(i, i[0])
                    votes_id.append(i[0])

                if len(response['data'][1]) > 0:
                    print("You already voted. Please try tomorrow.")
                else:
                    choice = input("Do you want to vote yes/no ")
                    if choice == 'yes':
                        meal_ids = input_handler.collect_votes(votes_id)
                        vote_response = send_message(self.client_socket, 'VOTE_FOR_NEXT_DAY', {'meal_ids': meal_ids, 'user_id': user_id})
                        print(vote_response)
                    else:
                        return
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

    def view_notification(self,user_id):
        try:
            response = send_message(self.client_socket, 'VIEW_NOTIFICATION', {'user_id' : user_id})
            if len(response['data']) > 0:
                for i in response['data']:
                    print("------>" + i[1])
            else:
                print("There is no Notification for today")
        except ValueError as e:
            print(e)

