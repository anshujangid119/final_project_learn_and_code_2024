from databases import db_connection , db_cursor

class RecommendationDatabase():

    def get_recommendation_dataset(self):
        print("inside class function ")

        query = '''
            WITH aggregated_data AS (
                SELECT
                    m.id AS food_id,
                    m.name AS food_name,
                    m.meal_type,
                    f.rating,
                    (f.rating + f.quality + f.quantity + f.value_for_money + f.sentiment_score) AS composite_score,
                    f.comment
                FROM feedback f
                JOIN meal m ON f.food_id = m.id
            )
            SELECT
                food_id,
                food_name,
                meal_type,
                avg(rating),
                AVG(composite_score) AS avg_composite_score,
                GROUP_CONCAT(comment SEPARATOR ', ') AS concatenated_comments
            FROM aggregated_data
            GROUP BY food_id;
        '''

        db_cursor.execute(query)
        result = db_cursor.fetchall()
        serialized_result = []
        for row in result:
            serialized_row = {
                "food_id": row[0],
                "food_name": row[1],
                "meal_type": row[2],
                "avg_rating" : float(row[3]),
                "avg_composite_score": float(row[4]),
                "total_rating": row[5]
                }
            serialized_result.append(serialized_row)

        return serialized_result