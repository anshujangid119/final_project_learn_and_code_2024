import mysql.connector


from databases import db_connection , db_cursor

class UserDatabase:

    def update_user_profile(self,data):
        query = 'update user_meal_preferences set spice_level = %s, region = %s, vegetarian_status = %s where user_id = %s'
        db_cursor.execute(query, (data['spice_level'],data['region'],data['vegetarian_status'],data['user_id']))
        db_connection.commit()
        return True

    def view_user_profile_data(self,user_id):
        query = 'select * from user_meal_preferences where user_id = %s'
        db_cursor.execute(query, (user_id,))
        result = db_cursor.fetchone()
        print(result)
        return result if result else None


    def get_user_details(self, username, password):
        query = "SELECT role,id FROM users WHERE username = %s AND password = %s"
        db_cursor.execute(query, (username, password))
        result = db_cursor.fetchone()
        # print(result)
        return result if result else None

    def add_user(self, username, password, role):
        if self.get_user_details(username, password):
            print("User already exists.")
            return False
        try:
            query = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
            db_cursor.execute(query, (username, password, role))
            db_connection.commit()
            user_id = db_cursor.lastrowid

            if role.lower() == 'employee':
                self.set_default_meal_preferences(user_id)

            print("User added successfully.")
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False

    def set_default_meal_preferences(self, user_id):
        try:
            query = '''
            INSERT INTO user_meal_preferences (user_id) 
            VALUES (%s)'''
            db_cursor.execute(query, (user_id,))
            db_connection.commit()
            print("Default meal preferences set for user.")
        except mysql.connector.Error as err:
            print(f"Error setting default meal preferences: {err}")

