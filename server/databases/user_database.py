import mysql.connector
import base64
import json
# from databases.secret import secrets
from databases import db_connection , db_cursor
#
# # user_entities = base64.b64decode(secrets['user_entities']).decode("utf-8")
# # password = base64.b64decode(secrets['password']).decode("utf-8")
# decoded_json_str = base64.b64decode(secrets).decode('utf-8')
# secret = json.loads(decoded_json_str)
class UserDatabase:

    def get_user_role(self, username, password):
        query = "SELECT role FROM users WHERE username = %s AND password = %s"
        db_cursor.execute(query, (username, password))
        result = db_cursor.fetchone()
        return result[0] if result else None

    def add_user(self, username, password, role):
        if self.get_user_role(username, password):
            return False
        query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        db_cursor.execute(query, (username, password, role))
        db_connection.commit()
        return True
