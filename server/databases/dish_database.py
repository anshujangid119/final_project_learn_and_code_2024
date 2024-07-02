import mysql.connector
from datetime import date
from databases import db_connection , db_cursor
from sentiment.analyzer import SentimentAnalyzer
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















