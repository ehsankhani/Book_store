import tkinter as tk
from tkinter import messagebox,scrolledtext
from DataBase_Connection import get_database_connection
import mysql.connector
import datetime
from decimal import Decimal
# import traceback

class BookstoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookstore")
        self.is_logged_in = False
        self.logged_in_username = None
        self.is_admin = False  # Flag to indicate admin login status
        self.manager_id = None

        # Get the database connection
        self.mydb, self.cursor = get_database_connection()

        # Create GUI elements
        self.create_main_page()

    def create_main_page(self):
        # Clear the window and create main page elements
        self.clear_window()

        # GUI elements for main page
        tk.Label(self.root, text="Search:").grid(row=0, column=0)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.grid(row=0, column=1)
        tk.Button(self.root, text="Search", command=self.search_books).grid(row=0, column=2)
        self.search_results_listbox = tk.Listbox(self.root)
        self.search_results_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Buttons for sign-in and sign-up
        tk.Button(self.root, text="Sign In", command=self.show_sign_in_page).grid(row=2, column=0)
        tk.Button(self.root, text="Sign Up", command=self.show_sign_up_page).grid(row=2, column=1)

        # Buttons for admin and manager login
        tk.Button(self.root, text="Admin Login", command=self.show_admin_login_page).grid(row=3, column=2, sticky="w")
        tk.Button(self.root, text="Manager Login", command=self.show_manager_login_page).grid(row=2, column=2,
                                                                                              sticky="e")

        self.login_status_label = tk.Label(self.root, text="", fg="red")
        self.login_status_label.grid(row=3, columnspan=3)

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

    def show_admin_login_page(self):
        # Clear the window and create admin login page elements
        self.clear_window()
        self.admin_login_label = tk.Label(self.root, text="Admin Login")
        self.admin_login_label.grid(row=0, column=0)

        # Create login input fields
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.grid(row=1, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1)

        # Button to submit admin login information
        self.admin_login_button = tk.Button(self.root, text="Login", command=self.validate_and_sign_in_admin)
        self.admin_login_button.grid(row=3, columnspan=2)

        # Create back button
        self.create_back_button()

    def show_manager_login_page(self):
        # Clear the window and create manager login page elements
        self.clear_window()
        self.manager_login_label = tk.Label(self.root, text="Manager Login")
        self.manager_login_label.grid(row=0, column=0)

        # Create login input fields
        self.username_label = tk.Label(self.root, text="Username:")
        self.username_label.grid(row=1, column=0)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self.root, text="Password:")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1)

        # Button to submit manager login information
        self.manager_login_button = tk.Button(self.root, text="Login", command=self.validate_and_sign_in_manager)
        self.manager_login_button.grid(row=3, columnspan=2)

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

    def validate_and_sign_in_admin(self):
        # Get user inputs
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        if not (username and password):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if the user exists and credentials are correct
        # Perform authentication for admin here, using a separate table for admins
        # Replace 'admin_table' with the actual table name for admins
        self.cursor.execute("SELECT admin_id FROM admin WHERE username = %s AND password = %s", (username, password))
        admin_id = self.cursor.fetchone()
        if admin_id:
            # Sign-in successful
            messagebox.showinfo("Success", "Admin sign-in successful!")
            self.admin_id = admin_id[0]  # Save the admin_id for further use
            self.open_admin_page()
        else:
            # Invalid credentials
            messagebox.showerror("Error", "Invalid username or password.")

    def validate_and_sign_in_manager(self):
        # Get user inputs
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Validate inputs
        if not (username and password):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Check if the user exists and credentials are correct
        # Perform authentication for manager here, using a separate table for managers
        # Replace 'manager_table' with the actual table name for managers
        self.cursor.execute("SELECT * FROM manager WHERE full_name = %s AND password = %s", (username, password))
        manager = self.cursor.fetchone()
        if manager:
            # Sign-in successful
            messagebox.showinfo("Success", "Manager sign-in successful!")
            self.open_manager_page()
        else:
            # Invalid credentials
            messagebox.showerror("Error", "Invalid username or password.")

    def open_admin_page(self):
        # Clear the window and create the admin page
        self.clear_window()
        welcome_label = tk.Label(self.root, text="Welcome Admin", fg="green")
        welcome_label.grid(row=0, column=0, columnspan=2)

        # Create a button to manage the bookstore
        manage_bookstore_button = tk.Button(self.root, text="Manage Bookstore",
                                            command=self.open_bookstore_management_page)
        manage_bookstore_button.grid(row=1, column=0, padx=10, pady=5)

        # Create a button for listing the books
        list_books_button = tk.Button(self.root, text="List of the Books", command=self.show_book_list)
        list_books_button.grid(row=1, column=1, padx=10, pady=5)

        # Create a button for placing orders
        place_orders_button = tk.Button(self.root, text="Place Orders", command=self.open_place_orders_window)
        place_orders_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Create a button for accessing the inbox
        inbox_button = tk.Button(self.root, text="Inbox", command=self.open_admin_inbox)
        inbox_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        # Create a back button
        back_button = tk.Button(self.root, text="Back", command=self.go_back)
        back_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def open_place_orders_window(self):
        # Create a new window for placing orders
        place_orders_window = tk.Toplevel(self.root)
        place_orders_window.title("Place Orders")

        # Retrieve the list of books from the database
        self.cursor.execute("SELECT book_id, title, present_stock, minimum_property FROM books")
        books_data = self.cursor.fetchall()

        # Create labels to display book details
        tk.Label(place_orders_window, text="Select a Book:").grid(row=0, column=0, padx=10, pady=5)
        book_listbox = tk.Listbox(place_orders_window, width=50, height=10)
        book_listbox.grid(row=1, column=0, padx=10, pady=5)

        # Populate the listbox with book titles
        for book in books_data:
            book_listbox.insert(tk.END, f"{book[1]} (ID: {book[0]})")

        def show_book_details():
            # Get the selected book index
            selected_index = book_listbox.curselection()
            if selected_index:
                index = int(selected_index[0])
                selected_book = books_data[index]

                # Display book details
                tk.Label(place_orders_window, text=f"Quantity: {selected_book[2]}").grid(row=2, column=0, padx=10,
                                                                                         pady=5)
                tk.Label(place_orders_window, text=f"Minimum Property: {selected_book[3]}").grid(row=3, column=0,
                                                                                                 padx=10, pady=5)

                # Entry field for the new quantity to order
                new_quantity_entry = tk.Entry(place_orders_window)
                new_quantity_entry.grid(row=4, column=0, padx=10, pady=5)

                # Create the confirm button and pass it to the place_order function
                confirm_button = tk.Button(place_orders_window, text="Place Order",
                                           command=lambda: self.place_order(new_quantity_entry, selected_book,
                                                                            confirm_button))
                confirm_button.grid(row=5, column=0, padx=10, pady=5)

        # Button to show book details
        show_details_button = tk.Button(place_orders_window, text="Show Details", command=show_book_details)
        show_details_button.grid(row=1, column=1, padx=10, pady=5)

    def place_order(self, new_quantity_entry, selected_book, confirm_button):
        # Disable the "Place Order" button to prevent multiple clicks
        confirm_button.config(state="disabled")

        # Get the new quantity to order
        new_quantity = new_quantity_entry.get()

        # Check for the present manager with date_out = NULL
        present_manager_query = "SELECT manager_id FROM manager WHERE date_out IS NULL"
        self.cursor.execute(present_manager_query)
        present_manager = self.cursor.fetchone()

        if present_manager:
            # Implement logic to send order to the present manager with new quantity
            message = f"New order for book ID {selected_book[0]}: Quantity - {new_quantity}"

            # Retrieve the existing messages in the manager's inbox
            self.cursor.execute("SELECT msg_box FROM manager WHERE manager_id = %s", (present_manager[0],))
            existing_messages = self.cursor.fetchone()[0]

            if existing_messages:
                # Append the new message to the existing messages with a comma separator
                message = existing_messages + ", " + message

            # Update the message box with the combined messages
            update_query = "UPDATE manager SET msg_box = %s WHERE manager_id = %s AND date_out IS NULL"
            self.cursor.execute(update_query, (message, present_manager[0]))
            self.mydb.commit()  # Commit the transaction
            self.refresh_database_connection()

            # Inform the admin that the order has been placed successfully
            messagebox.showinfo("Success", "Order sent to manager successfully. Waiting for response...")
        else:
            messagebox.showerror("Error", "No active manager found.")

        # Re-enable the "Place Order" button for subsequent orders
        confirm_button.config(state="normal")

    def open_bookstore_management_page(self):
        # Clear the window and create the page for managing the bookstore
        self.clear_window()
        tk.Label(self.root, text="Manage Bookstore", fg="blue").grid(row=0, column=0, columnspan=2)

        # Create buttons for managing the bookstore
        insert_button = tk.Button(self.root, text="Insert Book", command=self.insert_book_ui)
        insert_button.grid(row=1, column=0, padx=10, pady=5)

        modify_button = tk.Button(self.root, text="Modify Book", command=self.modify_book)
        modify_button.grid(row=1, column=1, padx=10, pady=5)

        delete_button = tk.Button(self.root, text="Delete Book", command=self.delete_book)
        delete_button.grid(row=2, column=0, padx=10, pady=5)

        back_button = tk.Button(self.root, text="Back", command=self.open_admin_page)
        back_button.grid(row=2, column=1, padx=10, pady=5)

    def open_admin_inbox(self):
        # Clear the window
        self.clear_window()

        # Retrieve messages from the admin's inbox
        self.cursor.execute("SELECT msg_box FROM admin WHERE admin_id = %s", (self.admin_id,))
        messages = self.cursor.fetchone()  # Retrieve only one row

        # Create a new window for displaying inbox messages
        inbox_window = tk.Toplevel(self.root)
        inbox_window.title("Admin Inbox")

        # Create a listbox to display message subjects
        message_listbox = tk.Listbox(inbox_window, width=50, height=10)
        message_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        if messages:
            # Split messages by comma to separate them
            msg_parts = messages[0].split(',')
            for msg in msg_parts:
                # Extract subject (order for book ID)
                subject = msg.split(":")[0].strip()
                message_listbox.insert(tk.END, subject)

            # Function to display full message on selection
            def show_full_message(event):
                # Get the index of the selected item
                index = message_listbox.curselection()[0]

                # Create a new window to display the full message
                full_message_window = tk.Toplevel(inbox_window)
                full_message_window.title("Full Message")

                # Retrieve and display the full message
                full_message = msg_parts[index].strip()
                full_message_text = tk.Text(full_message_window, height=10, width=50)
                full_message_text.insert(tk.END, full_message)
                full_message_text.pack(fill="both", expand=True, padx=10, pady=10)
                full_message_text.configure(state="disabled")

                # Function to delete the message
                def delete_message():
                    # Delete the selected message from the database
                    updated_messages = [msg for i, msg in enumerate(msg_parts) if i != index]
                    updated_msg_string = ','.join(updated_messages)
                    update_query = "UPDATE admin SET msg_box = %s WHERE admin_id = %s"
                    self.cursor.execute(update_query, (updated_msg_string, self.admin_id))
                    self.mydb.commit()  # Commit the transaction
                    full_message_window.destroy()  # Close the full message window
                    messagebox.showinfo("Delete", "Message deleted successfully")

                # Create a button to delete the message
                delete_button = tk.Button(full_message_window, text="Delete", command=delete_message)
                delete_button.pack(pady=10)

            # Bind the show_full_message function to listbox selection
            message_listbox.bind("<<ListboxSelect>>", show_full_message)
        else:
            # If there are no messages, display a message indicating so
            tk.Label(inbox_window, text="No messages in the inbox", fg="red").pack(pady=10)

        # Create a back button to return to the admin page
        back_button = tk.Button(inbox_window, text="Back", command=self.open_admin_page)
        back_button.pack(pady=10)

    def show_book_list(self):
        # Clear the current window
        self.clear_window()

        # Retrieve the list of books from the database
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()

        # Create a listbox to display the book titles
        book_listbox = tk.Listbox(self.root)
        book_listbox.pack(padx=10, pady=10)

        # Insert each book title into the listbox
        for book in books:
            book_listbox.insert(tk.END, f"{book[3]} by {book[1]}")

        # Double-click event handler for showing book details
        def show_book_details(event):
            # Get the index of the selected book in the listbox
            selected_index = book_listbox.curselection()
            if selected_index:
                index = int(selected_index[0])
                selected_book = books[index]

                # Display book details in a messagebox
                messagebox.showinfo("Book Details",
                                    f"Title: {selected_book[3]}\nAuthor: {selected_book[1]}\nCategory: {selected_book[2]}\nISBN: {selected_book[4]}\nReview: {selected_book[5]}\nPublisher: {selected_book[6]}\nMinimum Property: {selected_book[7]}\nPresent Property: {selected_book[8]}\nPrice: {selected_book[9]}\nPublish Year: {selected_book[10]}")

        # Bind the double - click event to the listbox
        book_listbox.bind("<Double-Button-1>", show_book_details)

        # Create a back button to return to the main admin page
        back_button = tk.Button(self.root, text="Back", command=self.open_admin_page)
        back_button.pack(pady=5)

    def insert_book_ui(self):
        # Clear the window
        self.clear_window()

        # Create labels and entry fields for book details
        tk.Label(self.root, text="Author:").grid(row=0, column=0)
        author_entry = tk.Entry(self.root)
        author_entry.grid(row=0, column=1)

        tk.Label(self.root, text="Category:").grid(row=1, column=0)
        category_var = tk.StringVar()
        categories = ["Fiction", "poetry", "Children", "classic", "romance", "History",
                      "Psychology", "Travel/Adventure", "Biography/Autobiography"]
        category_combobox = tk.OptionMenu(self.root, category_var, *categories)
        category_combobox.grid(row=1, column=1)

        tk.Label(self.root, text="Title:").grid(row=2, column=0)
        title_entry = tk.Entry(self.root)
        title_entry.grid(row=2, column=1)

        tk.Label(self.root, text="ISBN:").grid(row=3, column=0)
        isbn_entry = tk.Entry(self.root)
        isbn_entry.grid(row=3, column=1)

        tk.Label(self.root, text="Review:").grid(row=4, column=0)
        review_entry = tk.Entry(self.root)
        review_entry.grid(row=4, column=1)

        tk.Label(self.root, text="Publisher:").grid(row=5, column=0)
        publisher_entry = tk.Entry(self.root)
        publisher_entry.grid(row=5, column=1)

        tk.Label(self.root, text="Min. Property:").grid(row=6, column=0)
        min_property_entry = tk.Entry(self.root)
        min_property_entry.grid(row=6, column=1)

        tk.Label(self.root, text="Present Property:").grid(row=7, column=0)
        present_property_entry = tk.Entry(self.root)
        present_property_entry.grid(row=7, column=1)

        tk.Label(self.root, text="Price:").grid(row=8, column=0)
        price_entry = tk.Entry(self.root)
        price_entry.grid(row=8, column=1)

        tk.Label(self.root, text="Publish Year:").grid(row=9, column=0)
        publish_year_entry = tk.Entry(self.root)
        publish_year_entry.grid(row=9, column=1)

        # Button to submit book details
        submit_button = tk.Button(self.root, text="Submit", command=lambda: self.insert_book(
            author_entry.get(), category_var.get(), title_entry.get(), isbn_entry.get(), review_entry.get(),
            publisher_entry.get(), min_property_entry.get(), present_property_entry.get(), price_entry.get(),
            publish_year_entry.get()
        ))
        submit_button.grid(row=10, columnspan=2)

        # Create back button
        self.create_back_button()

    def record_admin_action(self, action_type, book_id=None, description=None):
        if book_id is None:
            query = "INSERT INTO admin_records (admin_id, action_type, description) VALUES (%s, %s, %s)"
            values = (self.admin_id, action_type, description)
        else:
            query = "INSERT INTO admin_records (admin_id, action_type, book_id, description) VALUES (%s, %s, %s, %s)"
            values = (self.admin_id, action_type, book_id, description)

        self.cursor.execute(query, values)
        self.mydb.commit()

    def insert_book(self, author, category, title, isbn, review, publisher, min_property, present_property, price,
                    publish_year):
        try:
            # Insert the book details into the database
            self.cursor.execute(
                "INSERT INTO books (author, category, title, ISBN, review, publisher, minimum_property, present_stock, price, publish_year, catalog_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (author, category, title, isbn, review, publisher, min_property, present_property, price, publish_year,
                 1))
            self.mydb.commit()
            # Show success message
            messagebox.showinfo("Success", "Book inserted successfully!")

            # Get the new book_id
            book_id = self.cursor.lastrowid

            # Record admin action
            self.record_admin_action(action_type='insert', book_id=book_id,
                                     description="Inserted book: {}".format(title))
        except Exception as e:
            # Show error message if insertion fails
            messagebox.showerror("Error", f"Failed to insert book: {str(e)}")

        # Navigate back to the management page
        self.open_admin_page()

    def modify_book(self):
        # Clear the window
        self.clear_window()

        # Retrieve the list of books from the database
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()

        # Create a listbox to display the book titles
        book_listbox = tk.Listbox(self.root)
        book_listbox.pack(padx=10, pady=10)

        # Insert each book title into the listbox
        for book in books:
            book_listbox.insert(tk.END, f"{book[3]} by {book[1]}")

        # Function to show book details and edit
        def show_book_to_edit(event):
            # Get the index of the selected book in the listbox
            selected_index = book_listbox.curselection()
            if selected_index:
                index = int(selected_index[0])
                selected_book = books[index]

                # Function to update book information
                def update_book_info():
                    # Retrieve the new values entered by the admin
                    new_author = author_entry.get()
                    new_category = category_entry.get()
                    new_title = title_entry.get()
                    new_review = review_entry.get()
                    new_publisher = publisher_entry.get()
                    new_min_property = min_property_entry.get()
                    new_present_stock = present_stock_entry.get()
                    new_price = price_entry.get()
                    new_publish_year = publish_year_entry.get()

                    # Query to retrieve the book_id based on other fields (adjust as per your database schema)
                    self.cursor.execute("""
                                SELECT book_id, title, author, category, publisher, minimum_property, present_stock, price, publish_year
                                FROM books 
                                WHERE title=%s AND author=%s AND category=%s AND publisher=%s
                            """, (new_title, new_author, new_category, new_publisher))
                    result = self.cursor.fetchone()
                    if result:
                        book_id, old_title, old_author, old_category, old_publisher, old_min_property, old_present_stock, old_price, old_publish_year = result
                    else:
                        messagebox.showerror("Error", "Book not found in the database.")
                        return

                    # Update the book information in the database
                    self.cursor.execute("""
                                UPDATE books 
                                SET author=%s, category=%s, title=%s, review=%s, publisher=%s, 
                                    minimum_property=%s, present_stock=%s, price=%s, publish_year=%s
                                WHERE book_id=%s
                            """, (new_author, new_category, new_title, new_review, new_publisher,
                                  new_min_property, new_present_stock, new_price, new_publish_year, book_id))
                    self.mydb.commit()
                    messagebox.showinfo("Success", "Book information updated successfully.")

                    # Prepare the description for recording admin action
                    description = "The '{}' book: ".format(old_title)
                    changes = []
                    if new_title != old_title:
                        changes.append("title changed from '{}' to '{}'".format(old_title, new_title))
                    if new_author != old_author:
                        changes.append("author changed from '{}' to '{}'".format(old_author, new_author))
                    if new_category != old_category:
                        changes.append("category changed from '{}' to '{}'".format(old_category, new_category))
                    if new_publisher != old_publisher:
                        changes.append("publisher changed from '{}' to '{}'".format(old_publisher, new_publisher))
                    if new_min_property != old_min_property:
                        changes.append(
                            "minimum property changed from '{}' to '{}'".format(old_min_property, new_min_property))
                    if new_present_stock != old_present_stock:
                        changes.append(
                            "present stock changed from '{}' to '{}'".format(old_present_stock, new_present_stock))
                    if new_price != old_price:
                        changes.append("price changed from '{}' to '{}'".format(old_price, new_price))
                    if new_publish_year != old_publish_year:
                        changes.append(
                            "publish year changed from '{}' to '{}'".format(old_publish_year, new_publish_year))

                    description += ", ".join(changes)
                    self.record_admin_action(action_type='modify', book_id=book_id, description=description)

                    # Clear the entry fields
                    author_entry.delete(0, tk.END)
                    category_entry.delete(0, tk.END)
                    title_entry.delete(0, tk.END)
                    review_entry.delete(0, tk.END)
                    publisher_entry.delete(0, tk.END)
                    min_property_entry.delete(0, tk.END)
                    present_stock_entry.delete(0, tk.END)
                    price_entry.delete(0, tk.END)
                    publish_year_entry.delete(0, tk.END)

                # Display book details and entry fields to edit
                edit_window = tk.Toplevel(self.root)
                edit_window.title("Edit Book Details")

                tk.Label(edit_window, text="Author:").grid(row=0, column=0, sticky="e")
                tk.Label(edit_window, text="Category:").grid(row=1, column=0, sticky="e")
                tk.Label(edit_window, text="Title:").grid(row=2, column=0, sticky="e")
                tk.Label(edit_window, text="Review:").grid(row=3, column=0, sticky="e")
                tk.Label(edit_window, text="Publisher:").grid(row=4, column=0, sticky="e")
                tk.Label(edit_window, text="Minimum Property:").grid(row=5, column=0, sticky="e")
                tk.Label(edit_window, text="Present Stock:").grid(row=6, column=0, sticky="e")
                tk.Label(edit_window, text="Price:").grid(row=7, column=0, sticky="e")
                tk.Label(edit_window, text="Publish Year:").grid(row=8, column=0, sticky="e")

                author_entry = tk.Entry(edit_window)
                author_entry.grid(row=0, column=1)
                author_entry.insert(tk.END, selected_book[1])

                category_entry = tk.Entry(edit_window)
                category_entry.grid(row=1, column=1)
                category_entry.insert(tk.END, selected_book[2])

                title_entry = tk.Entry(edit_window)
                title_entry.grid(row=2, column=1)
                title_entry.insert(tk.END, selected_book[3])

                review_entry = tk.Entry(edit_window)
                review_entry.grid(row=3, column=1)
                review_entry.insert(tk.END, selected_book[5])

                publisher_entry = tk.Entry(edit_window)
                publisher_entry.grid(row=4, column=1)
                publisher_entry.insert(tk.END, selected_book[6])

                min_property_entry = tk.Entry(edit_window)
                min_property_entry.grid(row=5, column=1)
                min_property_entry.insert(tk.END, selected_book[7])

                present_stock_entry = tk.Entry(edit_window)
                present_stock_entry.grid(row=6, column=1)
                present_stock_entry.insert(tk.END, selected_book[8])

                price_entry = tk.Entry(edit_window)
                price_entry.grid(row=7, column=1)
                price_entry.insert(tk.END, selected_book[9])

                publish_year_entry = tk.Entry(edit_window)
                publish_year_entry.grid(row=8, column=1)
                publish_year_entry.insert(tk.END, selected_book[10])

                # Button to update book information
                update_button = tk.Button(edit_window, text="Update", command=update_book_info)
                update_button.grid(row=9, columnspan=2, pady=10)

        # Bind double-click event to show book details
        book_listbox.bind("<Double-Button-1>", show_book_to_edit)

        # Create a back button to return to the main admin page
        back_button = tk.Button(self.root, text="Back", command=self.open_admin_page)
        back_button.pack(pady=5)

    def delete_book(self):
        # Clear the window and show the list of books for deletion
        self.clear_window()
        self.show_book_list_for_deletion()

    def show_book_list_for_deletion(self):
        # Retrieve the list of books from the database
        self.cursor.execute("SELECT book_id, title FROM books")
        books = self.cursor.fetchall()

        # Create a listbox to display the book titles
        book_listbox = tk.Listbox(self.root)
        book_listbox.pack(padx=10, pady=10)

        # Insert each book title into the listbox
        for book in books:
            book_listbox.insert(tk.END, f"{book[1]}")

        # Function to delete book from catalog
        def delete_from_catalog():
            # Get the index of the selected book in the listbox
            selected_index = book_listbox.curselection()
            if selected_index:
                index = int(selected_index[0])
                selected_book_id = books[index][0]

                # Update the catalog flag to 0 for the selected book
                self.cursor.execute("UPDATE books SET catalog_flag = 0 WHERE book_id = %s", (selected_book_id,))
                self.mydb.commit()
                messagebox.showinfo("Success", "Book deleted from catalog successfully.")

                # Description for the admin action
                description = f"Book (ID: {selected_book_id}) removed from catalog"

                # Record admin action
                self.record_admin_action(action_type='remove from catalog', book_id=selected_book_id,
                                         description=description)
                self.open_bookstore_management_page()

        # Function to delete book from database
        def delete_from_database():
            # Get the index of the selected book in the listbox
            selected_index = book_listbox.curselection()
            if selected_index:
                index = int(selected_index[0])
                selected_book_id = books[index][0]

                # Delete the book from the database
                self.cursor.execute("DELETE FROM books WHERE book_id = %s", (selected_book_id,))
                self.mydb.commit()
                messagebox.showinfo("Success", "Book deleted from database successfully.")

                # Description for the admin action
                description = f"Book (ID: {selected_book_id}) removed from database"

                # Record admin action with description
                self.record_admin_action(action_type='remove from database', book_id=selected_book_id,
                                         description=description)
                self.open_bookstore_management_page()

        # Create buttons for deletion options
        delete_catalog_button = tk.Button(self.root, text="Remove from Catalog", command=delete_from_catalog)
        delete_catalog_button.pack(padx=10, pady=5)

        delete_database_button = tk.Button(self.root, text="Remove from Database", command=delete_from_database)
        delete_database_button.pack(padx=10, pady=5)

        # Create a back button to return to the book store management page
        back_button = tk.Button(self.root, text="Back", command=self.open_bookstore_management_page)
        back_button.pack(pady=5)

    def open_manager_page(self):
        # Clear the window and create the manager page
        self.clear_window()
        tk.Label(self.root, text="Welcome Manager", fg="green").grid(row=0, column=0, columnspan=2)

        # Add manager-specific GUI elements here
        # For example, buttons to perform manager actions
        inbox_button = tk.Button(self.root, text="Inbox", command=self.open_manager_inbox)
        inbox_button.grid(row=1, column=0, padx=10, pady=5)

        # Add button for book operations
        book_operations_button = tk.Button(self.root, text="Book Operations", command=self.open_book_operations)
        book_operations_button.grid(row=2, column=0, padx=10, pady=5)

        logout_button = tk.Button(self.root, text="Logout", command=self.create_main_page)
        logout_button.grid(row=1, column=1, padx=10, pady=5)

    def open_book_operations(self):
        # Function to handle insert operation
        def get_manager_id():
            try:
                # Execute a query to retrieve the manager ID where date_out is NULL
                get_manager_query = "SELECT manager_id FROM manager WHERE date_out IS NULL"
                self.cursor.execute(get_manager_query)
                manager_id = self.cursor.fetchone()[0]  # Assuming there's only one manager with date_out NULL
                return manager_id
            except Exception as e:
                # Handle any exceptions (e.g., database connection error, no manager found)
                print("Error retrieving manager ID:", e)
                return None  # Return None if manager ID retrieval fails

        def open_additional_info_window():
            # Function to create a window for entering additional information

            # Function to handle saving the entered information
            def save_info():
                additional_info = info_text.get("1.0", tk.END)  # Retrieve the entered text
                additional_info_window.description = additional_info  # Store the entered text in the window object
                additional_info_window.destroy()  # Close the window

            # Create a new window for entering additional information
            additional_info_window = tk.Toplevel()
            additional_info_window.title("Additional Information")

            # Create a scrolled text box for entering information
            info_text = scrolledtext.ScrolledText(additional_info_window, width=40, height=10)
            info_text.pack(padx=10, pady=10)

            # Create a button to save the entered information
            save_button = tk.Button(additional_info_window, text="Save", command=save_info)
            save_button.pack(pady=5)

            # Make the window wait until it is closed
            additional_info_window.wait_window(additional_info_window)

            # Return the entered text when the window is closed
            return additional_info_window.description if hasattr(additional_info_window, 'description') else ""
        def insert_book():
            # Function to handle the insertion of a book

            def go_back_to_operations():
                # Open the book operations page
                self.clear_window()
                self.open_book_operations()

            def submit_book():
                # Get all the input values
                author = author_entry.get()
                category = category_var.get()
                title = title_entry.get()
                isbn = isbn_entry.get()
                review = review_entry.get()
                publisher = publisher_entry.get()
                minimum_property = minimum_property_entry.get()
                present_stock = present_stock_entry.get()
                price = price_entry.get()
                publish_year = publish_year_entry.get()
                catalog_flag = 1  # Default value

                # Insert the book into the database
                insert_query = "INSERT INTO books (author, category, title, review, isbn,  publisher, minimum_property, present_stock, price, publish_year, catalog_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                self.cursor.execute(insert_query, (
                author, category, title, review, isbn, publisher, minimum_property, present_stock, price, publish_year,
                catalog_flag))
                self.mydb.commit()

                # Show success message
                messagebox.showinfo("Success", "Book inserted successfully.")
                # Assuming insertion into books was successful, proceed to insert into manager_records
                manager_id = get_manager_id()
                operation = "Insert"
                timestamp = datetime.datetime.now()
                description = open_additional_info_window()

                # Insert record into manager_records table
                # Example:
                insert_record_query = "INSERT INTO manager_records (manager_id, book_operations, timestamp, description) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(insert_record_query, (manager_id, operation, timestamp, description))
                self.mydb.commit()

                # Close the book insertion window
                root.destroy()
                self.open_book_operations()

            # Clear the current page
            self.clear_window()

            # Labels and entry fields for book information
            tk.Label(root, text="Author:").grid(row=0, column=0, padx=10, pady=5)
            author_entry = tk.Entry(root)
            author_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(root, text="Category:").grid(row=1, column=0, padx=10, pady=5)
            category_var = tk.StringVar()
            categories = ["Fiction", "Poetry", "Children", "Classic", "Romance", "History", "Psychology",
                          "Travel/Adventure", "Biography/Autobiography"]
            category_combobox = tk.OptionMenu(root, category_var, *categories)
            category_combobox.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(root, text="Title:").grid(row=2, column=0, padx=10, pady=5)
            title_entry = tk.Entry(root)
            title_entry.grid(row=2, column=1, padx=10, pady=5)

            tk.Label(root, text="ISBN:").grid(row=3, column=0, padx=10, pady=5)
            isbn_entry = tk.Entry(root)
            isbn_entry.grid(row=3, column=1, padx=10, pady=5)

            tk.Label(root, text="Review:").grid(row=4, column=0, padx=10, pady=5)
            review_entry = tk.Entry(root)
            review_entry.grid(row=4, column=1, padx=10, pady=5)

            tk.Label(root, text="Publisher:").grid(row=5, column=0, padx=10, pady=5)
            publisher_entry = tk.Entry(root)
            publisher_entry.grid(row=5, column=1, padx=10, pady=5)

            tk.Label(root, text="Minimum Property:").grid(row=6, column=0, padx=10, pady=5)
            minimum_property_entry = tk.Entry(root)
            minimum_property_entry.grid(row=6, column=1, padx=10, pady=5)

            tk.Label(root, text="Present Stock:").grid(row=7, column=0, padx=10, pady=5)
            present_stock_entry = tk.Entry(root)
            present_stock_entry.grid(row=7, column=1, padx=10, pady=5)

            tk.Label(root, text="Price:").grid(row=8, column=0, padx=10, pady=5)
            price_entry = tk.Entry(root)
            price_entry.grid(row=8, column=1, padx=10, pady=5)

            tk.Label(root, text="Publish Year:").grid(row=9, column=0, padx=10, pady=5)
            publish_year_entry = tk.Entry(root)
            publish_year_entry.grid(row=9, column=1, padx=10, pady=5)

            # Submit button
            submit_button = tk.Button(root, text="Submit", command=submit_book)
            submit_button.grid(row=10, column=0, columnspan=2, pady=10)

            # Create a button to open book operations
            back_button = tk.Button(self.root, text="Back", command=go_back_to_operations)
            back_button.grid(row=11, column=0, columnspan=2, pady=10)

        # Function to handle modify operation
        def modify_book():
            self.refresh_database_connection()
            # Declare entry fields and category variable as global
            global author_entry, category_var, title_entry, isbn_entry, review_entry
            global publisher_entry, minimum_property_entry, present_stock_entry, price_entry, publish_year_entry

            def get_all_books():
                try:
                    # Execute query to retrieve all books
                    self.cursor.execute("SELECT * FROM books")
                    return self.cursor.fetchall()
                except mysql.connector.Error as err:
                    print("Error:", err)
                    return []

            def populate_book_list():
                books = get_all_books()
                for book in books:
                    book_listbox.insert(tk.END, f"{book[0]} - {book[2]}")  # Book ID and Title

            def select_book(event):
                # Get the selected book's ID
                selected_index = book_listbox.curselection()
                if selected_index:
                    selected_book_id = book_listbox.get(selected_index)[0]  # Extract book ID
                    populate_book_details(selected_book_id)

            def populate_book_details(book_id):
                try:
                    # Execute query to retrieve book details by ID
                    self.cursor.execute("SELECT * FROM books WHERE book_id = %s", (book_id,))
                    book_details = self.cursor.fetchone()

                    if book_details:
                        # Initialize a dictionary to store the changes
                        changes = {}

                        # Define the index mappings for each field in the book_details tuple
                        field_indices = {
                            'author': 1,
                            'category': 2,
                            'title': 3,
                            'isbn': 4,
                            'review': 5,
                            'publisher': 6,
                            'minimum_property': 7,
                            'present_stock': 8,
                            'price': 9,
                            'publish_year': 10
                        }

                        # Get the old values directly from the entry widgets
                        old_values = {
                            'author': author_entry.get(),
                            'category': category_var.get(),
                            'title': title_entry.get(),
                            'isbn': isbn_entry.get(),
                            'review': review_entry.get(),
                            'publisher': publisher_entry.get(),
                            'minimum_property': minimum_property_entry.get(),
                            'present_stock': present_stock_entry.get(),
                            'price': price_entry.get(),
                            'publish_year': publish_year_entry.get()
                        }

                        # Update entry fields with book details
                        author_entry.delete(0, tk.END)
                        author_entry.insert(tk.END, book_details[1])
                        category_var.set(book_details[2])
                        title_entry.delete(0, tk.END)
                        title_entry.insert(tk.END, book_details[3])
                        isbn_entry.delete(0, tk.END)
                        isbn_entry.insert(tk.END, book_details[4])
                        review_entry.delete(0, tk.END)
                        review_entry.insert(tk.END, book_details[5])
                        publisher_entry.delete(0, tk.END)
                        publisher_entry.insert(tk.END, book_details[6])
                        minimum_property_entry.delete(0, tk.END)
                        minimum_property_entry.insert(tk.END, book_details[7])

                        # Check if present_stock_entry is not empty before inserting value
                        present_stock_value = book_details[8] if book_details[8] else 0
                        present_stock_entry.delete(0, tk.END)
                        present_stock_entry.insert(tk.END, present_stock_value)

                        price_entry.delete(0, tk.END)
                        price_entry.insert(tk.END, book_details[9])
                        publish_year_entry.delete(0, tk.END)
                        publish_year_entry.insert(tk.END, book_details[10])

                        # Track changes and store old values
                        for field, index in field_indices.items():
                            old_value = old_values[field]
                            new_value = book_details[index]
                            print(f"Field: {field}, Old Value: {old_value}, New Value: {new_value}")
                            if field == 'price':
                                old_value = Decimal(old_value) if old_value else Decimal(0)
                                new_value = Decimal(new_value)
                            if old_value != new_value:
                                changes[field] = (old_value, new_value)
                    else:
                        print("No book found with the provided ID.")
                        return None
                except mysql.connector.Error as err:
                    print("Error:", err)
                    return None

            def save_changes():
                # Get the modified information
                author = author_entry.get()
                category = category_var.get()
                title = title_entry.get()
                isbn = isbn_entry.get()
                review = review_entry.get()
                publisher = publisher_entry.get()
                minimum_property = minimum_property_entry.get()
                present_stock = present_stock_entry.get()
                price = price_entry.get()
                publish_year = publish_year_entry.get()

                try:
                    # Get the selected book's ID
                    selected_index = book_listbox.curselection()
                    if selected_index:
                        selected_book_id = book_listbox.get(selected_index)[0]

                        # Update the book in the database
                        update_query = "UPDATE books SET author = %s, category = %s, title = %s, isbn = %s, review = %s, publisher = %s, minimum_property = %s, present_stock = %s, price = %s, publish_year = %s WHERE book_id = %s"
                        self.cursor.execute(update_query, (
                            author, category, title, isbn, review, publisher, minimum_property, present_stock, price,
                            publish_year, selected_book_id))
                        self.mydb.commit()
                        messagebox.showinfo("Success", "Book details updated successfully.")

                        # Record the book modification in manager_records
                        manager_id = get_manager_id()
                        operation = "Modify"
                        timestamp = datetime.datetime.now()
                        description = open_additional_info_window()
                        insert_record_query = "INSERT INTO manager_records (manager_id, book_operations, timestamp, description) VALUES (%s, %s, %s, %s)"
                        self.cursor.execute(insert_record_query, (manager_id, operation, timestamp, description))
                        self.mydb.commit()

                        # Clear the entry fields
                        clear_entry_fields()
                    else:
                        messagebox.showwarning("Warning", "No book selected.")
                except mysql.connector.Error as err:
                    print("Error:", err)

            def clear_entry_fields():
                # Clear all entry fields
                author_entry.delete(0, tk.END)
                category_var.set("")
                title_entry.delete(0, tk.END)
                isbn_entry.delete(0, tk.END)
                review_entry.delete(0, tk.END)
                publisher_entry.delete(0, tk.END)
                minimum_property_entry.delete(0, tk.END)
                present_stock_entry.delete(0, tk.END)
                price_entry.delete(0, tk.END)
                publish_year_entry.delete(0, tk.END)

            def go_back_to_operations():
                # Open the book operations page
                self.clear_window()
                self.open_book_operations()

            # Clear the current page
            self.clear_window()

            # Create a listbox to display all books
            book_listbox = tk.Listbox(self.root, width=50, height=10)
            book_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
            book_listbox.bind("<<ListboxSelect>>", select_book)
            populate_book_list()

            # Labels and entry fields for book information
            tk.Label(self.root, text="Author:").grid(row=1, column=0, padx=10, pady=5)
            author_entry = tk.Entry(self.root)
            author_entry.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(self.root, text="Category:").grid(row=2, column=0, padx=10, pady=5)
            category_var = tk.StringVar()
            categories = ["Fiction", "Poetry", "Children", "Classic", "Romance", "History", "Psychology",
                          "Travel/Adventure", "Biography/Autobiography"]
            category_combobox = tk.OptionMenu(self.root, category_var, *categories)
            category_combobox.grid(row=2, column=1, padx=10, pady=5)

            tk.Label(self.root, text="Title:").grid(row=3, column=0, padx=10, pady=5)
            title_entry = tk.Entry(self.root)
            title_entry.grid(row=3, column=1, padx=10, pady=5)

            tk.Label(self.root, text="ISBN:").grid(row=4, column=0, padx=10, pady=5)
            isbn_entry = tk.Entry(self.root)
            isbn_entry.grid(row=4, column=1, padx=10, pady=5)

            tk.Label(self.root, text="Review:").grid(row=5, column=0, padx=10, pady=5)
            review_entry = tk.Entry(self.root)
            review_entry.grid(row=5, column=1, padx=10, pady=5)

            tk.Label(self.root, text="Publisher:").grid(row=6, column=0, padx=10, pady=5)
            publisher_entry = tk.Entry(self.root)
            publisher_entry.grid(row=6, column=1, padx=10, pady=5)

            tk.Label(self.root, text="Minimum Property:").grid(row=7, column=0, padx=10, pady=5)
            minimum_property_entry = tk.Entry(self.root)
            minimum_property_entry.grid(row=7, column=1, padx=10, pady=5)

            tk.Label(self.root, text="Present Stock:").grid(row=8, column=0, padx=10, pady=5)
            present_stock_entry = tk.Entry(self.root)
            present_stock_entry.grid(row=8, column=1, padx=10, pady=5)

            tk.Label(self.root, text="Price:").grid(row=9, column=0, padx=10, pady=5)
            price_entry = tk.Entry(self.root)
            price_entry.grid(row=9, column=1, padx=10, pady=5)

            tk.Label(self.root, text="Publish Year:").grid(row=10, column=0, padx=10, pady=5)
            publish_year_entry = tk.Entry(self.root)
            publish_year_entry.grid(row=10, column=1, padx=10, pady=5)

            # Submit button
            submit_button = tk.Button(self.root, text="Save Changes", command=save_changes)
            submit_button.grid(row=11, column=0, columnspan=2, pady=10)

            # Create a button to go back to book operations
            back_button = tk.Button(self.root, text="Back", command=go_back_to_operations)
            back_button.grid(row=12, column=0, columnspan=2, pady=10)

        # Function to handle delete operation
        def add_manager_record(manager_id, operation, description):
            try:
                timestamp = datetime.datetime.now()
                insert_record_query = "INSERT INTO manager_records (manager_id, book_operations, timestamp, description) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(insert_record_query, (manager_id, operation, timestamp, description))
                self.mydb.commit()
            except mysql.connector.Error as err:
                print("Error:", err)

        def delete_book():
            try:
                # Fetch all books from the database
                self.cursor.execute("SELECT * FROM books")
                books = self.cursor.fetchall()

                # Display the list of books in a separate window
                delete_window = tk.Toplevel()
                delete_window.title("Delete Book")

                # Create a listbox to display all books
                book_listbox = tk.Listbox(delete_window, width=50, height=10)
                book_listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

                for book in books:
                    book_listbox.insert(tk.END, f"{book[0]} - {book[3]}")  # Book ID and Title

                def delete_selected_book():
                    # Get the selected book's ID
                    selected_index = book_listbox.curselection()
                    if selected_index:
                        selected_book_id = books[selected_index[0]][0]  # Extract book ID

                        # Ask the manager for confirmation before deleting
                        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this book?")
                        if confirmation:
                            # Delete the book based on the manager's choice
                            delete_type = delete_choice.get()
                            if delete_type == 0:
                                # Soft delete: Set the catalog_flag to 0
                                self.cursor.execute("UPDATE books SET catalog_flag = 0 WHERE book_id = %s",
                                                    (selected_book_id,))
                                self.mydb.commit()
                                messagebox.showinfo("Success", "Book deleted from catalog successfully.")
                                description = open_additional_info_window()
                                add_manager_record(get_manager_id(), "Delete", description)
                            elif delete_type == 1:
                                # Hard delete: Remove the book from the database
                                self.cursor.execute("DELETE FROM books WHERE book_id = %s", (selected_book_id,))
                                self.mydb.commit()
                                messagebox.showinfo("Success", "Book deleted from database successfully.")
                                description = open_additional_info_window()
                                add_manager_record(get_manager_id(), "Delete", description)
                            else:
                                messagebox.showwarning("Warning", "Invalid delete choice.")
                            # Close the delete window after deletion
                            delete_window.destroy()

                # Radio buttons to choose delete type
                delete_choice = tk.IntVar()
                tk.Radiobutton(delete_window, text="<Delete from catalog>", variable=delete_choice, value=0).grid(row=1,
                                                                                                                  column=0)
                tk.Radiobutton(delete_window, text="<Delete from database>", variable=delete_choice, value=1).grid(
                    row=1, column=1)

                # Button to confirm deletion
                delete_button = tk.Button(delete_window, text="Delete", command=delete_selected_book)
                delete_button.grid(row=2, column=0, columnspan=2, pady=10)

            except mysql.connector.Error as err:
                print("Error:", err)

        # Create a new window for book operations
        book_operations_window = tk.Toplevel(self.root)
        book_operations_window.title("Book Operations")

        # Buttons for book operations
        insert_button = tk.Button(book_operations_window, text="Insert", command=insert_book)
        insert_button.pack(pady=10)

        modify_button = tk.Button(book_operations_window, text="Modify", command=modify_book)
        modify_button.pack(pady=10)

        delete_button = tk.Button(book_operations_window, text="Delete", command=delete_book)
        delete_button.pack(pady=10)

        # Back button
        back_button = tk.Button(book_operations_window, text="Back", command=book_operations_window.destroy)
        back_button.pack(pady=10)
