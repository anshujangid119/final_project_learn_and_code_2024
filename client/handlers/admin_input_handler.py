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
        while True:
            meal_name = input("Enter Dish name: ").strip()
            if not meal_name:
                print("Dish name cannot be empty.")
            else:
                break

        while True:
            meal_type = input("Enter Dish Type: 1. For Breakfast 2. For Lunch 3. For Dinner: ").strip()
            if meal_type not in ['1', '2', '3']:
                print("Invalid meal type. Please enter 1, 2, or 3.")
            else:
                meal_type = 'breakfast' if meal_type == '1' else 'lunch' if meal_type == '2' else 'dinner'
                break

        while True:
            availability = input("Is available (yes/no): ").strip().lower()
            if availability not in ['yes', 'no']:
                print("Invalid availability. Please enter 'yes' or 'no'.")
            else:
                availability = 1 if availability == 'yes' else 0
                break

        while True:
            try:
                price = float(input("Enter Price (20 to 200): ").strip())
                if price < 20 or price > 200:
                    print("Price must be between 20 and 200.")
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a numeric value for the price.")

        while True:
            spice_level = input("Enter Spice Level (mild/medium/spicy): ").strip().lower()
            if spice_level not in ['mild', 'medium', 'spicy']:
                print("Invalid spice level. Please enter 'mild', 'medium', or 'spicy'.")
            else:
                break

        while True:
            region = input("Enter Region (South/North/Other): ").strip().capitalize()
            if region not in ['South', 'North', 'Other']:
                print("Invalid region. Please enter 'South', 'North', or 'Other'.")
            else:
                break

        while True:
            vegetarian_status = input("Is the dish Vegetarian, Non-Vegetarian, or Eggetarian?: ").strip().capitalize()
            if vegetarian_status not in ['Vegetarian', 'Non-Vegetarian', 'Eggetarian']:
                print("Invalid vegetarian status. Please enter 'Vegetarian', 'Non-Vegetarian', or 'Eggetarian'.")
            else:
                break

        return meal_name, meal_type, availability, price, spice_level, region, vegetarian_status


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
