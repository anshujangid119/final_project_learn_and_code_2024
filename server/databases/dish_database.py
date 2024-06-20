import mysql.connector

class DishDatabase:
    def add_dish(self, name, ingredients):
        query = "INSERT INTO dishes (name, ingredients) VALUES (%s, %s)"
        self.cursor.execute(query, (name, ingredients))
        self.connection.commit()
