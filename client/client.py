from user_entities.user import User
import sys
import getpass
sys.path.append("..")
from user_entities.admin import Admin
from user_entities.chef import Chef
from user_entities.employee import Employee

print("------------------------ welcome to Cafteria management-------------------------------------------")

retries_count = 2
def main():
    global retries_count
    username = input("Enter your Username: ")
    password = input("Enter your Password: ")
    user = User(username, password)
    role = user.connect()

    if role == 'admin':
        admin = Admin(username, password)
        admin.client_socket = user.client_socket
        admin.perform_actions()
        main()

    elif role == 'chef':
        chef = Chef(username, password)
        chef.client_socket = user.client_socket
        chef.perform_actions()
        main()
    #
    elif role == 'employee':
        employee = Employee(username, password)
        employee.client_socket = user.client_socket
        employee.perform_actions()
        main()
    else:
        if retries_count > 0:
            print(f"Please try again you have {retries_count} more attempt to login")
            retries_count -= 1
            main()
        else:
            print("You have reached the number of attempts please try again")




if __name__ == "__main__":
    main()





















