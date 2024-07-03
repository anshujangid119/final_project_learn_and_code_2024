import json
from recommendation_engine.recommendation import Recommendation
class ChefCommandHandler:
    def __init__(self, client_socket, dish_db, recomm_db, notification_db):
        self.client_socket = client_socket
        self.dish_db = dish_db
        self.recomm_db = recomm_db
        self.notification_db = notification_db

    def handle_commands(self):
        while True:
            try:
                message = self.client_socket.recv(8096).decode()
                if not message:
                    break

                parsed_message = self.parse_message(message)
                if parsed_message is None:
                    continue
                
                if parsed_message['command'] == 'LOGOUT':
                    break
                elif parsed_message['command'] == 'VIEW_MEAL':
                    self.handle_view_meal(parsed_message)
                elif parsed_message['command'] == 'VIEW_AVAILABLE_MEAL':
                    self.handle_view_meal_type(parsed_message)
                elif parsed_message['command'] == 'ROLL_OUT':
                    self.handle_roll_out_menu(parsed_message)
                elif parsed_message['command'] == 'RECIEVE_FEEDBACK':
                    self.handle_feedback_request(parsed_message)
                elif parsed_message['command'] == 'VIEW_USER_VOTES':
                    self.handle_view_user_vote(parsed_message)
                elif parsed_message['command'] == 'NEXT_DAY_MEAL':
                    self.handle_next_day_meal(parsed_message)
                elif parsed_message['command'] == 'RECOMMEND_MEAL':
                    self.handle_recommend_meal(parsed_message)
            except Exception as e:
                print(f"Error: {e}")
                break


    def handle_recommend_meal(self,message):
        number_of_meals = message['data']['meal_number']
        meal_list = self.recomm_db.get_recommendation_dataset()
        recomm_obj = Recommendation()
        data = recomm_obj.get_top_meals(meal_list,number_of_meals)

        print(meal_list)
        response = {
            'command': 'get_recommendation_dataset',
            'data': data
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())



    def handle_next_day_meal(self, message):
        meal_ids = message['data']
        if self.dish_db.add_next_day_meal(meal_ids):
            message = '[ROLLOUT SELECTION] For tomorrow the meals are selected'
            self.notification_db.update_notification(message)
            self.client_socket.send(self.create_message('NEXT_DAY_MEAL_SUCCESS', 'NEXT DAY MEAL UPDATED SUCCESSFULLY').encode())


    def handle_view_user_vote(self, message):
        meal_list =  self.dish_db.view_user_vote()
        response = {
            'command': 'VIEW_USER_VOTES',
            'data': meal_list
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())

    def handle_feedback_request(self, message):
        meal_ids = message['data']
        if self.dish_db.add_feedback_request(meal_ids):
            self.client_socket.send(self.create_message('RECIEVE_FEEDBACK_SUCCESSFUlly', 'receive feedback request').encode())


    def handle_roll_out_menu(self, message):
        meal_ids = message['data']
        if self.dish_db.add_roll_out_menu(meal_ids):
            message = '[ROLLOUT]' + 'Chef rollout menu for tomorrow please go and vote'
            self.notification_db.update_notification(message)
            self.client_socket.send(self.create_message('ROLL_OUT_SUCCESSFUlly', 'menu roll out successfully').encode())

    def handle_view_meal_type(self, message):
        meal_type = message['data']
        availability = meal_type['availability']
        meal_list = self.dish_db.available_meal(availability)
        response = {
            'command': 'VIEW_AVAILABLE_MEAL',
            'data': meal_list
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())


    def handle_view_meal(self, message):
        print("inside handle_view_meal")
        meal_list = self.dish_db.view_meal()
        response = {
            'command': 'VIEW_MEAL',
            'data': meal_list
        }
        json_response = json.dumps(response)
        self.client_socket.send(json_response.encode())


    def create_message(self, command, data):
        return json.dumps({'command': command, 'data': data})

    def parse_message(self, message):
        try:
            return json.loads(message)
        except json.JSONDecodeError:
            return None
