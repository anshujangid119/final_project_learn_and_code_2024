from user_entities.user import User
from user_entities.utils import send_message
from user_entities.design_literals import employee_literal
class Employee(User):
    def perform_actions(self):
        while True:
            action = input(employee_literal)
            if action == '1':
                try:
                    view_meal = send_message(self.client_socket, 'VIEW_MEAL',{})
                    print("view_meal")
                    print(view_meal)
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
                    feedback_response = send_message(self.client_socket, 'RECEIVE_FEEDBACK',{'meal_id':meal_id, 'rating':rating, 'quantity': quantity, 'quality':quantity, 'value_for_money': value_for_money, 'comment': comment})
                    print(feedback_response)


                    vote_response = send_message(self.client_socket, 'GIVE_FEEDBACK_DISHES', {'meal_id': meal_id})
                    print(vote_response)
                except ValueError as e:
                    print(e)


            elif action == 'LOGOUT':
                send_message(self.client_socket, 'LOGOUT', {})
                break