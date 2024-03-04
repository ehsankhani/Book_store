import tkinter as tk
from tkinter import messagebox
from DataBase_Connection import get_database_connection

class BookstoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookstore")

        # Get the database connection
        self.mydb, self.cursor = get_database_connection()

        # Create GUI elements
        self.create_main_page()

    def create_main_page(self):
        # Clear the window and create main page elements
        self.clear_window()
        self.search_label = tk.Label(self.root, text="Search:")
        self.search_label.grid(row=0, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=0, column=1)
        self.search_button = tk.Button(self.root, text="Search", command=self.search_books)
        self.search_button.grid(row=0, column=2)

        # Create a Listbox to display search results
        self.search_results_listbox = tk.Listbox(self.root)
        self.search_results_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Buttons for sign-in and sign-up
        self.sign_in_button = tk.Button(self.root, text="Sign In", command=self.show_sign_in_page)
        self.sign_in_button.grid(row=2, column=0)
        self.sign_up_button = tk.Button(self.root, text="Sign Up", command=self.show_sign_up_page)
        self.sign_up_button.grid(row=2, column=1)

    def show_sign_in_page(self):
        # Clear the window and create sign-in page elements
        self.clear_window()
        self.sign_in_label = tk.Label(self.root, text="Sign In Page")
        self.sign_in_label.grid(row=0, column=0)
        # Create sign-in input fields and button
        # Example: username_entry = tk.Entry(self.root)
        #          password_entry = tk.Entry(self.root, show="*")
        #          sign_in_button = tk.Button(self.root, text="Sign In", command=self.sign_in)

    def show_sign_up_page(self):
        # Clear the window and create sign-up page elements
        self.clear_window()
        self.sign_up_label = tk.Label(self.root, text="Sign Up Page")
        self.sign_up_label.grid(row=0, column=0)
        # Create sign-up input fields and button
        # Example: username_entry = tk.Entry(self.root)
        #          password_entry = tk.Entry(self.root, show="*")
        #          sign_up_button = tk.Button(self.root, text="Sign Up", command=self.sign_up)

    def clear_window(self):
        # Clear all widgets from the window
        for widget in self.root.winfo_children():
            widget.destroy()

    def search_books(self):
        # Clear any previous search results
        self.search_results_listbox.delete(0, tk.END)

        # Get the search query from the entry field
        search_query = self.search_entry.get()

        # Execute SQL query to search for books
        search_sql = "SELECT * FROM books WHERE title LIKE %s OR author LIKE %s"
        search_params = (f"%{search_query}%", f"%{search_query}%")
        self.cursor.execute(search_sql, search_params)
        search_results = self.cursor.fetchall()

        # Display search results in the GUI
        if search_results:
            for book in search_results:
                # Format the book information
                book_info = f"Title: {book[3]}, Author: {book[1]}"
                # Insert book information into the Listbox
                self.search_results_listbox.insert(tk.END, book_info)
        else:
            messagebox.showinfo("Search", "No books found matching the search query.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookstoreApp(root)
    root.mainloop()
