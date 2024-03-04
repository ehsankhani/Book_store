# database_connection.py
import mysql.connector

def get_database_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="ehsan",
        database="Book_Store"
    )
    cursor = mydb.cursor()
    return mydb, cursor
