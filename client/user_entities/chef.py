from user_entities.user import User
from user_entities.utils import send_message
from user_entities.design_literals import chef_literal, chef_roll_out

class Chef(User):
    def perform_actions(self):
        while True:
            action = input(chef_literal)
            if action == '1':
                try:
                    view_meal = send_message(self.client_socket, 'VIEW_MEAL',{})
                    print("view_meal")
                    print(view_meal)
                except ValueError as e:
                    print(e)


            elif action == '2':
                try:
                    availability = 1
                    view_meal = send_message(self.client_socket, 'VIEW_AVAILABLE_MEAL', {'availability': availability})
                    print("These are the total meals that are available for ")
                    print(view_meal)
                    meal_list = input("Enter meal id's seprated by , :").split(",")
                    roll_out_menu = send_message(self.client_socket, 'ROLL_OUT', {'meal_list': meal_list})
                    print(roll_out_menu)

                except ValueError as e:
                    print(e)

            elif action == 'LOGOUT':
                send_message(self.client_socket, 'LOGOUT', {})
                break
