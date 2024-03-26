from DataBase_Connection import get_database_connection
from datetime import datetime

# Get the database connection
mydb, cursor = get_database_connection()

# # CREATE DATABASE                                                               #CREATE DATABASE
# cursor.execute("CREATE DATABASE IF NOT EXISTS Book_Store")
#
# # SHOW DATABASE                                                                  #SHOW DATABASE
# cursor.execute("SHOW DATABASES")
# for db in cursor:
#     print(db[0])

# # CREATE TABLE                                                                  #CREATE TABLE  users
# # SQL statements to create tables
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
#     user_id INT AUTO_INCREMENT PRIMARY KEY,
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

##########################################################################      INSERT sample book
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
######################################################################################
# SQL statement to add the column                                                    # SQL statement to add the column
# alter_query = """
# ALTER TABLE books
# ADD COLUMN catalog_flag INT DEFAULT 1;
# """
#
# # Execute the SQL statement
# cursor.execute(alter_query)
# CREATE TABLE PURCHASE                                                 # CREATE TABLE PURCHASE
# create_table_query = """
# CREATE TABLE IF NOT EXISTS purchases (
#     purchase_id INT AUTO_INCREMENT PRIMARY KEY,
#     user_id INT,
#     ISBN VARCHAR(20),
#     book_name VARCHAR(50),
#     purchase_date DATETIME,
#     credit_card_type VARCHAR(50),
#     credit_card_number VARCHAR(20),
#     purchase_status VARCHAR(20),
#     admin_fullName VARCHAR(50),
#     admin_id INT,
#     FOREIGN KEY (user_id) REFERENCES users(user_id)
# );
# """
#
# # Execute the SQL statement
# cursor.execute(create_table_query)
# CREATE TABLE ADMIN                                                    # CREATE TABLE ADMIN
# create_table_query = """
# CREATE TABLE IF NOT EXISTS admin (
#     admin_id INT AUTO_INCREMENT PRIMARY KEY,
#     username VARCHAR(50) UNIQUE,
#     password VARCHAR(50),
#     msg_box TEXT,
#     purchase_actions TEXT,
#     worked_purchase_ids TEXT,
#     orders TEXT,
#     book_operations TEXT,
#     catalog_changes TEXT
# );
# """
# cursor.execute(create_table_query)
# SQL statement to add the date_in_out column
# alter_query = """
# ALTER TABLE manager
# ADD COLUMN password VARCHAR(20);
# """
#
# # Execute the SQL statement
# cursor.execute(alter_query)

# SQL statement to insert a new admin
# insert_query = """
# #     INSERT INTO admin (username, password, national_id, msg_box, purchase_actions,
# #                        worked_purchase_ids, orders, book_operations, catalog_changes,
# #                        date_in, date_out)
# #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
# # """
#
# # Define the values for the new admin
# new_admin_values = ('ehsanAdmin', '123123', '031240', None, None, None, None, None, None, datetime.now(), None)
#
# # Execute the INSERT query with the values
# cursor.execute(insert_query, new_admin_values)
#
# # Commit the transaction
# mydb.commit()

###########################################################################################################33
# SQL statement to create the manager table
# CREATE TABLE manager                                                            # CREATE TABLE manager
# create_table_query = """
# CREATE TABLE IF NOT EXISTS manager (
#     manager_id INT AUTO_INCREMENT PRIMARY KEY,
#     msg_box TEXT,
#     full_name VARCHAR(50),
#     national_id VARCHAR(10),
#     date_in DATETIME,
#     date_out DATETIME,
#     allowed_purchases TEXT,
#     orders_to_add TEXT,
#     book_oprations TEXT
# );
# """
#
# # Execute the SQL statement
# cursor.execute(create_table_query)
#SQL statement to insert a new row into the manager table
######################################################################################
# Define the values for the new manager                                          # Define the values for the new manager
# new_manager_values = {
#     "msg_box": None,
#     "full_name": "ehsan m",
#     "national_id": "0312402376",
#     "date_in": datetime.now(),
#     "date_out": None,
#     "allowed_purchases": None,
#     "orders_to_add": None,
#     "book_oprations": None
# }
# insert_query = """
#     INSERT INTO manager (msg_box, full_name, national_id, date_in, date_out, allowed_purchases, orders_to_add, book_oprations)
#     VALUES (%(msg_box)s, %(full_name)s, %(national_id)s, %(date_in)s, %(date_out)s, %(allowed_purchases)s, %(orders_to_add)s, %(book_oprations)s)
# """
#
# # Execute the INSERT query with the values
# cursor.execute(insert_query, new_manager_values)
#
# # Commit the transaction
# mydb.commit()

# -- Add a new column 'password' to the 'manager' table
#############################################################################
# #add column is_active
# # SQL command to add the column
# add_column_query = "UPDATE admin SET is_active = 1 WHERE admin_id = 1"
#
# # Executing the SQL command to add the column
# cursor.execute(add_column_query)
#
# # Committing the changes
# mydb.commit()
## CREATE TABLE MANAGER RECORDS MAN                                            # CREATE TABLE MANAGER RECORDS
# SQL query to create the manager_records table
# create_table_query = """
#             CREATE TABLE manager_records (
#                 record_id INT AUTO_INCREMENT PRIMARY KEY,
#                 manager_id INT,
#                 allowed_purchases BOOLEAN,
#                 orders_to_add TEXT,
#                 book_operations TEXT,
#                 timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                 description TEXT,
#                 FOREIGN KEY (manager_id) REFERENCES manager(manager_id)
#             )
#         """
#
# # Execute the SQL query to create the table
# cursor.execute(create_table_query)
#
# # Commit the transaction
# mydb.commit()
#
# # SQL command to drop the column
# drop_column_query = "ALTER TABLE manager DROP COLUMN book_oprations"
#
# # Executing the SQL command to drop the column
# cursor.execute(drop_column_query)
#
# # Committing the changes
# mydb.commit()
