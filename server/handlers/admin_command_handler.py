import json

class AdminCommandHandler:
    def __init__(self, client_socket, user_db):
        self.client_socket = client_socket
        self.user_db = user_db

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
            except Exception as e:
                print(f"Error: {e}")
                break

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
