import json
import time
class AdminCommandHandler:
    def __init__(self, client_socket, user_db, dish_db):
        self.client_socket = client_socket
        self.user_db = user_db
        self.dish_db = dish_db

    def handle_commands(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break

                parsed_message = self.parse_message(message)
                if parsed_message is None:
                    continue
                
                if parsed_message['command'] == 'LOGOUT':
                    break
                elif parsed_message['command'] == 'ADD_USER':
                    self.handle_add_user(parsed_message)
                elif parsed_message['command'] == 'ADD_DISH':
                    self.handle_add_meal(parsed_message)
                elif parsed_message['command'] == 'VIEW_MEAL':
                    print("inside view")
                    self.handle_view_meal(parsed_message)
            except Exception as e:
                print(f"Error: {e}")
                break
    def handle_view_meal(self,message):
        # meal_list = self.dish_db.view_meal()
        #
        # if meal_list:
        #     self.client_socket.send("Food Items:\n".encode())
        #     for item in meal_list:
        #         # print(f"Sending item: {item}")  # Debugging statement
        #         self.client_socket.send(item.encode())
        #         time.sleep(0.1)

        meal_list = self.dish_db.view_meal()

        response = {
            'command': 'VIEW_MEAL',
            'data': meal_list
        }

        # Convert the response to JSON format
        json_response = json.dumps(response)

        # Send the JSON response
        self.client_socket.send(json_response.encode())
    def handle_add_meal(self, message):
        new_meal = message['data']
        if self.dish_db.add_meal(new_meal['meal_name'], new_meal['meal_type'], new_meal['availability']):
            self.client_socket.send(self.create_message('ADD_MEAL_SUCCESS', 'meal added successfully').encode())
    def handle_add_user(self, message):
        new_user = message['data']
        if self.user_db.add_user(new_user['username'], new_user['password'], new_user['role']):
            self.client_socket.send(self.create_message('ADD_USER_SUCCESS', 'User added successfully').encode())
        else:
            self.client_socket.send(self.create_message('ADD_USER_FAILURE', 'User already exists').encode())

    def create_message(self, command, data):
        return json.dumps({'command': command, 'data': data})

    def parse_message(self, message):
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            return None
