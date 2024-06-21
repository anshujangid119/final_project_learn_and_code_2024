import json

class EmployeeCommandHandler:
    def __init__(self, client_socket):
        self.client_socket = client_socket

    def handle_commands(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break

                parsed_message = self.parse_message(message)
                if parsed_message is None:
                    continue
                elif parsed_message['command'] == 'VOTE_FOR_NEXT_DAY':
                    self.handle_vote_foe_next_day(parsed_message)


                elif parsed_message['command'] == 'LOGOUT':
                    break
            except Exception as e:
                print(f"Error: {e}")
                break

    def handle_vote_for_next_day(self, message):
        meal_ids = message['data']
        if self.dish_db.vote_for_next_day(meal_ids):
            self.client_socket.send(self.create_message('VOTE_FOR_NEXT_DAY_SUCCESS', 'VOTE ADDED SUCCESSFULLY').encode())
    def create_message(self, command, data):
        return json.dumps({'command': command, 'data': data})

    def parse_message(self, message):
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            return None
