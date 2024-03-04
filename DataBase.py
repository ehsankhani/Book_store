import mysql.connector
from DataBase_Connection import get_database_connection

# Get the database connection
mydb, cursor = get_database_connection()

# CREATE DATABASE                                                               #CREATE DATABASE
# cursor.execute("CREATE DATABASE IF NOT EXISTS Book_Store")

# SHOW DATABASE                                                                  #SHOW DATABASE
# cursor.execute("SHOW DATABASES")
# for db in cursor:
#     print(db[0])

# CREATE TABLE                                                                  #CREATE TABLE  users
# SQL statements to create tables
# create_users_table = """
# CREATE TABLE IF NOT EXISTS users (
#     user_id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(50),
#     password VARCHAR(50),
#     first_name VARCHAR(25),
#     last_name VARCHAR(25),
#     city VARCHAR(50),
#     state VARCHAR(50),
#     zip_code VARCHAR(10)
# )
# """
# CREATE TABLE                                                                  #CREATE TABLE  credit_cards
# create_credit_cards_table = """
# CREATE TABLE IF NOT EXISTS credit_cards (
#     card_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     card_number VARCHAR(16),
#     exp_date DATE,
#     card_type VARCHAR(50),
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# )
# """
#
# CREATE TABLE books                                                             #CREATE TABLE books
# create_books_table = """
# CREATE TABLE IF NOT EXISTS books (
#     book_id INT AUTO_INCREMENT PRIMARY KEY,
#     author VARCHAR(100),
#     category VARCHAR(100),
#     title VARCHAR(255),
#     ISBN VARCHAR(20),
#     review FLOAT,
#     publisher VARCHAR(100),
#     minimum_property VARCHAR(100),
#     present_stock INT,
#     price DECIMAL(10, 2),
#     publish_year YEAR
# )
# """

#
# # Execute the SQL statements                                               #Execute tables
# cursor.execute(create_users_table)
# cursor.execute(create_credit_cards_table)
# cursor.execute(create_books_table)

##############################################        INSERT sample book
# # Sample book data
# author = "John Doe"
# category = "Fiction"
# title = "Sample Book"
# ISBN = "1234567890"
# review = 4.5
# publisher = "jk"
# minimum_property = "1"
# present_stock = 10
# price = 19.99
# publish_year = 2023
#
# # SQL statement to insert the sample book into the books table
# insert_book_query = """
# INSERT INTO books (author, category, title, ISBN, review, publisher, minimum_property, present_stock, price, publish_year)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# """
#
# # Tuple containing the values to be inserted
# book_data = (author, category, title, ISBN, review, publisher, minimum_property, present_stock, price, publish_year)
#
# # Execute the SQL query
# cursor.execute(insert_book_query, book_data)
#
# # Commit the transaction
# mydb.commit()
##################################################
