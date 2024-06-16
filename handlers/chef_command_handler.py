import json

class ChefCommandHandler:
    def __init__(self, client_socket, dish_db):
        self.client_socket = client_socket
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
                elif parsed_message['command'] == 'ADD_DISH':
                    self.handle_add_dish(parsed_message)
            except Exception as e:
                print(f"Error: {e}")
                break

    def handle_add_dish(self, message):
        new_dish = message['data']
        self.dish_db.add_dish(new_dish['name'], new_dish['ingredients'])
        self.client_socket.send(self.create_message('ADD_DISH_SUCCESS', 'Dish added successfully').encode())

    def create_message(self, command, data):
        return json.dumps({'command': command, 'data': data})

    def parse_message(self, message):
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            return None
