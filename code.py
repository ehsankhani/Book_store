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

        # Create sign-in input fields
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.grid(row=1, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1)

        # Button to submit sign-in information
        self.sign_in_button = tk.Button(self.root, text="Sign In", command=self.validate_and_sign_in)
        self.sign_in_button.grid(row=3, columnspan=2)

        # Create back button
        self.create_back_button()

    def validate_and_sign_in(self):
        # Get user inputs
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        if not (username and password):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if the user exists and credentials are correct
        self.cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        if self.cursor.fetchone():
            messagebox.showinfo("Success", "Sign-in successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    # Add this method inside the class to create the back button
    def create_back_button(self):
        # Create back button to navigate to the last page
        self.back_button = tk.Button(self.root, text="Back", command=self.create_main_page)
        self.back_button.grid(row=4, column=1, sticky="se")

    def show_sign_up_page(self):
        # Clear the window and create sign-up page elements
        self.clear_window()
        self.sign_up_label = tk.Label(self.root, text="Sign Up Page")
        self.sign_up_label.grid(row=0, column=0)

        # Create sign-up input fields
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.grid(row=1, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1)

        self.first_name_label = tk.Label(self.root, text="First Name:")
        self.first_name_label.grid(row=3, column=0)
        self.first_name_entry = tk.Entry(self.root)
        self.first_name_entry.grid(row=3, column=1)

        self.last_name_label = tk.Label(self.root, text="Last Name:")
        self.last_name_label.grid(row=4, column=0)
        self.last_name_entry = tk.Entry(self.root)
        self.last_name_entry.grid(row=4, column=1)

        self.city_label = tk.Label(self.root, text="City:")
        self.city_label.grid(row=5, column=0)
        self.city_entry = tk.Entry(self.root)
        self.city_entry.grid(row=5, column=1)

        self.state_label = tk.Label(self.root, text="State:")
        self.state_label.grid(row=6, column=0)
        self.state_entry = tk.Entry(self.root)
        self.state_entry.grid(row=6, column=1)

        self.zip_code_label = tk.Label(self.root, text="Zip Code:")
        self.zip_code_label.grid(row=7, column=0)
        self.zip_code_entry = tk.Entry(self.root)
        self.zip_code_entry.grid(row=7, column=1)

        self.credit_card_number_label = tk.Label(self.root, text="Credit Card Number:")
        self.credit_card_number_label.grid(row=8, column=0)
        self.credit_card_number_entry = tk.Entry(self.root)
        self.credit_card_number_entry.grid(row=8, column=1)

        self.expiry_date_label = tk.Label(self.root, text="Expiry Date:")
        self.expiry_date_label.grid(row=9, column=0)
        self.expiry_date_entry = tk.Entry(self.root)
        self.expiry_date_entry.grid(row=9, column=1)

        self.card_type_label = tk.Label(self.root, text="Card Type:")
        self.card_type_label.grid(row=10, column=0)
        self.card_type_var = tk.StringVar()
        self.card_type_combobox = tk.OptionMenu(self.root, self.card_type_var, "Business Credit Card", "Travel Credit Card", "Secured Credit Card")
        self.card_type_combobox.grid(row=10, column=1)

        # Button to submit sign-up information
        self.sign_up_button = tk.Button(self.root, text="Sign Up", command=self.validate_and_sign_up)
        self.sign_up_button.grid(row=11, columnspan=2)

        # Create back button
        self.create_back_button()

    def validate_and_sign_up(self):
        # Get user inputs
        username = self.username_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zip_code = self.zip_code_entry.get()
        credit_card_number = self.credit_card_number_entry.get()
        expiry_date = self.expiry_date_entry.get()
        card_type = self.card_type_var.get()

        # Validate inputs
        if not (username and password and first_name and last_name and city and state and zip_code and credit_card_number and expiry_date):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if the user already exists
        self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        if self.cursor.fetchone():
            messagebox.showerror("Error", "Username already exists!")
            return

        # Store the user information in the database
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, first_name, last_name, city, state, zip_code) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (username, password, first_name, last_name, city, state, zip_code))
            self.mydb.commit()
            messagebox.showinfo("Success", "Sign-up successful!")

            # Get the user_id of the newly inserted user
            user_id = self.cursor.lastrowid

            # Store the credit card information in the database
            self.cursor.execute(
                "INSERT INTO credit_cards (user_id, card_number, exp_date, card_type) VALUES (%s, %s, %s, %s)",
                (user_id, credit_card_number, expiry_date, card_type))
            self.mydb.commit()
            messagebox.showinfo("Success", "Credit card information stored successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to sign up: {str(e)}")

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

    def create_back_button(self):
        # Create back button to navigate to the last page
        self.back_button = tk.Button(self.root, text="Back", command=self.create_main_page)
        self.back_button.grid(row=12, column=1, sticky="se")

if __name__ == "__main__":
    root = tk.Tk()
    app = BookstoreApp(root)
    root.mainloop()
