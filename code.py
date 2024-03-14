import tkinter as tk
from tkinter import messagebox
from DataBase_Connection import get_database_connection

class BookstoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookstore")
        self.is_logged_in = False
        self.logged_in_username = None

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

        # Create login status label
        self.login_status_label = tk.Label(self.root, text="", fg="red")
        self.login_status_label.grid(row=3, columnspan=3)

        # Update login status
        self.update_login_status()

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

    def go_back(self):
        # Check if the user is logged in
        if self.is_logged_in:
            self.create_main_page()  # Go back to the main page
        else:
            self.show_sign_in_page()  # Go back to the sign-in page

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
        user = self.cursor.fetchone()
        if user:
            messagebox.showinfo("Success", "Sign-in successful!")
            self.is_logged_in = True
            self.logged_in_username = user[3]  # Assuming the name is in the fourth column
        else:
            messagebox.showerror("Error", "Invalid username or password.")
            self.is_logged_in = False

        # Update login status
        self.update_login_status()

        # Go back to the previous page
        self.go_back()

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
        self.create_main_page()
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

    def update_login_status(self):
        # Clear any existing welcome and logout buttons
        if hasattr(self, 'welcome_label'):
            self.welcome_label.destroy()
        if hasattr(self, 'logout_button'):
            self.logout_button.destroy()
        if hasattr(self, 'msg_box_button'):
            self.msg_box_button.destroy()

        # Update welcome message and display logout button if logged in
        if self.is_logged_in:
            self.welcome_label = tk.Label(self.root, text=f"Welcome, {self.logged_in_username}", fg="green")
            self.welcome_label.grid(row=3, columnspan=2)

            self.logout_button = tk.Button(self.root, text="Logout", command=self.logout)
            self.logout_button.grid(row=3, column=2)

            # Show view and edit info buttons
            self.view_info_button = tk.Button(self.root, text="View Info", command=self.view_user_info)
            self.view_info_button.grid(row=4, column=1)
            self.edit_info_button = tk.Button(self.root, text="Edit Info", command=self.edit_user_info)
            self.edit_info_button.grid(row=4, column=2)

            # Show Message Box button
            self.msg_box_button = tk.Button(self.root, text="Message Box", command=self.show_message_box)
            self.msg_box_button.grid(row=4, column=0)
        else:
            self.welcome_label = tk.Label(self.root, text="not logged in", fg="red")
            self.welcome_label.grid(row=3, columnspan=3)

    def show_message_box(self):
        # Remember the current page
        self.previous_page = self.root.winfo_children()

        # Clear the window
        self.clear_window()

        # Get message box content from the database
        self.cursor.execute("SELECT msg_box FROM admin WHERE username = %s", (self.logged_in_username,))
        message_box_content = self.cursor.fetchone()

        # Display message box content in a dialog box
        if message_box_content:
            messagebox.showinfo("Message Box", message_box_content[0])
        else:
            messagebox.showinfo("Message Box", "No messages in the message box.")

        self.create_main_page()

    def view_user_info(self):
        # Retrieve user information from the database
        self.cursor.execute("SELECT * FROM users WHERE username = %s", (self.logged_in_username,))
        user_info = self.cursor.fetchone()

        # Display user information in a dialog box
        if user_info:
            user_info_text = f"Username: {user_info[1]}\nFirst Name: {user_info[3]}\nLast Name: {user_info[4]}\nCity: {user_info[5]}\nState: {user_info[6]}\nZip Code: {user_info[7]}"
            messagebox.showinfo("User Info", user_info_text)
        else:
            messagebox.showerror("Error", "Failed to retrieve user information.")

    def edit_user_info(self):
        # Clear the window
        self.clear_window()

        # Create the edit page
        self.edit_selected_parameter_page()


    def edit_selected_parameter_page(self):
        # List of parameters
        parameters = ["Password", "First Name", "Last Name", "City", "State", "Zip Code"]

        # Prompt user to select a parameter to edit
        selected_parameter = tk.StringVar(value=parameters[0])  # Default selection
        parameter_label = tk.Label(self.root, text="Select parameter to edit:")
        parameter_label.grid(row=0, column=0)
        parameter_dropdown = tk.OptionMenu(self.root, selected_parameter, *parameters)
        parameter_dropdown.grid(row=0, column=1)

        # Button to confirm parameter selection
        confirm_button = tk.Button(self.root, text="Confirm",
                                   command=lambda: self.edit_selected_parameter(selected_parameter.get()))
        confirm_button.grid(row=1, columnspan=2)

        # Create back button
        self.create_back_button()
    def edit_selected_parameter(self, parameter):
        # Clear the window
        self.clear_window()

        # Create labels and entry fields for editing the selected parameter
        parameter_label = tk.Label(self.root, text=f"Edit {parameter}:")
        parameter_label.grid(row=0, column=0)
        new_value_entry = tk.Entry(self.root)
        new_value_entry.grid(row=0, column=1)

        # Button to confirm the new value
        confirm_button = tk.Button(self.root, text="Confirm",
                                   command=lambda: self.update_parameter(parameter, new_value_entry.get()))
        confirm_button.grid(row=1, columnspan=2)
        self.create_back_button()


    def update_parameter(self, parameter, new_value):
        try:
            # Update the parameter in the database
            if parameter.lower() in ["password", "first name", "last name", "city", "state", "zip code"]:
                # Update user information
                self.cursor.execute(f"UPDATE users SET {parameter.lower().replace(' ', '_')} = %s WHERE username = %s",
                                    (new_value, self.logged_in_username))
            elif parameter.lower() in ["credit card number", "expiry date", "card type"]:
                # Update credit card information
                self.cursor.execute(
                    f"UPDATE credit_cards SET {parameter.lower().replace(' ', '_')} = %s WHERE user_id = (SELECT user_id FROM users WHERE username = %s)",
                    (new_value, self.logged_in_username))

            # Commit the changes to the database
            self.mydb.commit()

            # Clear the screen
            self.clear_window()

            # Show a messagebox indicating successful update
            messagebox.showinfo("Update Info", f"{parameter.capitalize()} updated successfully.")

            # After updating the parameter, you may want to refresh the user interface to reflect the changes
            # For example, you can call a method to update the user's information displayed on the screen
            self.update_login_status()  # Update login status to reflect changes
        except Exception as e:
            # Show error messagebox if update fails
            messagebox.showerror("Update Error", f"Failed to update {parameter}: {str(e)}")
        self.create_main_page()

    def logout(self):
        # Clear logged-in user information
        self.is_logged_in = False
        self.logged_in_username = None

        # Update login status
        self.update_login_status()

        # Clear the window and go back to the main page
        self.create_main_page()


if __name__ == "__main__":
    root = tk.Tk()
    app = BookstoreApp(root)
    root.mainloop()