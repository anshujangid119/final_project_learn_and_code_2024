from databases import db_connection , db_cursor
from datetime import date

class Notification:

    def view_notification(self):
        current_date = date.today()
        query = "SELECT message FROM notification WHERE date = %s order by id"
        db_cursor.execute(query, (current_date,))
        result = db_cursor.fetchall()
        return result


    def update_notification(self,message):
        current_date = date.today()
        query = 'Insert INTO notification (message, date) values (%s, %s)'
        db_cursor.execute(query, (message,current_date))
        db_connection.commit()
        return True



