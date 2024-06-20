# import database_connection
from databases.database_connection import DatabaseConnection

conn_obj = DatabaseConnection()
db_cursor = conn_obj.db_cursor()
db_connection = conn_obj.db_connection()