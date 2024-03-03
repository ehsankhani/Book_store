import mysql.connector
import code

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="ehsan",
    database="Book_Store"
)
print(mydb)
cursor = mydb.cursor()

# CREATE DATABASE                                                               #CREATE DATABASE
# cursor.execute("CREATE DATABASE Book_Store")

# SHOW DATABASE                                                                  #SHOW DATABASE
# cursor.execute("SHOW DATABASES")
# for db in cursor:
#     print(db[0])

# CREATE TABLE                                                                  #CREATE TABLE  users
# SQL statements to create tables
# create_users_table = """
# CREATE TABLE users (
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
# CREATE TABLE credit_cards (
#     card_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     card_number VARCHAR(16),
#     exp_date DATE,
#     card_type VARCHAR(50),
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# )
# """
#
#CREATE TABLE books                                                             #CREATE TABLE books
# create_books_table = """
# CREATE TABLE books (
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
# Check if the column exists before adding it
check_column_query = """
SELECT COUNT(*)
FROM information_schema.columns
WHERE table_name = 'books' AND column_name = 'book_image'
"""

cursor.execute(check_column_query)
column_exists = cursor.fetchone()[0]

if not column_exists:
    # ALTER TABLE to add a column for storing image data
    alter_table_query = """
    ALTER TABLE books
    ADD COLUMN book_image BLOB
    """

    # Execute the ALTER TABLE query
    cursor.execute(alter_table_query)

    # Commit the transaction
    mydb.commit()

    print("Column 'book_image' added successfully.")
else:
    print("Column 'book_image' already exists in the table.")

# Sample book data
author = "John Doe"
category = "Fiction"
title = "Sample Book"
ISBN = "1234567890"
review = 4.5
publisher = "jk"
minimum_property = "1"
present_stock = 10
price = 19.99
publish_year = 2023

# Sample book image (replace 'path_to_image' with the actual path to your image file)
image_path = "images/sample_image.jpg"
with open(image_path, 'rb') as file:
    book_image = file.read()

# SQL statement to insert the sample book into the books table with the image
insert_book_query = """
INSERT INTO books (author, category, title, ISBN, review, publisher, minimum_property, present_stock, price, publish_year, book_image) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Tuple containing the values to be inserted
book_data = (author, category, title, ISBN, review, publisher, minimum_property, present_stock, price, publish_year, book_image)

# Execute the SQL query
cursor.execute(insert_book_query, book_data)

# Commit the transaction
mydb.commit()
