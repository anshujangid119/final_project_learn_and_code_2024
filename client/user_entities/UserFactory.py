from user_entities.admin import Admin
from user_entities.chef import Chef
from user_entities.employee import Employee

class UserFactory:
    @staticmethod
    def create_user(role, username, password):
        if role == 'admin':
            return Admin(username, password)
        elif role == 'chef':
            return Chef(username, password)
        elif role == 'employee':
            return Employee(username, password)
