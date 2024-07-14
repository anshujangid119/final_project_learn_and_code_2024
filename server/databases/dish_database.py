import mysql.connector
from datetime import date
from databases import db_connection , db_cursor
from sentiment.analyzer import SentimentAnalyzer
class DishDatabase:

    def add_discard_item_feedback(self, data):
        try:
            query = '''
            INSERT INTO discard_feedback (discard_menu_id, like_text, dislike_text, recipe) 
            VALUES (%s, %s, %s, %s)
            '''
            db_cursor.execute(query, (data['discard_menu_id'], data['like_text'], data['dislike_text'], data['recipe']))
            db_connection.commit()
            print("Feedback added successfully.")
            return True
        except Exception as e:
            print(f"Error: {e}")

    def view_discard_menu(self):
        query = '''
        select * from discard_menu where is_discarded = true'''
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        return result

    def get_discard_feedback(self):
        query = '''
        SELECT 
            dm.id AS discard_menu_id,
            dm.food_id,
            m.name AS food_name,
            dm.is_discarded,
            df.like_text,
            df.dislike_text,
            df.recipe
        FROM 
            discard_menu dm
        JOIN 
            meal m ON dm.food_id = m.id
        LEFT JOIN 
            discard_feedback df ON dm.id = df.discard_menu_id'''
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        return result

    def update_discard(self, id):
        query = 'UPDATE discard_menu set is_discarded = true where food_id = %s'
        db_cursor.execute(query, (id,))
        db_connection.commit()
        return True

    def add_meal(self, name, meal_type, availability, price, spice_level, region, vegetarian_status):
        insert_meal_query = '''
        INSERT INTO meal (name, meal_type, availability, price) 
        VALUES (%s, %s, %s, %s)
        '''
        db_cursor.execute(insert_meal_query, (name, meal_type, availability, price))
        db_connection.commit()
        meal_id = db_cursor.lastrowid

        insert_properties_query = '''
        INSERT INTO meal_properties (meal_id, spice_level, region, vegetarian_status) 
        VALUES (%s, %s, %s, %s)
        '''
        db_cursor.execute(insert_properties_query, (meal_id, spice_level, region, vegetarian_status))
        db_connection.commit()
        print("Meal and its properties added successfully")
        return True

    def get_meal_name(self,id):
        query = "select name from meal where id = %s"
        db_cursor.execute(query,(id,))
        result = db_cursor.fetchall()
        return result

    def view_meal(self):
        query = '''
        SELECT m.id, m.name, m.meal_type, m.availability, m.price, mp.spice_level, mp.region, mp.vegetarian_status
        FROM meal m
        JOIN meal_properties mp 
        ON m.id = mp.meal_id;'''
        db_cursor.execute(query)
        result = db_cursor.fetchall()
        serialized_result = []
        for row in result:
            serialized_row = {
                "food_id": row[0],
                "food_name": row[1],
                "meal_type": row[2],
                "availability" : row[3],
                "price": float(row[4]),
                "spice_level": row[5],
                "region": row[6],
                "vegetarian_status": row[7]
                }
            serialized_result.append(serialized_row)

        return serialized_result
    def delete_meal(self,meal_id):
        print(meal_id)
        print(type(meal_id))
        query = 'Delete from meal where id = %s'
        db_cursor.execute(query, (meal_id,))
        db_connection.commit()
        print("Successfully")
        return True
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

    def add_feedback_request(self, meals_ids):
        list_id = meals_ids['meal_ids']
        current_date = date.today()
        for meal_id in list_id:
            query = "INSERT INTO feedback_requests (food_id, date) VALUES (%s, %s)"
            db_cursor.execute(query, (meal_id, current_date))
            db_connection.commit()
        return True

    def view_sorted_rollout_menu(self,user_id):
        current_date = date.today()

        query = '''
        SELECT m.id AS food_id, m.name, f.vote
        FROM dailymenu f
        JOIN meal m ON f.food_id = m.id
        JOIN meal_properties mp ON m.id = mp.meal_id
        JOIN user_meal_preferences ump ON ump.user_id = %s
        WHERE f.date = %s
        ORDER BY
            CASE WHEN mp.spice_level = ump.spice_level THEN 1 ELSE 0 END DESC,
            CASE WHEN mp.region = ump.region THEN 2 ELSE 0 END DESC,
            CASE WHEN mp.vegetarian_status = ump.vegetarian_status THEN 3 ELSE 0 END DESC;
        '''

        # Execute the query with current date and user ID
        db_cursor.execute(query, (user_id, current_date))
        result = db_cursor.fetchall()

        return result


    def view_user_vote(self):
        current_date = date.today()
        query = "select f.food_id , m.name , f.vote from dailymenu f join meal m on f.food_id = m.id where f.date = %s"
        db_cursor.execute(query,(current_date,))
        result = db_cursor.fetchall()
        return result

    def add_next_day_meal(self, meal_ids):
        list_id = meal_ids['meal_ids']
        for meal_id in list_id:
            query = "update dailymenu set isselected = 1 where food_id = %s"
            db_cursor.execute(query, (meal_id, ))
            db_connection.commit()
            return True

    def vote_for_next_day(self,data,):
        list_id = data['meal_ids']
        user_id = data['user_id']

        current_date = date.today()
        for meal_id in list_id:
            query = """
            UPDATE dailymenu
            SET vote = vote + 1
            WHERE food_id = %s AND date = %s
            """
            db_cursor.execute(query, (meal_id,current_date))
            db_connection.commit()
        query = "insert into vote_update(user_id, date_of_vote) values(%s, %s) "
        db_cursor.execute(query, (user_id, current_date))
        db_connection.commit()
        return True

    def view_feedback_dishes(self):
        query = "select  f.food_id , m.name from feedback_requests f join meal m on f.food_id = m.id where f.date = %s"
        current_date = date.today()
        db_cursor.execute(query,(current_date,))
        result = db_cursor.fetchall()
        return result

    def add_receive_feedback(self, data):
        sentiment = SentimentAnalyzer()
        user_id = data['user_id']
        current_date = date.today()
        comment = data['comment']
        score = sentiment.sentiment_score(comment)
        meal_id = data['meal_id']
        quantity = data['quantity']
        quality = data['quality']
        rating = data['rating']
        value_for_money = data['value_for_money']
        query = 'INSERT INTO FEEDBACK (date,user_id,food_id, rating,quality, quantity,value_for_money,comment,sentiment_score) values (%s, %s, %s, %s,%s, %s,%s, %s,%s)'
        db_cursor.execute(query, (current_date, user_id, meal_id,rating,quality,quantity,value_for_money,comment,score))
        db_connection.commit()
        return True
    def user_already_voted(self,message):
        user_id = message['data']['user_id']
        print("inside user already voted")
        current_date = date.today()
        query = "Select * from vote_update where user_id = %s and date_of_vote = %s"
        db_cursor.execute(query, (user_id,current_date))
        result = db_cursor.fetchall()
        print(result)
        return result















