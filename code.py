import DataBase
import tkinter as tk
import mysql.connector
from tkinter import messagebox




class BookstoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookstore")

        # Connect to the database
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="ehsan",
            database="Book_Store"
        )
        self.cursor = self.mydb.cursor()

        # Create GUI elements
        self.search_label = tk.Label(root, text="Search:")
        self.search_label.grid(row=0, column=0)
        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=0, column=1)
        self.search_button = tk.Button(root, text="Search", command=self.search_books)
        self.search_button.grid(row=0, column=2)

        self.create_account_button = tk.Button(root, text="Create Account", command=self.create_account)
        self.create_account_button.grid(row=1, column=0)

        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=1, column=1)

    def search_books(self):
        # Get the search query from the entry field
        search_query = self.search_entry.get()

        # Clear any previous search results
        # Implement this based on how you display search results in your GUI

        # Execute SQL query to search for books
        search_sql = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s"
        search_params = (f"%{search_query}%", f"%{search_query}%")
        self.cursor.execute(search_sql, search_params)
        search_results = self.cursor.fetchall()

        # Display search results in the GUI
        if search_results:
            for book in search_results:
                # Implement how you want to display search results in your GUI
                # For example, you could create labels or insert into a listbox
                print(book)  # Placeholder, replace with GUI code
        else:
            messagebox.showinfo("Search", "No books found matching the search query.")

    def create_account(self):
        # Implement account creation functionality here
        pass

    def login(self):
        # Implement login functionality here
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = BookstoreApp(root)
    root.mainloop()
