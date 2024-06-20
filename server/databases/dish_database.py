import mysql.connector

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