############################## new
    def open_manager_inbox(self):
        # Clear the window
        self.clear_window()

        # Refresh the database connection
        self.refresh_database_connection()

        # Retrieve the present manager ID
        self.get_present_manager_id()

        # Retrieve messages from the manager's inbox
        self.cursor.execute("SELECT msg_box FROM manager WHERE manager_id = %s", (self.manager_id,))
        inbox_messages = self.cursor.fetchall()

        if inbox_messages:
            # Split messages by comma to separate them
            messages = inbox_messages[0][0].split(',')

            # Create a listbox to display message subjects
            message_listbox = tk.Listbox(self.root, width=50, height=10)
            message_listbox.pack(fill="both", expand=True, padx=10, pady=10)

            # Populate the listbox with message subjects (without quantity)
            for msg in messages:
                parts = msg.split(":")
                if len(parts) >= 2:
                    subject = parts[1].strip()  # Extract subject without quantity
                    message_listbox.insert(tk.END, subject)
                else:
                    message_listbox.insert(tk.END, msg)  # Insert the whole message

            # Function to display full message on selection
            def show_full_message(event):
                # Get the index of the selected item
                index = message_listbox.curselection()[0]

                # Create a new window to display full message
                full_message_window = tk.Toplevel(self.root)
                full_message_window.title("Full Message")

                # Retrieve and display the full message
                full_message = messages[index].strip()  # Get the selected full message
                full_message_text = tk.Text(full_message_window)
                full_message_text.insert(tk.END, full_message)
                full_message_text.pack(fill="both", expand=True, padx=10, pady=10)
                full_message_text.configure(state="disabled")

                # Function to handle accepting the message
                def open_additional_info_window(parent):
                    additional_info = None

                    def submit_info():
                        nonlocal additional_info
                        additional_info = info_entry.get()
                        window.destroy()

                    window = tk.Toplevel(parent)
                    window.title("Additional Information")

                    info_label = tk.Label(window, text="Enter additional information:")
                    info_label.pack(pady=10)

                    info_entry = tk.Entry(window, width=40)
                    info_entry.pack(pady=5)

                    submit_button = tk.Button(window, text="Submit", command=submit_info)
                    submit_button.pack(pady=5)

                    window.wait_window()  # Wait for the window to be closed before continuing

                    return additional_info

                # Now you can use this function in your accept_message and decline_message functions like this:

                # Function to handle accepting the message
                def accept_message():
                    try:
                        # Get the index of the selected item
                        index = message_listbox.curselection()[0]

                        # Get the full message
                        full_message = messages[index].strip()

                        # Parse the message to extract book ID and quantity
                        parts = full_message.split(":")
                        book_id = int(parts[0].split()[-1])
                        quantity = int(parts[1].split()[-1])

                        # Open a new window for additional information input
                        additional_info = open_additional_info_window(self.root)

                        try:
                            # Update the quantity of the book in the database
                            update_query = "UPDATE books SET present_stock = %s WHERE book_id = %s"
                            self.cursor.execute(update_query, (quantity, book_id))
                            self.mydb.commit()

                            # Insert a record into manager_record table for accepting the order
                            insert_record_query = "INSERT INTO manager_records (manager_id, description, orders_to_add, timestamp) VALUES (%s, %s, %s, NOW())"
                            description = f"Accepted order: Book ID {book_id}. Quantity changed to {quantity}. Additional info: {additional_info}"
                            self.cursor.execute(insert_record_query,
                                                (self.manager_id, description, f"Accepted for Book ID {book_id}"))
                            self.mydb.commit()

                            # Get the ID of the active admin
                            active_admin_query = "SELECT admin_id FROM admin WHERE is_active = 1"
                            self.cursor.execute(active_admin_query)
                            active_admin_id = self.cursor.fetchone()[0]

                            # Insert a new message into the active admin's message box
                            admin_message = f"Order for book ID {book_id} accepted. Quantity updated."
                            insert_query = "UPDATE admin SET msg_box = CONCAT(msg_box, %s) WHERE admin_id = %s"
                            self.cursor.execute(insert_query, (f", {admin_message}", active_admin_id))
                            self.mydb.commit()

                            # Show success message
                            messagebox.showinfo("Success", "Order accepted. Quantity updated.")
                        except mysql.connector.Error as err:
                            # Handle any errors
                            print("Error:", err)
                            messagebox.showerror("Error", "Failed to accept the order.")
                    except Exception as e:
                        print("Error:", e)

                # Function to handle declining the message
                def decline_message():
                    try:
                        # Get the index of the selected item
                        index = message_listbox.curselection()[0]

                        # Get the full message
                        full_message = messages[index].strip()

                        # Open a new window for additional information input
                        additional_info = open_additional_info_window(self.root)

                        # Parse the message to extract book ID and quantity
                        parts = full_message.split(":")
                        book_id = int(parts[0].split()[-1])

                        # Insert a record into manager_record table for declining the order
                        insert_record_query = "INSERT INTO manager_records (manager_id, description, orders_to_add, timestamp) VALUES (%s, %s, %s, NOW())"
                        description = f"Declined order: {full_message}. Additional info: {additional_info}"
                        self.cursor.execute(insert_record_query,
                                            (self.manager_id, description, f"Declined for Book ID {book_id}"))
                        self.mydb.commit()

                        # Get the ID of the active admin
                        active_admin_query = "SELECT admin_id FROM admin WHERE is_active = 1"
                        self.cursor.execute(active_admin_query)
                        active_admin_id = self.cursor.fetchone()[0]

                        # Insert a new message into the active admin' s message box
                        admin_message = f"Order declined: {full_message}"
                        insert_query = "UPDATE admin SET msg_box = CONCAT(msg_box, %s) WHERE admin_id = %s"
                        self.cursor.execute(insert_query, (f", {admin_message}", active_admin_id))
                        self.mydb.commit()

                        # Show success message
                        messagebox.showinfo("Success", "Order declined successfully. Message sent to admin.")
                    except Exception as e:
                        print("Error:", e)
                        messagebox.showerror("Error", "Failed to decline the order.")

                # Function to handle deleting the message
                def delete_message():
                    try:
                        # Get the index of the selected item
                        index = message_listbox.curselection()[0]

                        # Retrieve the current messages from the manager's message box
                        self.cursor.execute("SELECT msg_box FROM manager WHERE manager_id = %s", (self.manager_id,))
                        manager_messages = self.cursor.fetchone()[0]
                        messages = manager_messages.split(',')

                        # Remove the selected message from the list of messages
                        updated_messages = [msg for i, msg in enumerate(messages) if i != index]

                        # Update the manager's message box with the remaining messages
                        updated_msg_string = ','.join(updated_messages)
                        update_query = "UPDATE manager SET msg_box = %s WHERE manager_id = %s"
                        self.cursor.execute(update_query, (updated_msg_string, self.manager_id))
                        self.mydb.commit()

                        # Show success message
                        messagebox.showinfo("Delete", "Message deleted successfully")

                        # Refresh the inbox to reflect changes
                        self.open_manager_inbox()
                    except Exception as e:
                        # Handle any errors
                        print("Error:", e)
                        messagebox.showerror("Error", "Failed to delete the message")

                # Create buttons for accept, decline, and delete
                accept_button = tk.Button(full_message_window, text="Accept", command=accept_message)
                accept_button.pack(side="left", padx=5, pady=5)

                decline_button = tk.Button(full_message_window, text="Decline", command=decline_message)
                decline_button.pack(side="left", padx=5, pady=5)

                delete_button = tk.Button(full_message_window, text="Delete", command=delete_message)
                delete_button.pack(side="left", padx=5, pady=5)

            # Bind the show_full_message function to double-click event on message listbox
            message_listbox.bind("<Double-Button-1>", show_full_message)
        else:
            # If there are no messages, display a message indicating so
            tk.Label(self.root, text="No messages in the inbox", fg="red").pack(pady=10)

        # Create a back button to return to the manager page
        back_button = tk.Button(self.root, text="Back", command=self.open_manager_page)
        back_button.pack(pady=10)

    def refresh_database_connection(self):
        try:
            # Commit any pending changes
            self.mydb.commit()
        except mysql.connector.Error as err:
            print("Error committing changes:", err)
            # Rollback changes if there's an error
            self.mydb.rollback()

        # Close the current cursor
        self.cursor.close()

        # Reopen the database connection and cursor
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ehsan",
            database="Book_Store"
        )
        self.cursor = self.mydb.cursor()

    def get_present_manager_id(self):
        # Query to retrieve manager ID based on username
        query = "SELECT manager_id FROM manager WHERE date_out IS NULL "
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        if result:
            self.manager_id = result[0]
        else:
            messagebox.showerror("Error", "Manager not found")

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
        self.cursor.execute("SELECT inbox FROM users WHERE username = %s", (self.logged_in_username,))
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
