from user_entities.user import User
from user_entities.admin import Admin
from user_entities.chef import Chef
from user_entities.employee import Employee

if __name__ == "__main__":
    username = input("Username: ")
    password = input("Password: ")
    user = User(username, password)
    role = user.connect()

    if role == 'admin':
        admin = Admin(username, password)
        admin.client_socket = user.client_socket
        admin.perform_actions()

    elif role == 'chef':
        chef = Chef(username, password)
        chef.client_socket = user.client_socket
        chef.perform_actions()

    elif role == 'employee':
        employee = Employee(username, password)
        employee.client_socket = user.client_socket
        employee.perform_actions()

























