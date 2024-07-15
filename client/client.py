from user_entities.user import User
import sys
sys.path.append("..")
# from user_entities.admin import Admin
# from user_entities.chef import Chef
# from user_entities.employee import Employee
from user_entities.UserFactory import UserFactory

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

        user_instance = UserFactory.create_user(role, username, password)
        if user_instance:
            user_instance.client_socket = user_obj.client_socket
            user_instance.perform_actions(user_id)
            main()
        else:
            print("Invalid role. Please try again.")
            main()
    else:
        if retries_count > 0:
            print(f"Please try again. You have {retries_count} more attempts to login.")
            retries_count -= 1
            main()
        else:
            print("You have reached the number of attempts. Please try again later.")

if __name__ == "__main__":
    main()
