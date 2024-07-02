

class Recommendation:

    def get_top_meals(self,feedback_data,number_of_meals):
        breakfast_foods = []
        lunch_foods = []
        dinner_foods = []

        # Separate food items by meal type
        for item in feedback_data:
            item['composite_score'] = float(item.get('avg_composite_score', 0))
            if item['meal_type'] == 'breakfast':
                breakfast_foods.append(item)
            elif item['meal_type'] == 'lunch':
                lunch_foods.append(item)
            elif item['meal_type'] == 'dinner':
                dinner_foods.append(item)

        # Sort each list by composite score in descending order
        breakfast_foods_sorted = sorted(breakfast_foods, key=lambda x: x['composite_score'], reverse=True)
        lunch_foods_sorted = sorted(lunch_foods, key=lambda x: x['composite_score'], reverse=True)
        dinner_foods_sorted = sorted(dinner_foods, key=lambda x: x['composite_score'], reverse=True)

        # Get the top N food items for each meal type
        top_breakfast_foods = breakfast_foods_sorted
        top_lunch_foods = lunch_foods_sorted
        top_dinner_foods = dinner_foods_sorted

        return {
            'breakfast': top_breakfast_foods[:number_of_meals],
            'lunch': top_lunch_foods[:number_of_meals],
            'dinner': top_dinner_foods[:number_of_meals]
        }






