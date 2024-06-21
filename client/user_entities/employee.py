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
                    print("hello")
                    view_meal = send_message(self.client_socket, 'VIEW_USER_VOTES',{})
                    print(view_meal)
                    meal_ids = input("Enter Ids that you want to vote for tomorrow").split(",")
                    vote_response = send_message(self.client_socket, 'VOTE_FOR_NEXT_DAY', {'meal_ids': meal_ids})
                    print(vote_response)
                except ValueError as e:
                    print(e)


            elif action == 'LOGOUT':
                send_message(self.client_socket, 'LOGOUT', {})
                break