import mysql.connector
from datetime import date
from databases import db_connection , db_cursor
class DishDatabase:
    def add_meal(self, name, type, availability):
        query = "INSERT INTO meal (name, meal_type, availability) VALUES (%s, %s , %s)"
        db_cursor.execute(query, (name, type, availability))
        db_connection.commit()
        # print("added successfully")
        return True

    def view_meal(self):
        query = "SELECT * FROM meal"
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        return result

    def update_meal(self, meal_id, availability):
        print(type(meal_id))
        print(type(availability))
        query = "update meal set availability = %s where id = %s"
        # print(f"Executing query: {query} with values ({availability}, {meal_id})")
        db_cursor.execute(query, (availability , meal_id))
        db_connection.commit()
        return True

    def available_meal(self, availability):
        query = "select * from meal where availability = %s"
        db_cursor.execute(query, (availability,))
        result = db_cursor.fetchall()
        return result

    def add_roll_out_menu(self, meal_ids):
        list_id = meal_ids['meal_list']
        vote = 0
        current_date = date.today()
        print(current_date)
        print(meal_ids)
        for meal_id in list_id:
            print(meal_id)
            query = """
            INSERT INTO dailymenu (food_id, vote, date)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE vote = VALUES(vote);
            """
            db_cursor.execute(query, (meal_id, vote, current_date))
            db_connection.commit()
        return True






