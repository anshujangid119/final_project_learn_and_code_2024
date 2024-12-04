from databases import db_connection, db_cursor
from datetime import date

class Notification:

    def view_notification(self,user_id):
        try:
            # current_date = date.today()

            query = '''
            SELECT n.id, n.message 
                FROM notification n
                WHERE NOT EXISTS (
                    SELECT 1 
                    FROM viewed_notification v 
                    WHERE v.notification_id = n.id 
                    AND v.user_id = %s
                )
                ORDER BY n.id;'''
            db_cursor.execute(query, (user_id,))
            result = db_cursor.fetchall()
            ids = []
            for row in result:
                ids.append(row[0])

            for id in ids:
                query = ''' Insert into viewed_notification (notification_id, user_id) values (%s,%s)'''
                db_cursor.execute(query, (id,user_id))
                db_connection.commit()

            return result

        except Exception as e:
            print(f"Error retrieving notifications: {e}")
            return []

    def update_notification(self, message):
        try:
            current_date = date.today()
            query = 'Insert INTO notification (message, date) values (%s, %s)'
            db_cursor.execute(query, (message, current_date))
            db_connection.commit()
            return True
        except Exception as e:
            print(f"Error updating notification: {e}")
            return False
