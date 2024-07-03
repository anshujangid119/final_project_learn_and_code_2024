def get_meal_number():
    while True:
        try:
            meal_number = int(input("For Rollout, enter how many meals you want to get recommended by the system: "))
            return meal_number
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def confirm_choice(prompt):
    while True:
        choice = input(prompt).strip().lower()
        if choice in ['yes', 'no']:
            return choice
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")

def get_meal_ids(prompt):
    while True:
        try:
            meal_ids = input(prompt).split(",")
            meal_ids = [int(meal_id.strip()) for meal_id in meal_ids]
            return meal_ids
        except ValueError:
            print("Invalid input. Please enter valid meal IDs separated by commas.")

def get_meal_list():
    return get_meal_ids("Enter meal ids separated by commas: ")

def get_feedback_meal_ids():
    return get_meal_ids("Enter Ids that you want to get feedback for, separated by commas: ")

def get_next_day_meal_ids(valid_ids):
    while True:
        try:
            prompt = ''
            meal_ids = input(prompt).split(",")
            meal_ids = [int(meal_id.strip()) for meal_id in meal_ids]
            if all(meal_id in valid_ids for meal_id in meal_ids):
                return meal_ids
            else:
                print("Invalid meal ID(s). Please enter IDs from the provided list.")
        except ValueError:
            print("Invalid input. Please enter valid meal IDs separated by commas.")
