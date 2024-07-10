from user_entities.user import User
import sys
sys.path.append("..")
from user_entities.admin import Admin
from user_entities.chef import Chef
from user_entities.employee import Employee

print("------------------------ welcome to Cafteria management-------------------------------------------")

retries_count = 2
def main(role = None, user_id = None):
    global retries_count
    username = input("Enter your Username: ")
    password = input("Enter your Password: ")
    user_obj = User(username, password)

    user = user_obj.connect()
    if user is not None:
        role = user[0]
        user_id = user[1]
# factory design pattern
        if role == 'admin':
            admin = Admin(username, password)
            admin.client_socket = user_obj.client_socket
            admin.perform_actions(user_id)
            main()

        elif role == 'chef':
            chef = Chef(username, password)
            chef.client_socket = user_obj.client_socket
            chef.perform_actions(user_id)
            main()
    #
        elif role == 'employee':
            employee = Employee(username, password)
            employee.client_socket = user_obj.client_socket
            employee.perform_actions(user_id)
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





















