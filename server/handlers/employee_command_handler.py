import json

class EmployeeCommandHandler:
    def __init__(self, client_socket, dish_db,notification_db,user_db,):
        self.client_socket = client_socket
        self.dish_db = dish_db
        self.notification_db = notification_db
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
                elif parsed_message['command'] == 'VIEW_NOTIFICATION':
                    self.handle_view_notification(parsed_message)
                elif parsed_message['command'] == 'VIEW_USER_VOTES':
                    self.handle_view_user_vote(parsed_message)
                elif parsed_message['command'] == 'VIEW_MEAL':
                    self.handle_view_meal(parsed_message)
                elif parsed_message['command'] == 'VOTE_FOR_NEXT_DAY':
                    self.handle_vote_for_next_day(parsed_message)
                elif parsed_message['command'] == 'VIEW_FEEDBACK_DISHES':
                    self.handle_view_feedback_dishes(parsed_message)
                elif parsed_message['command'] == 'RECEIVE_FEEDBACK':
                    self.handle_receive_feedback(parsed_message)
                elif parsed_message['command'] == 'VIEW_DISCARD_MENU':
                    self.handle_view_discard_menu(parsed_message)
                elif parsed_message['command'] == 'DISCARD_ITEM_FEEDBACK':
                    self.handle_discard_item_feedback(parsed_message)
                elif parsed_message['command'] == 'VIEW_ROLLOUT_MEALS':
                    self.handle_view_rollout_meals(parsed_message)
                elif parsed_message['command'] == 'PROFILE_DATA':
                    self.handle_view_profile_data(parsed_message)
                elif parsed_message['command'] == 'UPDATE_PROFILE':
                    self.handle_update_profile(parsed_message)
                elif parsed_message['command'] == 'LOGOUT':
                    break
            except Exception as e:
                print(f"Error: {e}")
                break

    def handle_update_profile(self,message):
        data = message['data']
        if self.user_db.update_user_profile(data):
            self.client_socket.send(self.create_message('UPDATE_PROFILE_SUCCESS', 'UPDATE PROFILE SUCCESSFULLY').encode())

    def handle_view_profile_data(self, message):
        user_id = message['data']['user_id']
        user_data = self.user_db.view_user_profile_data(user_id)
        response = {
            'command': 'VIEW_USER_VOTES',
            'data': user_data
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())

    def handle_view_rollout_meals(self,message):
        data = message['data']
        menu = self.dish_db.view_sorted_rollout_menu(data['user_id'])
        is_voted = self.dish_db.user_already_voted(message)
        converted_data = [(user_id, (date.year, date.month, date.day)) for user_id, date in is_voted]
        response = {
            'command': 'VIEW_USER_VOTES',
            'data': (menu, converted_data)
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())

    def handle_discard_item_feedback(self,message):
        data = message['data']
        if self.dish_db.add_discard_item_feedback(data):
            self.client_socket.send(self.create_message('DISCARD_ITEM_FEEDBACK_SUCCESS', 'FEEDBACK ADDED SUCCESSFULLY').encode())

    def handle_view_discard_menu(self, message):
        menu = self.dish_db.view_discard_menu()
        response = {
            'command': 'VIEW_NOTIFICATION',
            'data': menu
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())

    def handle_view_notification(self,message):
        notifications = self.notification_db.view_notification()
        response = {
            'command': 'VIEW_NOTIFICATION',
            'data': notifications
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())

    def handle_view_meal(self,message):
        availability = 1
        meal_list = self.dish_db.available_meal(availability)
        response = {
            'command': 'VIEW_AVAILABLE_MEAL',
            'data': meal_list
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())
    def handle_receive_feedback(self, message):
        data = message['data']
        if self.dish_db.add_receive_feedback(data):
            self.client_socket.send(self.create_message('VOTE_FOR_NEXT_DAY_SUCCESS', 'VOTE ADDED SUCCESSFULLY').encode())

    def handle_view_feedback_dishes(self, message):
        meal_list = self.dish_db.view_feedback_dishes()
        response = {
            'command': 'VIEW_FEEDBACK_DISHES',
            'data': meal_list
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())


    def handle_view_user_vote(self,message):
        meal_list =  self.dish_db.view_user_vote()
        print("meal list")
        print(message)
        is_voted = self.dish_db.user_already_voted(message)
        converted_data = [(user_id, (date.year, date.month, date.day)) for user_id, date in is_voted]
        response = {
            'command': 'VIEW_USER_VOTES',
            'data': (meal_list,converted_data)
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())


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
