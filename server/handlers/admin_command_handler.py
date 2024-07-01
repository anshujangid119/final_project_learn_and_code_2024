import json
import time
from exception_handlers.custom_exception import DatabaseError, InvalidCommandError

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

                command = parsed_message.get('command')
                if command == 'LOGOUT':
                    break
                elif command == 'ADD_USER':
                    self.handle_add_user(parsed_message)
                elif command == 'ADD_DISH':
                    self.handle_add_meal(parsed_message)
                elif command == 'VIEW_MEAL':
                    print("inside view")
                    self.handle_view_meal(parsed_message)
                elif command == 'UPDATE_MEAL':
                    self.handle_update_meal(parsed_message)
                elif command == 'DELETE_MEAL':
                    self.handle_delete_meal(parsed_message)
                else:
                    raise InvalidCommandError(f"Received unknown command: {command}")
            except InvalidCommandError as ice:
                print(f"Invalid command error: {ice}")
                self.client_socket.send(self.create_message('ERROR', str(ice)).encode())
            except DatabaseError as de:
                print(f"Database error: {de}")
                self.client_socket.send(self.create_message('ERROR', str(de)).encode())
            except Exception as e:
                print(f"Error: {e}")
                self.client_socket.send(self.create_message('ERROR', str(e)).encode())

    def handle_delete_meal(self, message):
        data = message['data']
        try:
            if self.dish_db.delete_meal(data['meal_id']):
                self.client_socket.send(self.create_message('DELETED_SUCCESSFULLY', 'Meal deleted successfully').encode())
        except Exception as e:
            raise DatabaseError(f"Failed to delete meal: {e}")

    def handle_update_meal(self, message):
        print("inside server handler")
        meal = message['data']
        print(meal)
        try:
            if self.dish_db.update_meal(meal['meal_id'], meal['availability']):
                self.client_socket.send(self.create_message('UPDATE_MEAL_SUCCESS', 'Meal updated successfully').encode())
        except Exception as e:
            raise DatabaseError(f"Failed to update meal: {e}")

    def handle_view_meal(self, message):
        try:
            meal_list = self.dish_db.view_meal()
            response = {
                'command': 'VIEW_MEAL',
                'data': meal_list
            }
            json_response = json.dumps(response)
            self.client_socket.send(json_response.encode())
        except Exception as e:
            raise DatabaseError(f"Failed to view meals: {e}")

    def handle_add_meal(self, message):
        new_meal = message['data']
        try:
            if self.dish_db.add_meal(new_meal['meal_name'], new_meal['meal_type'], new_meal['availability']):
                self.client_socket.send(self.create_message('ADD_MEAL_SUCCESS', 'Meal added successfully').encode())
        except Exception as e:
            raise DatabaseError(f"Failed to add meal: {e}")

    def handle_add_user(self, message):
        new_user = message['data']
        try:
            if self.user_db.add_user(new_user['username'], new_user['password'], new_user['role']):
                self.client_socket.send(self.create_message('ADD_USER_SUCCESS', 'User added successfully').encode())
            else:
                self.client_socket.send(self.create_message('ADD_USER_FAILURE', 'User already exists').encode())
        except Exception as e:
            raise DatabaseError(f"Failed to add user: {e}")

    def create_message(self, command, data):
        return json.dumps({'command': command, 'data': data})

    def parse_message(self, message):
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            return None
