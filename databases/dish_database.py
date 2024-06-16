import mysql.connector

class DishDatabase:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="admin",
            password = "admin@1234",
            database="cafeteria"
        )
        self.cursor = self.connection.cursor()

    def add_dish(self, name, ingredients):
        query = "INSERT INTO dishes (name, ingredients) VALUES (%s, %s)"
        self.cursor.execute(query, (name, ingredients))
        self.connection.commit()
