from user_entities.user import User
from user_entities.utils import send_message

class Chef(User):
    def perform_actions(self):
        while True:
            action = input("Enter command (ADD_DISH/LOGOUT): ")
            if action == 'ADD_DISH':
                dish_name = input("Dish name: ")
                ingredients = input("Ingredients: ")
                try:
                    add_dish_response = send_message(self.client_socket, 'ADD_DISH', {'name': dish_name, 'ingredients': ingredients})
                    print(add_dish_response)
                except ValueError as e:
                    print(e)
            elif action == 'LOGOUT':
                send_message(self.client_socket, 'LOGOUT', {})
                break
