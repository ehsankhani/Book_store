import mysql.connector
from DataBase_Connection import get_database_connection

class RecommendationSystem:
    def __init__(self):
        # Get the database connection
        self.mydb, self.cursor = get_database_connection()

    def get_recommendations(self, user_id, count):
        # Get the list of books purchased by the user
        self.cursor.execute("SELECT book_id FROM purchases WHERE user_id = %s", (user_id,))
        user_purchases = self.cursor.fetchall()

        # Extract features of the purchased books
        features = []
        for purchase in user_purchases:
            book_id = purchase[0]
            self.cursor.execute("SELECT author, category, publisher FROM books WHERE book_id = %s", (book_id,))
            book_features = self.cursor.fetchone()
            features.append(book_features)

        # Calculate similarity between purchased books and all other books
        recommendations = []
        for feature in features:
            author, category, publisher = feature
            # Example: Calculate similarity based on category only
            self.cursor.execute("SELECT book_id, category FROM books WHERE category = %s AND book_id NOT IN %s",
                                 (category, tuple(user_purchases)))
            similar_books = self.cursor.fetchall()
            recommendations.extend(similar_books)

        # Filter out duplicate recommendations
        recommendations = list(set(recommendations))

        # Select the top N recommendations
        top_recommendations = recommendations[:count]

        return top_recommendations


    def get_random_books(self, count):
        self.cursor.execute("SELECT * FROM books WHERE catalog_flag = 1 ORDER BY RAND() LIMIT %s", (count,))
        random_books = self.cursor.fetchall()
        return random_books
