import mysql.connector
from databases.secret_manager import secrets
class DatabaseConnection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user=secrets['user'],
            password = secrets['password'],
            database="cafeteria"
        )
        self.cursor = self.connection.cursor()

    def db_cursor(self):
        return self.cursor

    def db_connection(self):
        return self.connection

