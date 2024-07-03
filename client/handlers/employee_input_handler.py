def get_validated_input(prompt, valid_range):
    while True:
        try:
            value = int(input(prompt))
            if value in valid_range:
                return value
            else:
                print(f"Invalid input. Please enter a value between {valid_range.start} and {valid_range.stop - 1}.")
        except ValueError:
            print("Invalid input. Please enter a numerical value.")

def collect_feedback(response_data):
    print(f"{'ID':<15} {'Name':<15}")
    lis_of_id = []
    for i in response_data:
        lis_of_id.append(i[0])
        print(f"{i[0]:<15} {i[1]:<15}")
    number_of_attempt = 3
    while number_of_attempt>0:
        try:
            meal_id = int(input("Enter food ID for which you want to give feedback: "))
            if meal_id in lis_of_id:
                rating = get_validated_input("Enter overall rating (1-5): ", range(1, 6))
                quantity = get_validated_input("Rate your satisfaction on quantity (1-5): ", range(1, 6))
                quality = get_validated_input("Rate your satisfaction on quality (1-5): ", range(1, 6))
                value_for_money = get_validated_input("Is your money worth this meal (1-5): ", range(1, 6))
                comment = input("Provide a comment so that we can improve ourselves: ")

                return {
                    'meal_id': meal_id,
                    'rating': rating,
                    'quantity': quantity,
                    'quality': quality,
                    'value_for_money': value_for_money,
                    'comment': comment
                }

            else:
                number_of_attempt -=1
                print("Invalid food ID. Please enter a valid ID from the list you have only",number_of_attempt ,"left")
        except ValueError:
            print("Invalid input. Please enter a numerical value for food ID.")



def collect_votes(votes_list):
    while True:
        meal_ids = input("Enter IDs that you want to vote for tomorrow, separated by commas: ").split(',')
        meal_ids = [int(meal_id.strip()) for meal_id in meal_ids]
        print("inside", meal_ids)

        invalid_ids = [meal_id for meal_id in meal_ids if meal_id not in votes_list]

        if invalid_ids:
            print(
                f"Invalid IDs: Please enter valid meal IDs from the list: ")
        else:
            return meal_ids