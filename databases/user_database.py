import mysql.connector
import base64
from databases.secret import secrets

user = base64.b64decode(secrets['user']).decode("utf-8")
password = base64.b64decode(secrets['password']).decode("utf-8")
class UserDatabase:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user=user,
            password = password,
            database="cafeteria"
        )
        self.cursor = self.connection.cursor()

    def get_user_role(self, username, password):
        query = "SELECT role FROM users WHERE username = %s AND password = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def add_user(self, username, password, role):
        if self.get_user_role(username, password):
            return False
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (username, password, role))
        self.connection.commit()
        return True
