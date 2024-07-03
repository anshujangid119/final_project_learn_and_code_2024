def get_new_user_details():
    while True:
        # Loop to get a valid username
        while True:
            new_username = input("New username: ").strip()
            if not new_username:
                print("Username cannot be empty.")
            else:
                break  # Exit the loop if the username is valid

        # Loop to get a valid password
        while True:
            new_password = input("New password: ").strip()
            if not new_password:
                print("Password cannot be empty.")
            else:
                break  # Exit the loop if the password is valid

        # Loop to get a valid role
        while True:
            new_role = input("New role (admin/chef/employee): ").strip().lower()
            if new_role not in ['admin', 'chef', 'employee']:
                print("Invalid role. Please enter 'admin', 'chef', or 'employee'.")
            else:
                break  # Exit the loop if the role is valid

        return new_username, new_password, new_role


def get_new_dish_details():
    while True:
        # Loop to get a valid meal name
        while True:
            meal_name = input("Enter Dish name: ").strip()
            if not meal_name:
                print("Dish name cannot be empty.")
            else:
                break  # Exit the loop if the dish name is valid

        # Loop to get a valid meal type
        while True:
            meal_type = input("Enter Dish Type: 1. For Breakfast 2. For Lunch 3. For Dinner: ").strip()
            if meal_type not in ['1', '2', '3']:
                print("Invalid meal type. Please enter 1, 2, or 3.")
            else:
                break  # Exit the loop if the meal type is valid

        # Loop to get a valid availability
        while True:
            availability = input("Is available (yes/no): ").strip().lower()
            if availability not in ['yes', 'no']:
                print("Invalid availability. Please enter 'yes' or 'no'.")
            else:
                availability = 1 if availability == 'yes' else 0
                break  # Exit the loop if the availability is valid

        meal_type = 'breakfast' if meal_type == '1' else 'lunch' if meal_type == '2' else 'dinner'

        return meal_name, meal_type, availability


def get_meal_id():
    while True:
        try:
            meal_id = int(input("Enter meal id: "))
            return meal_id
        except ValueError:
            print("Invalid input. Please enter a valid meal ID.")


def get_availability_status():
    while True:
        try:
            availability = int(input("Enter availability status (0 for Not Available, 1 for Available): "))
            if availability in [0, 1]:
                return availability
            else:
                print("Invalid input. Please enter 0 or 1.")
        except ValueError:
            print("Invalid input. Please enter 0 or 1.")
