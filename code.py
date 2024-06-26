import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, scrolledtext, simpledialog, filedialog, Toplevel
from DataBase_Connection import get_database_connection
import mysql.connector
import datetime
# import random
# from decimal import Decimal
import re
from Reports import ManagerReports  # Import the Reports class from reports.py
from Reports import AdminReports
from recommendation_system import RecommendationSystem
from PlaceHolder import PlaceholderEntry
# import traceback
from Retirement import Retirement
import os
from PIL import Image, ImageTk
import shutil


class BookstoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bookstore")
        self.root.attributes('-fullscreen', True)
        self.is_logged_in = False
        self.logged_in_username = None
        self.logged_in_lastName = None
        self.logged_in_id = None
        self.is_admin = False  # Flag to indicate admin login status
        self.manager_id = None
        self.cart = {}
        self.recommendation_system = RecommendationSystem()
        self.retirement = Retirement(self)
        self.placeholder = PlaceholderEntry()

        # Get the database connection
        self.mydb, self.cursor = get_database_connection()

        # Create GUI elements
        self.create_main_page()

    def create_main_page(self):
        # Clear the window and create main page elements
        self.clear_window()

        # Define custom styles
        title_font = ("Helvetica", 16, "bold")
        section_font = ("Helvetica", 14, "bold")
        button_font = ("Helvetica", 12)

        # Main frame
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center main frame within the window

        # Search Frame
        search_frame = tk.LabelFrame(main_frame, text="Search Books", font=section_font, bg="#f9f9f9", fg="#333333",
                                     bd=2, relief="groove")
        search_frame.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # Entry for search text with placeholder
        self.search_entry = PlaceholderEntry(search_frame, placeholder="Search the books here...", font=button_font, bd=2,
                                             relief="sunken")
        self.search_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Combobox for search type
        self.search_type = ttk.Combobox(search_frame, values=["Title", "Author", "Publisher"], font=button_font)
        self.search_type.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.search_type.current(0)  # Set default value

        tk.Button(search_frame, text="Search", command=self.search_books, width=15, font=button_font, bg="#4CAF50",
                  fg="white").grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.search_results_listbox = tk.Listbox(search_frame, height=10, width=80, font=button_font, bd=2,
                                                 relief="sunken")
        self.search_results_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        # Book Info Button
        tk.Button(search_frame, text="Book Info", command=self.show_book_info, font=button_font, bg="#4CAF50",
                  fg="white").grid(row=2, column=2, padx=10, pady=10, sticky="ew")

        # User Actions Frame
        user_actions_frame = tk.LabelFrame(main_frame, text="User Actions", font=section_font, bg="#f9f9f9",
                                           fg="#333333", bd=2, relief="groove")
        user_actions_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        tk.Button(user_actions_frame, text="Sign In", command=self.show_sign_in_page, font=button_font, bg="#2196F3",
                  fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        tk.Button(user_actions_frame, text="Sign Up", command=self.show_sign_up_page, font=button_font, bg="#2196F3",
                  fg="white").grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Admin & Manager Actions Frame
        admin_manager_frame = tk.LabelFrame(main_frame, text="Admin & Manager Actions", font=section_font,
                                            bg="#f9f9f9",
                                            fg="#333333", bd=2, relief="groove")
        admin_manager_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        tk.Button(admin_manager_frame, text="Admin Login", command=self.show_admin_login_page, font=button_font,
                  bg="#FF9800", fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        tk.Button(admin_manager_frame, text="Manager Login", command=self.show_manager_login_page, font=button_font,
                  bg="#FF9800", fg="white").grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Cart Actions Frame
        cart_actions_frame = tk.LabelFrame(main_frame, text="Cart Actions", font=section_font, bg="#f9f9f9",
                                           fg="#333333", bd=2, relief="groove")
        cart_actions_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        tk.Button(cart_actions_frame, text="Add to Cart", command=self.add_to_cart, font=button_font, bg="#9C27B0",
                  fg="white").grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        tk.Button(cart_actions_frame, text="View Cart", command=self.view_cart, font=button_font, bg="#9C27B0",
                  fg="white").grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(cart_actions_frame, text="Proceed to Checkout", command=self.not_logged_in_warning, font=button_font,
                  bg="#9C27B0", fg="white").grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        # Exit Button
        tk.Button(main_frame, text="Exit", command=self.root.quit, font=button_font, bg="#FF5733",
                  fg="white").grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # Login Status Label
        self.login_status_label = tk.Label(user_actions_frame, text="", fg="red", font=button_font, bg="#ffffff")
        self.login_status_label.grid(row=0, column=2, padx=10, pady=10, sticky="ew", columnspan=3)

        self.update_login_status()

    def not_logged_in_warning(self):
        # Clear the window
        self.clear_window()

        # Display the warning message
        tk.Label(self.root, text="Warning", font=("Helvetica", 14), fg="red").grid(row=0, column=0, columnspan=2,
                                                                                   pady=10)
        tk.Label(self.root, text="Please login first", font=("Helvetica", 16), fg="red").grid(row=1, column=0, columnspan=2, pady=5)

        # Create buttons to redirect the user
        tk.Button(self.root, text="Go to Sign Up Page", command=self.show_sign_up_page).grid(row=2, column=0, padx=10,
                                                                                             pady=5)
        tk.Button(self.root, text="Go to Main Page", command=self.create_main_page).grid(row=2, column=1, padx=10,
                                                                                         pady=5)

    def show_sign_in_page(self):
        # Clear the window and create sign-in page elements
        self.clear_window()

        # Define custom styles
        title_font = ("Helvetica", 16, "bold")
        label_font = ("Helvetica", 14)
        entry_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12, "bold")

        # Main frame to center the content
        sign_in_frame = tk.Frame(self.root, bg="#f0f0f0")
        sign_in_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        self.sign_in_label = tk.Label(sign_in_frame, text="Sign In", font=title_font, bg="#f0f0f0", fg="#333333")
        self.sign_in_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username Label and Entry
        self.username_label = tk.Label(sign_in_frame, text="Username:", font=label_font, bg="#f0f0f0", fg="#333333")
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(sign_in_frame, font=entry_font, bd=2, relief="sunken")
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Password Label and Entry
        self.password_label = tk.Label(sign_in_frame, text="Password:", font=label_font, bg="#f0f0f0", fg="#333333")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(sign_in_frame, font=entry_font, bd=2, relief="sunken", show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Sign In Button
        self.sign_in_button = tk.Button(sign_in_frame, text="Sign In", font=button_font, bg="#4CAF50", fg="white",
                                        command=self.validate_and_sign_in, width=20)
        self.sign_in_button.grid(row=3, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

        # Back Button
        self.back_button = tk.Button(sign_in_frame, text="Back", font=button_font, bg="#FF5733", fg="white",
                                     command=self.create_main_page, width=20)
        self.back_button.grid(row=4, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="ew")

        # Configure column weights to ensure proper stretching
        sign_in_frame.columnconfigure(0, weight=1)
        sign_in_frame.columnconfigure(1, weight=1)

    def show_admin_login_page(self):
        # Clear the window and create admin login page elements
        self.clear_window()

        # Define custom styles
        title_font = ("Helvetica", 16, "bold")
        label_font = ("Helvetica", 14)
        entry_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12, "bold")

        # Main frame to center the content
        admin_login_frame = tk.Frame(self.root, bg="#f0f0f0")
        admin_login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        self.admin_login_label = tk.Label(admin_login_frame, text="Admin Login", font=title_font, bg="#f0f0f0",
                                          fg="#333333")
        self.admin_login_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username Label and Entry
        self.username_label = tk.Label(admin_login_frame, text="Username:", font=label_font, bg="#f0f0f0", fg="#333333")
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(admin_login_frame, font=entry_font, bd=2, relief="sunken")
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Password Label and Entry
        self.password_label = tk.Label(admin_login_frame, text="Password:", font=label_font, bg="#f0f0f0", fg="#333333")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(admin_login_frame, font=entry_font, bd=2, relief="sunken", show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Login Button
        self.admin_login_button = tk.Button(admin_login_frame, text="Login", font=button_font, bg="#4CAF50", fg="white",
                                            command=self.validate_and_sign_in_admin, width=20)
        self.admin_login_button.grid(row=3, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

        # Back Button
        self.back_button = tk.Button(admin_login_frame, text="Back", font=button_font, bg="#FF5733", fg="white",
                                     command=self.create_main_page, width=20)
        self.back_button.grid(row=4, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="ew")

        # Configure column weights to ensure proper stretching
        admin_login_frame.columnconfigure(0, weight=1)
        admin_login_frame.columnconfigure(1, weight=1)

    def show_manager_login_page(self):
        # Clear the window and create manager login page elements
        self.clear_window()

        # Define custom styles
        title_font = ("Helvetica", 16, "bold")
        label_font = ("Helvetica", 14)
        entry_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12, "bold")

        # Main frame to center the content
        manager_login_frame = tk.Frame(self.root, bg="#f0f0f0")
        manager_login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        self.manager_login_label = tk.Label(manager_login_frame, text="Manager Login", font=title_font, bg="#f0f0f0",
                                            fg="#333333")
        self.manager_login_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username Label and Entry
        self.username_label = tk.Label(manager_login_frame, text="Username:", font=label_font, bg="#f0f0f0",
                                       fg="#333333")
        self.username_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.username_entry = tk.Entry(manager_login_frame, font=entry_font, bd=2, relief="sunken")
        self.username_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Password Label and Entry
        self.password_label = tk.Label(manager_login_frame, text="Password:", font=label_font, bg="#f0f0f0",
                                       fg="#333333")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = tk.Entry(manager_login_frame, font=entry_font, bd=2, relief="sunken", show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Login Button
        self.manager_login_button = tk.Button(manager_login_frame, text="Login", font=button_font, bg="#4CAF50",
                                              fg="white",
                                              command=self.validate_and_sign_in_manager, width=20)
        self.manager_login_button.grid(row=3, column=0, columnspan=2, pady=20, padx=10, sticky="ew")

        # Back Button
        self.back_button = tk.Button(manager_login_frame, text="Back", font=button_font, bg="#FF5733", fg="white",
                                     command=self.create_main_page, width=20)
        self.back_button.grid(row=4, column=0, columnspan=2, pady=(10, 0), padx=10, sticky="ew")

        # Configure column weights to ensure proper stretching
        manager_login_frame.columnconfigure(0, weight=1)
        manager_login_frame.columnconfigure(1, weight=1)

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
            self.logged_in_username = user[1]  # Assuming the name is in the fourth column
            self.logged_in_lastName = user[4]  # last name
            self.logged_in_id = user[0]  # first name
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
        self.cursor.execute("SELECT admin_id FROM admin WHERE username = %s AND password = %s AND date_out IS NULL",
                            (username, password))
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
        self.cursor.execute("SELECT * FROM manager WHERE full_name = %s AND password = %s AND date_out IS NULL",
                            (username, password))
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

        # Define custom styles
        title_font = ("Helvetica", 24, "bold")
        button_font = ("Helvetica", 14, "bold")
        button_bg = "#3498DB"
        button_fg = "white"
        button_hover_bg = "#2980B9"
        frame_bg = "#f0f8ff"
        title_fg = "#2C3E50"

        # Main frame to center the content
        admin_frame = tk.Frame(self.root, bg=frame_bg, bd=10, relief="raised")
        admin_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        welcome_label = tk.Label(admin_frame, text="Welcome Admin", font=title_font, fg=title_fg, bg=frame_bg)
        welcome_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Button style function
        def style_button(button):
            button.configure(font=button_font, bg=button_bg, fg=button_fg, activebackground=button_hover_bg, bd=5,
                             relief="raised", width=40, height=2)

        # Manage Bookstore Button
        manage_bookstore_button = tk.Button(admin_frame, text="Manage Bookstore",
                                            command=self.open_bookstore_management_page)
        style_button(manage_bookstore_button)
        manage_bookstore_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # List Books Button
        list_books_button = tk.Button(admin_frame, text="List of the Books", command=self.show_book_list)
        style_button(list_books_button)
        list_books_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Place Orders Button
        place_orders_button = tk.Button(admin_frame, text="Place Orders", command=self.open_place_orders_window)
        style_button(place_orders_button)
        place_orders_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Inbox Button
        inbox_button = tk.Button(admin_frame, text="Inbox", command=self.open_admin_inbox)
        style_button(inbox_button)
        inbox_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Reports Button
        admin_reports_button = tk.Button(admin_frame, text="Reports", command=self.open_admin_reports)
        style_button(admin_reports_button)
        admin_reports_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # Retirement Button
        retirement_button = tk.Button(admin_frame, text="Retirement", command=self.open_admin_retirement_page)
        style_button(retirement_button)
        retirement_button.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

        # Back Button
        back_button = tk.Button(admin_frame, text="Back", command=self.show_admin_login_page)
        style_button(back_button)
        back_button.configure(bg="#E74C3C", activebackground="#C0392B")
        back_button.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # Configure column weights to ensure proper stretching
        admin_frame.columnconfigure(0, weight=1)
        admin_frame.columnconfigure(1, weight=1)

    def open_admin_reports(self):
        reports_admin = AdminReports(self.root)  # Create an instance of the Reports class
        # Call the manager_report method on the instance to open the reports window
        reports_admin.create_report_window()

    def open_admin_retirement_page(self):
        self.retirement.show_retire_admin_page(self.root)

    def open_place_orders_window(self):
        # Create a new window for placing orders
        place_orders_window = tk.Toplevel(self.root)
        place_orders_window.title("Place Orders")

        # Frame to organize widgets
        frame = tk.Frame(place_orders_window, bg="#f0f0f0")
        frame.pack(padx=20, pady=20)

        # Retrieve the list of books from the database
        self.cursor.execute("SELECT book_id, title, present_stock, minimum_property FROM books")
        books_data = self.cursor.fetchall()

        # Label to prompt book selection
        select_book_label = tk.Label(frame, text="Select a Book:", font=("Helvetica", 12), bg="#f0f0f0")
        select_book_label.grid(row=0, column=0, padx=10, pady=5)

        # Listbox to display book titles
        book_listbox = tk.Listbox(frame, width=50, height=10, font=("Helvetica", 10), bd=2, relief="sunken")
        book_listbox.grid(row=1, column=0, padx=10, pady=5)

        # Populate the listbox with book titles
        for book in books_data:
            book_listbox.insert(tk.END, f"{book[1]} (ID: {book[0]})")

        # Function to show book details
        def show_book_details():
            # Get the selected book index
            selected_index = book_listbox.curselection()
            if selected_index:
                index = int(selected_index[0])
                selected_book = books_data[index]

                # Frame to display book details
                details_frame = tk.Frame(frame, bg="#f0f0f0")
                details_frame.grid(row=1, column=1, padx=10, pady=5)

                # Display book details
                quantity_label = tk.Label(details_frame, text=f"Quantity: {selected_book[2]}", font=("Helvetica", 10),
                                          bg="#f0f0f0")
                quantity_label.grid(row=0, column=0, padx=10, pady=5)

                min_property_label = tk.Label(details_frame, text=f"Minimum Property: {selected_book[3]}",
                                              font=("Helvetica", 10), bg="#f0f0f0")
                min_property_label.grid(row=1, column=0, padx=10, pady=5)

                # Entry field for the new quantity to order
                new_quantity_entry = tk.Entry(details_frame, font=("Helvetica", 10), bd=2, relief="sunken")
                new_quantity_entry.grid(row=2, column=0, padx=10, pady=5)

                # Create the confirm button and pass it to the place_order function
                confirm_button = tk.Button(details_frame, text="Place Order", font=("Helvetica", 10, "bold"),
                                           bg="#4CAF50", fg="white",
                                           command=lambda: self.place_order(new_quantity_entry, selected_book,
                                                                            confirm_button))
                confirm_button.grid(row=3, column=0, padx=10, pady=5)

        # Button to show book details
        show_details_button = tk.Button(frame, text="Show Details", font=("Helvetica", 12), bg="#4CAF50", fg="white",
                                        command=show_book_details)
        show_details_button.grid(row=1, column=1, padx=10, pady=5)

        # Create a back button
        back_button = tk.Button(frame, text="Back", font=("Helvetica", 12), bg="#FF5733", fg="white",
                                command=self.open_admin_page)
        back_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        # Configure column weights to ensure proper stretching
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

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

        # Define custom styles
        title_font = ("Helvetica", 24, "bold")
        button_font = ("Helvetica", 14, "bold")
        button_bg = "#3498DB"
        button_fg = "white"
        button_hover_bg = "#2980B9"
        frame_bg = "#f0f8ff"
        title_fg = "#2C3E50"

        # Main frame to center the content
        manage_frame = tk.Frame(self.root, bg=frame_bg, bd=10, relief="raised")
        manage_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        tk.Label(manage_frame, text="Manage Bookstore", font=title_font, fg=title_fg, bg=frame_bg).grid(row=0, column=0,
                                                                                                        columnspan=2,
                                                                                                        pady=(0, 20))

        # Button style function
        def style_button(button):
            button.configure(font=button_font, bg=button_bg, fg=button_fg, activebackground=button_hover_bg, bd=5,
                             relief="raised", width=20, height=2)

        # Create buttons for managing the bookstore
        insert_button = tk.Button(manage_frame, text="Insert Book", command=self.insert_book_ui)
        style_button(insert_button)
        insert_button.grid(row=1, column=0, padx=10, pady=10)

        modify_button = tk.Button(manage_frame, text="Modify Book", command=self.modify_book)
        style_button(modify_button)
        modify_button.grid(row=1, column=1, padx=10, pady=10)

        delete_button = tk.Button(manage_frame, text="Delete Book", command=self.delete_book)
        style_button(delete_button)
        delete_button.grid(row=2, column=0, padx=10, pady=10)

        back_button = tk.Button(manage_frame, text="Back", command=self.open_admin_page)
        style_button(back_button)
        back_button.configure(bg="#E74C3C", activebackground="#C0392B")
        back_button.grid(row=2, column=1, padx=10, pady=10)

        # Configure column weights to ensure proper stretching
        manage_frame.columnconfigure(0, weight=1)
        manage_frame.columnconfigure(1, weight=1)

    def open_admin_inbox(self):
        # Clear the window
        self.clear_window()

        # Retrieve messages from the admin's inbox
        self.cursor.execute("SELECT msg_box FROM admin WHERE admin_id = %s", (self.admin_id,))
        messages = self.cursor.fetchone()  # Retrieve only one row

        # Create a new window for displaying inbox messages
        inbox_window = tk.Toplevel(self.root)
        inbox_window.title("Admin Inbox")

        # Frame to organize widgets
        frame = tk.Frame(inbox_window, bg="#f0f0f0")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create a listbox to display message subjects
        message_listbox = tk.Listbox(frame, width=50, height=10, font=("Helvetica", 12), bd=2, relief="sunken")
        message_listbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Function to populate message listbox
        def populate_messages():
            if messages and messages[0]:
                # Split messages by comma to separate them
                msg_parts = messages[0].split(',')
                for msg in msg_parts:
                    # Extract subject (order for book ID)
                    subject = msg.split(":")[0].strip()
                    message_listbox.insert(tk.END, subject)
                return msg_parts  # Return msg_parts
            else:
                # If there are no messages, show a message in the listbox
                message_listbox.insert(tk.END, "No messages in the inbox.")
                return None  # Return None if no messages

        # Populate the message listbox and store msg_parts
        msg_parts = populate_messages()

        if msg_parts is not None:  # Check if msg_parts is None
            # Function to display full message on selection
            def show_full_message(event):
                # Get the index of the selected item
                index = message_listbox.curselection()[0]

                # Create a new window to display the full message
                full_message_window = tk.Toplevel(inbox_window)
                full_message_window.title("Full Message")

                # Retrieve and display the full message
                full_message = msg_parts[index].strip()
                full_message_text = tk.Text(full_message_window, height=10, width=50, font=("Helvetica", 12), bd=2,
                                            relief="sunken")
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
                    # Clear and repopulate the message listbox
                    message_listbox.delete(0, tk.END)
                    populate_messages()

                # Create a button to delete the message
                delete_button = tk.Button(full_message_window, text="Delete", font=("Helvetica", 12), bg="#FF5733",
                                          fg="white", command=delete_message)
                delete_button.pack(pady=10)

            # Bind the show_full_message function to listbox selection
            message_listbox.bind("<<ListboxSelect>>", show_full_message)
        else:
            # If no messages, disable listbox selection
            message_listbox.bind("<<ListboxSelect>>", lambda event: None)

        # Create a button to view user orders
        user_orders_button = tk.Button(frame, text="User Orders", font=("Helvetica", 12), bg="#4CAF50", fg="white",
                                       command=self.open_user_orders)
        user_orders_button.grid(row=1, column=0, pady=10)

        # Create a back button to return to the admin page
        back_button = tk.Button(frame, text="Back", font=("Helvetica", 12), bg="red", fg="white",
                                command=self.open_admin_page)
        back_button.grid(row=2, column=0, pady=10)

        # Configure grid weights to ensure proper stretching
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

    def open_user_orders(self):
        # Clear the window
        self.clear_window()

        # Create a new window for displaying user orders
        user_orders_window = tk.Toplevel(self.root)
        user_orders_window.title("User Orders")

        # Add a label to indicate the purpose of the window
        tk.Label(user_orders_window, text="User Orders", font=("Helvetica", 16)).pack()

        # Execute SQL query to retrieve orders with status "AwaitingResponse"
        self.cursor.execute("SELECT * FROM purchases WHERE purchase_status = %s", ("AwaitingResponse",))
        orders = self.cursor.fetchall()

        if orders:
            # Create a frame to hold the order details
            order_frame = tk.Frame(user_orders_window)
            order_frame.pack(padx=20, pady=20)

            # Add labels to display column names
            column_names = ["Order ID", "User ID", "book_id", "ISBN", "Book Name", "category", "Quantity", "Price",
                            "Purchase Date", "Credit Card Type", "Credit Card Number", "Purchase Status"]
            for col, column_name in enumerate(column_names):
                tk.Label(order_frame, text=column_name, font=("Helvetica", 10, "bold")).grid(row=0, column=col, padx=5,
                                                                                             pady=5)

            # Create a dictionary to store the checkboxes
            checkboxes = {}
            action_buttons = {}

            # Populate the frame with order details and checkboxes
            for row, order in enumerate(orders, start=1):
                for col, value in enumerate(order):
                    if col == len(order) - 1:
                        # Create a checkbox for each row
                        checkboxes[row] = tk.BooleanVar()
                        tk.Checkbutton(order_frame, variable=checkboxes[row]).grid(row=row, column=15, padx=5, pady=5)
                    else:
                        tk.Label(order_frame, text=value).grid(row=row, column=col, padx=5, pady=5)
                # Create Accept and Decline buttons for each row
                accept_button = tk.Button(order_frame, text="Accept", bg="#4CAF50", fg="white",
                                          command=lambda idx=row: self.accept_order(orders[idx - 1][0]))
                accept_button.grid(row=row, column=len(column_names), padx=5, pady=5, sticky="nsew")
                decline_button = tk.Button(order_frame, text="Decline", bg="#FF5733", fg="white",
                                           command=lambda idx=row: self.decline_order(orders[idx - 1][0]))
                decline_button.grid(row=row, column=len(column_names) + 1, padx=5, pady=5, sticky="nsew")
            # Function to display book info for selected orders
            def show_book_info():
                for row, var in checkboxes.items():
                    if var.get():
                        # Retrieve the ISBN of the selected order
                        # order_id = orders[row - 1][0]  # Adjust index for zero-based indexing
                        isbn = orders[row - 1][3]  # Extract ISBN from selected order
                        # Retrieve book info using ISBN and display it
                        self.display_book_info(isbn)

            # Function to display user info for selected orders
            def show_user_info():
                for row, var in checkboxes.items():
                    if var.get():
                        # Retrieve the user ID of the selected order
                        # order_id = orders[row - 1][0]  # Adjust index for zero-based indexing
                        user_id = orders[row - 1][1]  # Extract User ID from selected order
                        # Retrieve user info using user ID and display it
                        self.display_user_info(user_id)

            # Add buttons for viewing book info and user info
            book_info_button = tk.Button(user_orders_window, text="Book Info", command=show_book_info)
            book_info_button.pack(side="left", padx=5, pady=10)

            user_info_button = tk.Button(user_orders_window, text="User Info", command=show_user_info)
            user_info_button.pack(side="left", padx=5, pady=10)

        else:
            # If there are no orders, display a message indicating so
            tk.Label(user_orders_window, text="No orders found.", fg="red").pack(pady=10)

        # Add a button to close the user orders window
        close_button = tk.Button(user_orders_window, text="Back", command=self.open_admin_inbox)
        close_button.pack(pady=10)

    def accept_order(self, order_id):
        # Get the admin information (admin ID and admin username) from the admin table
        admin_info_query = "SELECT admin_id, username FROM admin WHERE date_out IS NULL"
        self.cursor.execute(admin_info_query)
        admin_info = self.cursor.fetchone()

        get_order = "SELECT book_id from purchases WHERE purchase_id = %s"
        self.cursor.execute(get_order, (order_id,))
        book_id_tuple = self.cursor.fetchone()
        book_id = book_id_tuple[0]  # Extract the integer value from the tuple


        if admin_info:
            admin_id, admin_username = admin_info
            submit_date = datetime.datetime.now()

            # Update the purchase table to mark the order as accepted
            update_query = ("UPDATE purchases SET purchase_status = 'Accepted', admin_id = %s, admin_fullname = %s,"
                            " submit_date = %s WHERE purchase_id = %s")
            self.cursor.execute(update_query, (admin_id, admin_username, submit_date, order_id))
            self.mydb.commit()  # Commit the transaction
            self.refresh_database_connection()

            # Insert a record into the admin records table
            description = f"The purchase ID {order_id} was accepted by {admin_username}"
            self.cursor.execute(
                "INSERT INTO admin_records (admin_id, action_type, book_id, timestamp, description) VALUES (%s, %s, %s, %s, %s)",
                (admin_id, "Accept Order", book_id, submit_date, description))
            self.mydb.commit()  # Commit the transaction
            self.refresh_database_connection()

            # Insert a message into the user's message box
            user_id_query = "SELECT user_id FROM purchases WHERE purchase_id = %s"
            self.cursor.execute(user_id_query, (order_id,))
            user_id = self.cursor.fetchone()[0]

            # Get the book name and purchase date from the purchase table
            purchase_details_query = "SELECT book_name, purchase_date, quantity FROM purchases WHERE purchase_id = %s"
            self.cursor.execute(purchase_details_query, (order_id,))
            purchase_details = self.cursor.fetchone()

            if purchase_details:
                book_name, purchase_date, quantity = purchase_details

                # Construct the message for the user
                user_message = (f"Your order of {quantity} {book_name} purchased on {purchase_date} has been accepted. "
                                f"Thank you for your order!")

                # Insert the message into the user's message box
                insert_message_query = "UPDATE users SET inbox = CONCAT(IFNULL(inbox, ''), %s) WHERE user_id = %s"
                self.cursor.execute(insert_message_query, (user_message + '\n', user_id))
                self.mydb.commit()  # Commit the transaction
                self.refresh_database_connection()

                # Display a messagebox indicating that the order has been accepted
                messagebox.showinfo("Success", f"Order {order_id} accepted successfully.")
            else:
                # Display a messagebox with an error message if purchase details are not found
                messagebox.showerror("Error", "Failed to retrieve purchase details.")

            # Get the ISBN and quantity of the book from the purchase table
            purchase_info_query = "SELECT isbn, quantity FROM purchases WHERE purchase_id = %s"
            self.cursor.execute(purchase_info_query, (order_id,))
            purchase_info = self.cursor.fetchone()

            if purchase_info:
                isbn, quantity = purchase_info

                # Reduce the quantity of the book in the books table
                reduce_quantity_query = "UPDATE books SET present_stock = present_stock - %s WHERE isbn = %s"
                self.cursor.execute(reduce_quantity_query, (quantity, isbn))
                self.mydb.commit()  # Commit the transaction
                self.refresh_database_connection()

                # Display a messagebox indicating that the order has been accepted
                messagebox.showinfo("Success", f"Order {order_id} accepted successfully.")
            else:
                # Display a messagebox with an error message if no purchase info is found
                messagebox.showerror("Error", "Failed to retrieve purchase information.")
        else:
            # Display a messagebox with an error message if no active admin is found
            messagebox.showerror("Error", "No active admin found.")

    def decline_order(self, order_id):
        # Get the admin information (admin ID and admin username) from the admin table
        admin_info_query = "SELECT admin_id, username FROM admin WHERE date_out IS NULL"
        self.cursor.execute(admin_info_query)
        admin_info = self.cursor.fetchone()

        get_order = "SELECT book_id from purchases WHERE purchase_id = %s"
        self.cursor.execute(get_order, (order_id,))
        book_id_tuple = self.cursor.fetchone()
        book_id = book_id_tuple[0]  # Extract the integer value from the tuple

        if admin_info:
            admin_id, admin_username = admin_info
            submit_date = datetime.datetime.now()

            # Update the purchase table to mark the order as declined
            update_query = ("UPDATE purchases SET purchase_status = 'Declined', admin_id = %s, admin_fullname = %s,"
                            " submit_date = %s WHERE purchase_id = %s")
            self.cursor.execute(update_query, (admin_id, admin_username, submit_date, order_id))
            self.mydb.commit()  # Commit the transaction
            self.refresh_database_connection()

            # Insert a record into the admin records table
            description = f"The purchase ID {order_id} was declined by {admin_username}"
            self.cursor.execute(
                "INSERT INTO admin_records (admin_id, action_type, book_id, timestamp, description) VALUES"
                " (%s, %s, %s, %s, %s)",
                (admin_id, "Decline Order", book_id, submit_date, description))
            self.mydb.commit()  # Commit the transaction
            self.refresh_database_connection()

            # Get the book name and purchase date from the purchase table
            purchase_details_query = ("SELECT book_name, purchase_date , quantity , user_id "
                                      "FROM purchases WHERE purchase_id = %s")
            self.cursor.execute(purchase_details_query, (order_id,))
            purchase_details = self.cursor.fetchone()

            if purchase_details:
                book_name, purchase_date, quantity, user_id = purchase_details

                # Construct the message for the user
                user_message = (f"Your order of {quantity} {book_name} purchased on {purchase_date} has been declined."
                                f" We apologize for any inconvenience.")

                # Insert the message into the user's message box
                insert_message_query = "UPDATE users SET inbox = CONCAT(IFNULL(inbox, ''), %s) WHERE user_id = %s"
                self.cursor.execute(insert_message_query, (user_message + '\n', user_id))
                self.mydb.commit()  # Commit the transaction
                self.refresh_database_connection()

                # Display a messagebox indicating that the order has been declined
                messagebox.showinfo("Success", f"Order {order_id} declined successfully.")
            else:
                # Display a messagebox with an error message if purchase details are not found
                messagebox.showerror("Error", "Failed to retrieve purchase details.")

            # Display a messagebox indicating that the order has been declined
            messagebox.showinfo("Success", f"Order {order_id} declined successfully.")
        else:
            # Display a messagebox with an error message if no active admin is found
            messagebox.showerror("Error", "No active admin found.")

    # Add methods to display book info and user info based on their IDs
    def display_book_info(self, isbn):
        # Fetch book information from the database using ISBN
        self.cursor.execute("SELECT author, category, title, ISBN, publisher, minimum_property, present_stock, price, "
                            " publish_year , catalog_flag FROM books WHERE isbn = %s", (isbn,))
        book_info = self.cursor.fetchone()
        if book_info:
            (author, category, title, ISBN, publisher, minimum_property, present_stock,
             price, publish_year, catalog_flag) = book_info
            # Display book information
            messagebox.showinfo("Book Information",
                                f"Author: {author}\n"
                                f"Category: {category}\n"
                                f"Title: {title}\n"
                                f"ISBN: {ISBN}\n"
                                f"publisher: {publisher}\n"
                                f"minimum_property: {minimum_property}\n"
                                f"present_stock: {present_stock}\n"
                                f"Price: {price}\n"
                                f"publish_year: {publish_year}\n"
                                f"catalog_flag: {catalog_flag}\n")
        else:
            messagebox.showerror("Error", "Book information not found.")

    def display_user_info(self, user_id):
        # Fetch user information from the database using user ID
        self.cursor.execute(
            "SELECT first_name, last_name, users.city, users.state, users.zip_code, card_type, exp_date, card_number "
            "FROM users JOIN credit_cards ON users.user_id = credit_cards.user_id WHERE users.user_id = %s",
            (user_id,))
        user_info = self.cursor.fetchone()
        if user_info:
            first_name, last_name, city, state, zip_code, card_type, exp_date, card_number = user_info
            # Display user information
            messagebox.showinfo("User Information",
                                f"First Name: {first_name}\n"
                                f"Last Name: {last_name}\n"
                                f"City: {city}\n"
                                f"State: {state}\n"
                                f"zip_code: {zip_code}\n"
                                f"Card Type: {card_type}\n"
                                f"Expire date: {exp_date}\n"
                                f"Card Number: {card_number}")
        else:
            messagebox.showerror("Error", "User information not found.")

    def show_book_list(self):
        # Clear the current window
        self.clear_window()

        # Retrieve the list of books from the database
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()

        # Create a listbox to display the book titles
        book_listbox = tk.Listbox(self.root, height=20, width=80)
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
                                    f"Title: {selected_book[3]}\nAuthor: {selected_book[1]}\nCategory: "
                                    f"{selected_book[2]}\nISBN: {selected_book[4]}\nReview: {selected_book[5]}\n"
                                    f"Publisher: {selected_book[6]}\nMinimum Property: {selected_book[7]}\n"
                                    f"Present Property: {selected_book[8]}\nPrice: {selected_book[9]}\n"
                                    f"Publish Year: {selected_book[10]}")

        # Bind the double - click event to the listbox
        book_listbox.bind("<Double-Button-1>", show_book_details)

        # Create a back button to return to the main admin page
        back_button = tk.Button(self.root, text="Back", command=self.open_admin_page)
        back_button.pack(pady=5)

    def select_book_image(self, title):
        # Open file dialog to select an image file
        file_path = filedialog.askopenfilename(
            filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        if file_path:
            try:
                # Define the new file path
                new_file_path = f"book_pics/{title}.jpg"
                # Copy and rename the selected file
                shutil.copy(file_path, new_file_path)
                messagebox.showinfo("Success", f"Image successfully saved as {new_file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    def insert_book_ui(self):
        # Clear the window
        self.clear_window()

        # Define custom styles
        title_font = ("Helvetica", 16, "bold")
        label_font = ("Helvetica", 14)
        entry_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12, "bold")
        button_bg = "#3498DB"
        button_fg = "white"
        button_hover_bg = "#2980B9"
        frame_bg = "#f0f8ff"
        title_fg = "#2C3E50"

        # Main frame to center the content
        insert_frame = tk.Frame(self.root, bg=frame_bg, bd=10, relief="raised")
        insert_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Create labels and entry fields for book details
        def create_label_entry(frame, text, row):
            tk.Label(frame, text=text, font=label_font, bg=frame_bg, fg=title_fg).grid(row=row, column=0, padx=10,
                                                                                       pady=5, sticky="e")
            entry = tk.Entry(frame, font=entry_font, bd=2, relief="sunken")
            entry.grid(row=row, column=1, padx=10, pady=5, sticky="ew")
            return entry

        tk.Label(insert_frame, text="Insert Book Details", font=title_font, bg=frame_bg, fg=title_fg).grid(row=0,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=(0, 20))

        author_entry = create_label_entry(insert_frame, "Author:", 1)
        category_var = tk.StringVar()
        categories = ["Fiction", "Poetry", "Children", "Classic", "Romance", "History", "Psychology",
                      "Travel/Adventure", "Biography/Autobiography"]
        tk.Label(insert_frame, text="Category:", font=label_font, bg=frame_bg, fg=title_fg).grid(row=2, column=0,
                                                                                                 padx=10, pady=5,
                                                                                                 sticky="e")
        category_combobox = tk.OptionMenu(insert_frame, category_var, *categories)
        category_combobox.config(font=entry_font, bg="white", bd=2, relief="sunken")
        category_combobox.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        title_entry = create_label_entry(insert_frame, "Title:", 3)
        isbn_entry = create_label_entry(insert_frame, "ISBN:", 4)
        review_entry = create_label_entry(insert_frame, "Review:", 5)
        publisher_entry = create_label_entry(insert_frame, "Publisher:", 6)
        min_property_entry = create_label_entry(insert_frame, "Min. Property:", 7)
        present_property_entry = create_label_entry(insert_frame, "Present Property:", 8)
        price_entry = create_label_entry(insert_frame, "Price:", 9)
        publish_year_entry = create_label_entry(insert_frame, "Publish Year:", 10)

        # Button style function
        def style_button(button):
            button.configure(font=button_font, bg=button_bg, fg=button_fg, activebackground=button_hover_bg, bd=5,
                             relief="raised", width=20, height=2)

        # Button to submit book details
        submit_button = tk.Button(insert_frame, text="Submit", command=lambda: self.insert_book(
            author_entry.get(), category_var.get(), title_entry.get(), isbn_entry.get(), review_entry.get(),
            publisher_entry.get(), min_property_entry.get(), present_property_entry.get(), price_entry.get(),
            publish_year_entry.get()
        ))
        style_button(submit_button)
        submit_button.grid(row=11, column=0, columnspan=2, pady=(10, 5))

        # Button to select book image
        image_button = tk.Button(insert_frame, text="Select Image",
                                 command=lambda: self.select_book_image(title_entry.get()))
        style_button(image_button)
        image_button.grid(row=12, column=0, columnspan=2, pady=5)

        # Button to go back to the previous page
        back_button = tk.Button(insert_frame, text="Back", command=self.open_bookstore_management_page)
        style_button(back_button)
        back_button.configure(bg="#E74C3C", activebackground="#C0392B")
        back_button.grid(row=13, column=0, columnspan=2, pady=(5, 10))

        # Configure column weights to ensure proper stretching
        insert_frame.columnconfigure(0, weight=1)
        insert_frame.columnconfigure(1, weight=1)

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
            # Check if the ISBN is unique
            self.cursor.execute("SELECT COUNT(*) FROM books WHERE ISBN = %s", (isbn,))
            result = self.cursor.fetchone()
            if result[0] > 0:
                # ISBN already exists
                messagebox.showerror("Error", "ISBN already exists. Please enter a unique ISBN.")
                return
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
        book_listbox = tk.Listbox(self.root, height=30, width=120)
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
        # Clear the window
        self.clear_window()

        # Retrieve the list of books from the database
        self.cursor.execute("SELECT book_id, title FROM books")
        books = self.cursor.fetchall()

        # Create a frame to hold the listbox and buttons
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(padx=20, pady=20)

        # Create a label for the title
        title_label = tk.Label(frame, text="Select Book to Delete", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        # Create a listbox to display the book titles
        book_listbox = tk.Listbox(frame, font=("Helvetica", 12), bd=2, relief="sunken")
        book_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

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
        delete_catalog_button = tk.Button(frame, text="Remove from Catalog", font=("Helvetica", 12),
                                          command=delete_from_catalog, bg="#FF5733", fg="white")
        delete_catalog_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        delete_database_button = tk.Button(frame, text="Remove from Database", font=("Helvetica", 12),
                                           command=delete_from_database, bg="#FF5733", fg="white")
        delete_database_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Create a back button to return to the book store management page
        back_button = tk.Button(frame, text="Back", font=("Helvetica", 12), command=self.open_bookstore_management_page,
                                bg="#FF5733", fg="white")
        back_button.grid(row=3, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # Configure column weights to ensure proper stretching
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

    def open_manager_page(self):
        # Clear the window and create the manager page
        self.clear_window()

        # Set window title
        self.root.title("Manager Dashboard")

        # Create a frame for the manager page content
        manager_frame = tk.Frame(self.root, bg="#2c3e50")
        manager_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Add a welcome label
        welcome_label = tk.Label(manager_frame, text="Welcome Manager", fg="#ecf0f1", bg="#2c3e50",
                                 font=("Helvetica", 28, "bold"))
        welcome_label.pack(pady=20)

        # Create a frame for the buttons with a grid layout
        button_frame = tk.Frame(manager_frame, bg="#2c3e50")
        button_frame.pack(pady=20)

        # Define button properties
        button_font = ("Helvetica", 14, "bold")
        button_style = ttk.Style()
        button_style.configure("TButton", font=button_font, padding=10)
        button_style.map("TButton",
                         foreground=[('active', '#30405C')],
                         background=[('active', '#FF1111')],
                         relief=[('pressed', 'sunken'), ('!pressed', 'raised')])

        # Helper function to create buttons with hover effect
        def create_button(text, command, row, col, colspan=1):
            button = ttk.Button(button_frame, text=text, style="TButton", command=command)
            button.grid(row=row, column=col, columnspan=colspan, padx=20, pady=15, sticky="ew")

            # Add hover effect
            button.bind("<Enter>", lambda e: button.config(style="Hover.TButton"))
            button.bind("<Leave>", lambda e: button.config(style="TButton"))

        # Define hover button style
        button_style.configure("Hover.TButton", font=button_font, padding=10, background="#FF5733")

        # Add manager-specific buttons in a more interesting layout
        create_button("Inbox", self.open_manager_inbox, 0, 0, 2)
        create_button("Book Operations", self.open_book_operations, 1, 0)
        create_button("Edit Info", self.open_edit_manager_info, 1, 1)
        create_button("Reports", self.open_manager_reports, 2, 0)
        create_button("Retirement", self.open_retirement_page, 2, 1)
        create_button("Check for Inequality", self.check_for_inequality, 3, 0, 2)
        create_button("Logout", self.create_main_page, 4, 0, 2)

        # Set equal column weights to ensure even spacing
        for i in range(2):
            button_frame.columnconfigure(i, weight=1)

        # Set the window to a reasonable size
        self.root.geometry("700x500")

        # Add a method to open the retirement page
    def open_retirement_page(self):
        self.retirement.show_retire_manager_page(self.root)

    def check_for_inequality(self):
        self.clear_window()

        # Create a frame for the content with a consistent background color
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Add a title label with a larger font and some padding
        title_label = tk.Label(content_frame, text="Stock Levels Check", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # Fetch the present stock and minimum property from the books table
        self.cursor.execute("SELECT title, present_stock, minimum_property FROM books")
        books = self.cursor.fetchall()

        for title, present_stock, min_property in books:
            try:
                # Convert present_stock and min_property to integers (or floats if needed)
                present_stock = int(present_stock)
                min_property = int(min_property)

                if present_stock <= min_property * 1.1:  # If stock is near or below 10% above the minimum
                    # Display a warning label for low stock levels
                    warning_label = tk.Label(content_frame,
                                             text=f"Warning: {title} stock is low. Present: {present_stock}, Minimum: {min_property}",
                                             bg="#f0f0f0")
                    warning_label.pack(pady=5)
            except ValueError:
                # Handle the case where present_stock or min_property are not numeric
                error_label = tk.Label(content_frame,
                                       text=f"Error: Invalid stock data for {title}. Present: {present_stock}, Minimum: {min_property}",
                                       bg="#f0f0f0")
                error_label.pack(pady=5)

        # Add spacing between elements
        content_frame.pack_propagate(False)

        # Add buttons for navigation with some padding
        navigation_frame = tk.Frame(content_frame, bg="#f0f0f0")
        navigation_frame.pack(pady=20)

        go_to_modify_button = tk.Button(navigation_frame, text="Go to Modify Books", command=self.open_book_operations,
                                        bg="#3498db", fg="white", padx=10, pady=5)
        go_to_modify_button.grid(row=0, column=0, padx=10)

        back_button = tk.Button(navigation_frame, text="Back", command=self.open_manager_page,
                                bg="#2ecc71", fg="white", padx=10, pady=5)
        back_button.grid(row=0, column=1, padx=10)

    def open_manager_reports(self):
        reports_manager = ManagerReports(self.root)  # Create an instance of the Reports class
        # Call the manager_report method on the instance to open the reports window
        reports_manager.create_report_window()

    def open_edit_manager_info(self):
        # Clear the window and create the edit info page
        self.clear_window()
        self.root.title("Edit Manager Info")

        # Create a frame for the content
        content_frame = tk.Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Add a title label with larger font and padding
        title_label = tk.Label(content_frame, text="Edit Manager Info", fg="#2c3e50", bg="#f0f0f0",
                               font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        try:
            # Fetch existing manager info from the database where date_out is NULL
            self.cursor.execute("SELECT * FROM manager WHERE date_out IS NULL")
            manager_info = self.cursor.fetchone()

            if manager_info:
                manager_id = manager_info[0]  # Assuming index 0 is for manager ID

                # Define entry properties
                entry_bg = "#ecf0f1"
                entry_fg = "#2c3e50"
                entry_font = ("Helvetica", 14)

                # Populate entry fields with existing manager info
                tk.Label(content_frame, text="Full Name:", bg="#f0f0f0", font=("Helvetica", 14)).grid(row=1, column=0,
                                                                                                      padx=10, pady=5,
                                                                                                      sticky=tk.E)
                full_name_entry = tk.Entry(content_frame, bg=entry_bg, fg=entry_fg, font=entry_font)
                full_name_entry.insert(tk.END, manager_info[2])  # for full name
                full_name_entry.grid(row=1, column=1, padx=10, pady=5)

                tk.Label(content_frame, text="National ID:", bg="#f0f0f0", font=("Helvetica", 14)).grid(row=2, column=0,
                                                                                                        padx=10, pady=5,
                                                                                                        sticky=tk.E)
                national_id_entry = tk.Entry(content_frame, bg=entry_bg, fg=entry_fg, font=entry_font)
                national_id_entry.insert(tk.END, manager_info[3])  # for national ID
                national_id_entry.grid(row=2, column=1, padx=10, pady=5)

                tk.Label(content_frame, text="Password:", bg="#f0f0f0", font=("Helvetica", 14)).grid(row=3, column=0,
                                                                                                     padx=10, pady=5,
                                                                                                     sticky=tk.E)
                password_entry = tk.Entry(content_frame, bg=entry_bg, fg=entry_fg, font=entry_font, show="*")
                password_entry.insert(tk.END, manager_info[6])  # for password
                password_entry.grid(row=3, column=1, padx=10, pady=5)

                tk.Label(content_frame, text="Date of Birth:", bg="#f0f0f0", font=("Helvetica", 14)).grid(row=4,
                                                                                                          column=0,
                                                                                                          padx=10,
                                                                                                          pady=5,
                                                                                                          sticky=tk.E)
                dob_entry = tk.Entry(content_frame, bg=entry_bg, fg=entry_fg, font=entry_font)
                dob_entry.insert(tk.END, manager_info[7])  # for date of birth
                dob_entry.grid(row=4, column=1, padx=10, pady=5)

                tk.Label(content_frame, text="Phone Number:", bg="#f0f0f0", font=("Helvetica", 14)).grid(row=5,
                                                                                                         column=0,
                                                                                                         padx=10,
                                                                                                         pady=5,
                                                                                                         sticky=tk.E)
                phone_entry = tk.Entry(content_frame, bg=entry_bg, fg=entry_fg, font=entry_font)
                phone_entry.insert(tk.END, manager_info[8])  # for phone number
                phone_entry.grid(row=5, column=1, padx=10, pady=5)

                # Define button styles
                button_bg = "#3498db"
                button_fg = "white"
                button_font = ("Helvetica", 14, "bold")
                button_hover_bg = "#2980b9"

                # Helper function to create styled buttons
                def create_button(text, command, row, col, colspan=1):
                    button = tk.Button(content_frame, text=text, command=command, bg=button_bg, fg=button_fg,
                                       font=button_font)
                    button.grid(row=row, column=col, columnspan=colspan, padx=10, pady=10, sticky="ew")

                    # Add hover effect
                    button.bind("<Enter>", lambda e: button.config(bg=button_hover_bg))
                    button.bind("<Leave>", lambda e: button.config(bg=button_bg))
                    return button

                # Add button to submit changes
                create_button("Submit",
                              lambda: self.update_manager_info(full_name_entry.get(),
                                                               national_id_entry.get(),
                                                               password_entry.get(),
                                                               dob_entry.get(),
                                                               phone_entry.get(),
                                                               manager_id), 6, 0, 2)

                # Add button to go back to the manager page
                create_button("Back", self.open_manager_page, 7, 0, 2)

            else:
                messagebox.showerror("Error", "No active manager found.")
        except mysql.connector.Error as err:
            print("Error:", err)
            messagebox.showerror("Error", "Failed to fetch manager information.")

    def update_manager_info(self, full_name, national_id, password, dob, phone, manager_id):
        # Update manager info in the database
        try:
            update_query = "UPDATE manager SET full_name = %s, national_id = %s, password = %s, date_of_birth = %s, phone_number = %s WHERE manager_id = %s"
            self.cursor.execute(update_query, (full_name, national_id, password, dob, phone, manager_id))
            self.mydb.commit()
            messagebox.showinfo("Success", "Manager information updated successfully.")
        except mysql.connector.Error as err:
            print("Error:", err)
            messagebox.showerror("Error", "Failed to update manager information.")

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

                # Check if the ISBN is unique
                self.cursor.execute("SELECT COUNT(*) FROM books WHERE ISBN = %s", (isbn,))
                result = self.cursor.fetchone()
                if result[0] > 0:
                    # ISBN already exists
                    messagebox.showerror("Error", "ISBN already exists. Please enter a unique ISBN.")
                    return
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

            # Button to select book image
            image_button = tk.Button(self.root, text="Select Image",
                                     command=lambda: self.select_book_image(title_entry.get()))
            image_button.grid(row=11, columnspan=2)

            # Create back button
            self.create_back_button()

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

                        # # Track changes and store old values (this is for the test case)
                        # for field, index in field_indices.items():
                        #     old_value = old_values[field]
                        #     new_value = book_details[index]
                        #     print(f"Field: {field}, Old Value: {old_value}, New Value: {new_value}")
                        #     if field == 'price':
                        #         old_value = Decimal(old_value) if old_value else Decimal(0)
                        #         new_value = Decimal(new_value)
                        #     if old_value != new_value:
                        #         changes[field] = (old_value, new_value)
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

        # Check if the main window (self.root) exists before creating a new Toplevel window
        if self.root.winfo_exists():
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
            back_button = tk.Button(book_operations_window, text="Back", command=self.open_manager_page)
            back_button.pack(pady=10)
        else:
            messagebox.showerror("Error", "Main window has been destroyed. Cannot open book operations.")

    def open_manager_inbox(self):
        # Clear the window
        self.clear_window()

        # Refresh the database connection
        self.refresh_database_connection()

        # Retrieve the present manager ID
        self.get_present_manager_id()

        # Retrieve messages from the manager's inbox
        self.cursor.execute("SELECT msg_box FROM manager WHERE manager_id = %s", (self.manager_id,))
        inbox_messages = self.cursor.fetchone()

        # Create a listbox to display message subjects
        message_listbox = tk.Listbox(self.root, width=50, height=10)
        message_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        if inbox_messages and inbox_messages[0]:
            # Split messages by comma to separate them
            messages = inbox_messages[0].split(',')

            # Populate the listbox with message subjects (without quantity)
            for msg in messages:
                parts = msg.split(":")
                if len(parts) >= 2:
                    subject = parts[1].strip()  # Extract subject without quantity
                    message_listbox.insert(tk.END, subject)
                else:
                    message_listbox.insert(tk.END, msg)  # Insert the whole message
            # else:
            #     # If there are no messages, show a message in the listbox
            #     message_listbox.insert(tk.END, "No messages in the inbox.")

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
                            active_admin_query = "SELECT admin_id FROM admin WHERE date_out IS NULL"
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
                        insert_record_query = ("INSERT INTO manager_records (manager_id, description, orders_to_add, "
                                               "timestamp) VALUES (%s, %s, %s, NOW())")
                        description = f"Declined order: {full_message}. Additional info: {additional_info}"
                        self.cursor.execute(insert_record_query,
                                            (self.manager_id, description, f"Declined for Book ID {book_id}"))
                        self.mydb.commit()

                        # Get the ID of the active admin
                        active_admin_query = "SELECT admin_id FROM admin WHERE date_out IS NULL"
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
        # Clear the window and set the title
        self.clear_window()
        self.root.title("Sign Up Page")
        self.root.configure(bg="#f0f0f0")

        # Create a frame to hold all the elements with some padding and styling
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief="groove", padx=20, pady=20)
        frame.grid(row=0, column=0, padx=20, pady=20)

        # Title label
        self.sign_up_label = tk.Label(frame, text="Sign Up", font=("Arial", 24, "bold"), bg="#ffffff")
        self.sign_up_label.grid(row=0, columnspan=2, pady=(0, 20))

        # Create input fields with labels
        self.username_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid")
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 12), bd=2, relief="solid")
        self.first_name_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid")
        self.last_name_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid")
        self.city_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid")
        self.state_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid")
        self.zip_code_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid")
        self.credit_card_number_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid")
        self.expiry_date_entry = tk.Entry(frame, font=("Arial", 12), bd=2, relief="solid")

        fields = [
            ("Username:", self.username_entry),
            ("Password:", self.password_entry),
            ("First Name:", self.first_name_entry),
            ("Last Name:", self.last_name_entry),
            ("City:", self.city_entry),
            ("State:", self.state_entry),
            ("Zip Code:", self.zip_code_entry),
            ("Credit Card Number:", self.credit_card_number_entry),
            ("Expiry Date:", self.expiry_date_entry)
        ]

        for i, (label_text, entry_var) in enumerate(fields, start=1):
            label = tk.Label(frame, text=label_text, font=("Arial", 12), bg="#ffffff")
            label.grid(row=i, column=0, sticky="e", pady=5)
            entry_var.grid(row=i, column=1, pady=5, padx=(10, 0), ipadx=5, ipady=3)

        # Card type label and combobox
        self.card_type_label = tk.Label(frame, text="Card Type:", font=("Arial", 12), bg="#ffffff")
        self.card_type_label.grid(row=len(fields) + 1, column=0, sticky="e", pady=5)
        self.card_type_var = tk.StringVar()
        self.card_type_combobox = tk.OptionMenu(frame, self.card_type_var, "Business Credit Card", "Travel Credit Card",
                                                "Secured Credit Card")
        self.card_type_combobox.config(font=("Arial", 12), bg="#ffffff", bd=2, relief="solid")
        self.card_type_combobox.grid(row=len(fields) + 1, column=1, pady=5, padx=(10, 0), ipadx=5, ipady=3)

        # Button to submit sign-up information
        self.sign_up_button = tk.Button(frame, text="Sign Up", font=("Arial", 14, "bold"), bg="#4CAF50", fg="#ffffff",
                                        bd=0, padx=10, pady=5, command=self.validate_and_sign_up)
        self.sign_up_button.grid(row=len(fields) + 2, columnspan=2, pady=(20, 10))

        # Create back button directly within this method
        self.back_button = tk.Button(frame, text="Back", font=("Arial", 14, "bold"), bg="#f44336", fg="#ffffff", bd=0,
                                     padx=10, pady=5, command=self.create_main_page)
        self.back_button.grid(row=len(fields) + 3, columnspan=2, pady=(10, 0))

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
        # Get the search type and query
        search_query = self.search_entry.get()
        search_type = self.search_type.get().lower()  # Get selected search type

        # Clear previous search results
        self.search_results_listbox.delete(0, tk.END)

        # Define the search query based on the selected search type
        if search_type == "title":
            self.cursor.execute("SELECT title, author FROM books WHERE title LIKE %s", ('%' + search_query + '%',))
        elif search_type == "author":
            self.cursor.execute("SELECT title, author FROM books WHERE author LIKE %s", ('%' + search_query + '%',))
        elif search_type == "publisher":
            self.cursor.execute("SELECT title, author FROM books WHERE publisher LIKE %s", ('%' + search_query + '%',))

        # Fetch and display the search results
        search_results = self.cursor.fetchall()
        for result in search_results:
            title, author = result
            self.search_results_listbox.insert(tk.END, f"Title: {title}, Author: {author}")

    def add_to_cart(self):
        # Get the selected book from the search results listbox
        selected_index = self.search_results_listbox.curselection()
        if selected_index:
            selected_book = self.search_results_listbox.get(selected_index)
            # Split the selected book based on the comma separator
            book_parts = selected_book.split(", ")
            if len(book_parts) == 2:
                # Extract book title and author
                title_parts = book_parts[0].split(": ")
                author_parts = book_parts[1].split(": ")
                if len(title_parts) == 2 and len(author_parts) == 2:
                    book_title = title_parts[1]
                    author = author_parts[1]

                    # Prompt the user to enter the quantity
                    quantity = simpledialog.askinteger("Quantity",
                                                       f"How many copies of '{book_title}' by {author} would you like to add to the cart?",
                                                       parent=self.root)

                    if quantity is not None:
                        # Format the book ID to match the database query
                        book_id = f"{book_title} by {author}"
                        if book_id in self.cart:
                            # If the book is already in the cart, update the quantity
                            self.cart[book_id] += quantity
                        else:
                            # Otherwise, add a new entry to the cart
                            self.cart[book_id] = quantity

                        # Display a confirmation message with a custom style
                        confirmation_message = f"{quantity} copies of '{book_title}' by {author} added to the cart."
                        messagebox.showinfo("Success", confirmation_message)

                        # Update the cart view window
                        self.view_cart()
                else:
                    # Display an error message if the format is invalid
                    messagebox.showerror("Error", "Selected book format is invalid.")
            else:
                # Display an error message if the format is invalid
                messagebox.showerror("Error", "Selected book format is invalid.")

    def view_cart(self, parent=None):
        # Create a new window or frame within the parent window to display the cart contents
        if parent:
            cart_window = parent
        else:
            cart_window = tk.Toplevel(self.root)
            cart_window.title("Cart")
            cart_window.configure(bg="#f0f0f0")  # Set background color

        # Add a label to indicate the purpose of the window
        tk.Label(cart_window, text="Your Cart", font=("Helvetica", 16), bg="#f0f0f0").pack()

        if self.cart:
            # Display the contents of the cart
            for book_info, quantity in self.cart.items():
                # Split the book_info to extract title and author
                title, author = book_info.split(" by ")

                # Retrieve book details from the database using title and author
                self.cursor.execute("SELECT title, author, price , ISBN FROM books WHERE title = %s AND author = %s",
                                    (title, author))
                book_details = self.cursor.fetchone()
                if book_details:
                    book_title, author, price, isbn = book_details
                    # Calculate the total price for each book (price * quantity)
                    total_price = price * quantity
                    label_text = f"{book_title} by {author} (ISBN: {isbn}) - Quantity: {quantity} - Total Price: {total_price}"
                    tk.Label(cart_window, text=label_text, bg="#f0f0f0", fg="#333333", font=("Helvetica", 12)).pack()

                    # After the label is created, extract the ISBN using regular expressions
                    isbn_match = re.search(r'\(ISBN: (\d+)\)', label_text)
                    if isbn_match:
                        isbn = isbn_match.group(1)
        else:
            # If the cart is empty, display a message
            tk.Label(cart_window, text="Your cart is empty.", bg="#f0f0f0", fg="#333333", font=("Helvetica", 12)).pack()

        # Add a button to close the window if it's a separate window
        if not parent:
            close_button = tk.Button(cart_window, text="Close", command=cart_window.destroy, bg="#4CAF50", fg="white",
                                     font=("Helvetica", 12), padx=10, pady=5)
            close_button.pack(pady=10)

        # # Assuming you want to print the cart contents at a certain point in your code
        # print("Cart Contents:")
        # for book_info, quantity in self.cart.items():
        #     print(f"Book Info: {book_info}, Quantity: {quantity}")

    def proceed_to_checkout(self):
        # Create a new window for checkout
        checkout_window = tk.Toplevel(self.root)
        checkout_window.title("Checkout")
        checkout_window.configure(bg="#f0f0f0")  # Set background color

        # Add a label to indicate the purpose of the window
        tk.Label(checkout_window, text="Checkout", font=("Helvetica", 20, "bold"), bg="#f0f0f0").pack(pady=10)

        # Fetch user ID from the user table
        self.cursor.execute("SELECT user_id FROM users WHERE username = %s", (self.logged_in_username,))
        user_id = self.cursor.fetchone()[0]

        # Fetch user's first name and last name
        self.cursor.execute("SELECT first_name, last_name FROM users WHERE user_id = %s", (user_id,))
        user_info = self.cursor.fetchone()
        if user_info:
            first_name, last_name = user_info
            tk.Label(checkout_window, text=f"User: {first_name} {last_name}", font=("Helvetica", 14),
                     bg="#f0f0f0").pack()

        # Fetch credit card details from the credit card table
        self.cursor.execute("SELECT card_type, card_number FROM credit_cards WHERE user_id = %s", (user_id,))
        credit_card_info = self.cursor.fetchone()
        if credit_card_info:
            card_type, card_number = credit_card_info
            tk.Label(checkout_window, text=f"Credit Card Type: {card_type}", font=("Helvetica", 12),
                     bg="#f0f0f0").pack()
            tk.Label(checkout_window, text=f"Credit Card Number: {card_number}", font=("Helvetica", 12),
                     bg="#f0f0f0").pack()

        # Display the contents of the cart
        self.view_cart(parent=checkout_window)

        # Add a button for finalizing the purchase
        purchase_button = tk.Button(checkout_window, text="Proceed with Purchase", command=self.purchase,
                                    bg="#4CAF50", fg="white", font=("Helvetica", 14), padx=10, pady=5)
        purchase_button.pack(pady=20)

        # Add a button to close the checkout window
        close_button = tk.Button(checkout_window, text="Close", command=checkout_window.destroy,
                                 bg="#FF5733", fg="white", font=("Helvetica", 14), padx=10, pady=5)
        close_button.pack()

    def purchase(self):
        self.refresh_database_connection()

        # Check if the cart is empty
        if self.cart == {}:
            messagebox.showinfo("Empty Cart", "Your cart is empty. Please add items to your cart before proceeding.")
            return

        # Fetch user ID from the user table
        self.cursor.execute("SELECT user_id FROM users WHERE username = %s", (self.logged_in_username,))
        user_id = self.cursor.fetchone()[0]

        # Iterate over the cart items and add purchase information to the purchase table
        for book_info, quantity in self.cart.items():
            # Split the book_info to extract title and author
            title, author = book_info.split(" by ")

            # Retrieve book details from the database using title and author
            self.cursor.execute("SELECT book_id, isbn, price, category FROM books WHERE title = %s AND author = %s",
                                (title, author))
            book_data = self.cursor.fetchone()

            if book_data:
                book_id, book_isbn, book_price, book_category = book_data
                purchase_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Fetch credit card details from the credit card table
                self.cursor.execute("SELECT card_type, card_number, exp_date FROM credit_cards WHERE user_id = %s",
                                    (user_id,))
                credit_card_info = self.cursor.fetchone()

                if credit_card_info:
                    card_type, card_number, expiry_date = credit_card_info

                    # expiry_date is already a datetime.date object, compare directly
                    if expiry_date < datetime.datetime.now().date():
                        # Credit card is expired, show a messagebox with an option to update card info
                        response = messagebox.askyesno("Credit Card Expired",
                                                       "Your credit card has expired."
                                                       " Do you want to update your credit card information?")
                        if response:
                            self.edit_selected_parameter_page()
                        return  # Exit the purchase process

                    # Insert purchase information into the purchase table
                    self.cursor.execute(
                        "INSERT INTO purchases (user_id, book_id, isbn, book_name, category, quantity,"
                        " price, purchase_date, credit_card_type, credit_card_number, purchase_status) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        (user_id, book_id, book_isbn, title, book_category, quantity, book_price,
                         purchase_date, card_type, card_number,
                         'AwaitingResponse'))

                    # Commit the transaction
                    self.mydb.commit()
        # Show a messagebox confirming that the order has been submitted
        messagebox.showinfo("Order Submitted", "Your order has been submitted. Please wait for "
                                               "confirmation. You can see the confirmation message in the inbox.")

        # Clear the cart after the purchase
        self.cart = {}

        # Update the cart view window
        self.view_cart()

    def update_login_status(self):
        # Clear any existing welcome and logout buttons
        for widget_name in ['welcome_label', 'logout_button', 'msg_box_button', 'view_info_button',
                            'edit_info_button',
                            'add_to_cart_button', 'cart_button', 'checkout_button']:
            if hasattr(self, widget_name):
                getattr(self, widget_name).destroy()

        # Define custom styles
        title_font = ("Helvetica", 16, "bold")
        label_font = ("Helvetica", 14)
        entry_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12, "bold")

        # Update welcome message and display logout button if logged in
        if self.is_logged_in:
            # Clear the window
            self.clear_window()

            # Main frame to center the content
            main_frame = tk.Frame(self.root, bg="#f0f0f0")
            main_frame.place(relx=0.5, rely=0.5, anchor="center")

            # Welcome Label
            self.welcome_label = tk.Label(main_frame, text=f"Welcome, {self.logged_in_username}", font=label_font,
                                          bg="#f0f0f0", fg="green")
            self.welcome_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

            # Logout Button
            self.logout_button = tk.Button(main_frame, text="Logout", font=button_font, bg="#FF5733", fg="white",
                                           command=self.logout)
            self.logout_button.grid(row=0, column=2, padx=(10, 0))

            # View and Edit Info Buttons
            self.view_info_button = tk.Button(main_frame, text="View Info", font=button_font, bg="#2196F3", fg="white",
                                              command=self.view_user_info)
            self.view_info_button.grid(row=1, column=0, padx=(0, 10), pady=10, sticky="ew")
            self.edit_info_button = tk.Button(main_frame, text="Edit Info", font=button_font, bg="#2196F3", fg="white",
                                              command=self.edit_selected_parameter_page)
            self.edit_info_button.grid(row=1, column=1, padx=(10, 0), pady=10, sticky="ew")

            # Message Box Button
            self.msg_box_button = tk.Button(main_frame, text="Message Box", font=button_font, bg="#4CAF50", fg="white",
                                            command=self.show_message_box)
            self.msg_box_button.grid(row=1, column=2, pady=10, sticky="ew")

            # Search Label
            tk.Label(main_frame, text="Search:", font=label_font, bg="#f0f0f0").grid(row=2, column=0, pady=10,
                                                                                     sticky="e")

            # Entry for search text
            self.search_entry = tk.Entry(main_frame, font=entry_font, bd=2, relief="sunken")
            self.search_entry.grid(row=2, column=1, pady=10, sticky="ew")

            # Combobox for search type
            self.search_type = ttk.Combobox(main_frame, values=["Title", "Author", "Publisher"], font=entry_font)
            self.search_type.grid(row=2, column=2, pady=10, sticky="ew")
            self.search_type.current(0)  # Set default value

            # Search Button
            tk.Button(main_frame, text="Search", font=button_font, bg="#4CAF50", fg="white",
                      command=self.search_books).grid(row=2, column=3, padx=(10, 0), pady=10, sticky="ew")

            # Search Results Listbox
            self.search_results_listbox = tk.Listbox(main_frame, height=10, width=100, font=entry_font, bd=2,
                                                     relief="sunken")
            self.search_results_listbox.grid(row=3, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

            # Add to Cart Button
            self.add_to_cart_button = tk.Button(main_frame, text="Add to Cart", font=button_font, bg="#9C27B0",
                                                fg="white", command=self.add_to_cart)
            self.add_to_cart_button.grid(row=4, column=0, pady=10, sticky="ew")

            # View Cart Button
            self.cart_button = tk.Button(main_frame, text="See the Cart", font=button_font, bg="#9C27B0", fg="white",
                                         command=self.view_cart)
            self.cart_button.grid(row=4, column=1, pady=10, sticky="ew")

            # Proceed to Checkout Button
            self.checkout_button = tk.Button(main_frame, text="Proceed to Checkout", font=button_font, bg="#9C27B0",
                                             fg="white", command=self.proceed_to_checkout)
            self.checkout_button.grid(row=4, column=2, pady=10, sticky="ew")

            # Book Info Button
            tk.Button(main_frame, text="Book Info", font=button_font, bg="#4CAF50", fg="white",
                      command=self.show_book_info).grid(row=4, column=3, padx=(10, 0), pady=10, sticky="ew")

            # Get random books from the recommendation_system.py
            recommendations = self.recommendation_system.get_recommendations(self.logged_in_username, 3)

            # Display books in the listbox
            for book in recommendations:
                # Extract book information
                book_id, category = book

                # Fetch additional details of the book using the book_id
                self.cursor.execute("SELECT title, author FROM books WHERE book_id = %s", (book_id,))
                book_info = self.cursor.fetchone()
                if book_info:
                    title, author = book_info
                    book_info_str = f"Title: {title}, Author: {author}"
                    self.search_results_listbox.insert(tk.END, book_info_str)
                else:
                    # Handle case where book information is not found
                    print(f"Book with ID {book_id} not found in database.")
            self.inbox_alert()
        else:
            self.welcome_label = tk.Label(self.root, text="Not logged in", font=label_font, fg="red", bg="#f0f0f0")
            self.welcome_label.grid(row=0, column=0, columnspan=2, pady=10)

    def show_book_info(self):
        selected_index = self.search_results_listbox.curselection()
        if selected_index:
            selected_book = self.search_results_listbox.get(selected_index)
            book_title, book_author = self.parse_book_info(selected_book)
            self.cursor.execute("SELECT * FROM books WHERE title = %s AND author = %s", (book_title, book_author))
            book_info = self.cursor.fetchone()
            if book_info:
                self.book_info(book_info)
            else:
                messagebox.showerror("Error", "Book information not found.")
        else:
            messagebox.showwarning("No selection", "Please select a book from the list.")

    def parse_book_info(self, book_info_str):
        # Extract book title and author from the book info string
        parts = book_info_str.split(", Author: ")
        title = parts[0].replace("Title: ", "")
        author = parts[1]
        return title, author

    def book_info(self, book_info):
        # Create a new window to display the book info
        info_window = tk.Toplevel(self.root)
        info_window.title("Book Info")
        info_window.configure(bg="#f0f0f0")

        # Create a frame with padding and background color
        frame = tk.Frame(info_window, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        # Create a stylish card-like design with a gradient background and rounded corners
        card_frame = tk.Frame(frame, bg="#FFFFFF", bd=2, relief="solid", padx=20, pady=20)
        card_frame.pack(expand=True, fill="both")

        # Display text information with improved font and styling
        title_label = tk.Label(card_frame, text=f"Title: {book_info[3]}", font=("Arial", 18, "bold"), bg="#FFFFFF",
                               fg="#333333")
        title_label.pack(anchor="w", pady=(0, 10))

        author_label = tk.Label(card_frame, text=f"Author: {book_info[1]}", font=("Arial", 14), bg="#FFFFFF",
                                fg="#666666")
        author_label.pack(anchor="w", pady=(0, 5))

        publisher_label = tk.Label(card_frame, text=f"Publisher: {book_info[6]}", font=("Arial", 14), bg="#FFFFFF",
                                   fg="#666666")
        publisher_label.pack(anchor="w", pady=(0, 5))

        category_label = tk.Label(card_frame, text=f"Category: {book_info[2]}", font=("Arial", 14), bg="#FFFFFF",
                                  fg="#666666")
        category_label.pack(anchor="w", pady=(0, 5))

        review_label = tk.Label(card_frame, text=f"Review: {book_info[5]}", font=("Arial", 14), bg="#FFFFFF",
                                fg="#666666")
        review_label.pack(anchor="w", pady=(0, 10))

        # Create a frame for the book picture with a border and shadow effect
        picture_frame = tk.Frame(card_frame, bg="#FFFFFF", bd=2, relief="solid")
        picture_frame.pack(pady=20)

        # Check if an image file exists for the book
        image_file = f"book_pics/{book_info[3]}.jpg"
        if os.path.exists(image_file):
            # Open the JPEG image file using PIL
            image = Image.open(image_file)

            # Resize the image to fit the frame
            image = image.resize((220, 300), Image.LANCZOS)

            # Convert the image to a Tkinter-compatible format
            tk_image = ImageTk.PhotoImage(image)

            # Create a Tkinter label to display the image in the frame
            image_label = tk.Label(picture_frame, image=tk_image, bg="#FFFFFF")
            image_label.image = tk_image  # Keep a reference to avoid garbage collection
            image_label.pack(pady=10)

        else:
            # Display a message if no image file is found
            no_image_label = tk.Label(picture_frame, text="No image available", font=("Arial", 14), bg="#FFFFFF",
                                      fg="#666666")
            no_image_label.pack(pady=10)

        # Run the Tkinter event loop for the info_window
        info_window.mainloop()

    def inbox_alert(self):
        # Get the user's inbox content
        self.cursor.execute("SELECT inbox FROM users WHERE user_id = %s", (self.logged_in_id,))
        inbox_content = self.cursor.fetchone()

        if inbox_content is not None:
            inbox_content = inbox_content[0]  # Extract the inbox content
            if inbox_content and len(inbox_content) > 250:
                # Display an alert message
                messagebox.showwarning("Inbox Alert",
                                       "We highly recommend to empty the inbox or it will be deleted.")

                # Create a new window for inbox management
                inbox_window = tk.Toplevel(self.root)
                inbox_window.title("Inbox Management")

                # Add buttons to manage the inbox
                tk.Button(inbox_window, text="Show Inbox", command=self.show_message_box).pack()
                tk.Button(inbox_window, text="Delete Inbox", command=self.delete_inbox).pack()
                tk.Button(inbox_window, text="Back", command=inbox_window.destroy).pack()
            if inbox_content and len(inbox_content) > 380:
                self.delete_inbox()
        else:
            # Handle case where no inbox content is found
            messagebox.showinfo("Message Box", "No messages in the message box.")

    def delete_inbox(self):
        # Clear the inbox content
        self.cursor.execute("UPDATE users SET inbox = NULL WHERE user_id = %s", (self.logged_in_id,))
        self.mydb.commit()  # Commit the transaction
        messagebox.showinfo("Success", "Inbox deleted successfully.")

    def show_message_box(self):
        # Remember the current page
        self.previous_page = self.root.winfo_children()

        # Clear the window
        self.clear_window()

        # Get message box content from the database
        self.cursor.execute("SELECT inbox FROM users WHERE username = %s", (self.logged_in_username,))
        message_box_content = self.cursor.fetchone()

        # Main frame for centering content
        main_frame = tk.Frame(self.root, bg="#ffffff")
        main_frame.pack(expand=True, fill="both")

        # Title Label
        title_label = tk.Label(main_frame, text="Message Box", font=("Helvetica", 20, "bold"), bg="#ffffff",
                               fg="#2980b9")
        title_label.pack(pady=20)

        # Frame for displaying message box content
        message_frame = tk.Frame(main_frame, bg="#ffffff")
        message_frame.pack()

        # Display message box content if available
        if message_box_content:
            messages = message_box_content[0].split(",") if message_box_content[0] else []  # Split messages by comma
            for message in messages:
                tk.Label(message_frame, text=message.strip(), font=("Helvetica", 12), bg="#ffffff").pack(anchor="w",
                                                                                                         padx=20,
                                                                                                         pady=5)
        else:
            tk.Label(message_frame, text="No messages in the message box.", font=("Helvetica", 12), bg="#ffffff").pack(
                pady=10)

        # Frame for buttons
        button_frame = tk.Frame(main_frame, bg="#ffffff")
        button_frame.pack(pady=20)

        # Button to delete all messages
        delete_button = tk.Button(button_frame, text="Delete All Messages",
                                  command=self.delete_all_inbox_messages_of_user,
                                  font=("Helvetica", 12, "bold"), bg="#e74c3c", fg="#ffffff")
        delete_button.pack(side="left", padx=10)

        # Button to go back to the main page
        back_button = tk.Button(button_frame, text="Back", command=self.create_main_page,
                                font=("Helvetica", 12, "bold"), bg="#2980b9", fg="#ffffff")
        back_button.pack(side="right", padx=10)

    def delete_all_inbox_messages_of_user(self):
        # Delete all messages from the user's inbox in the database
        self.cursor.execute("UPDATE users SET inbox = Null WHERE username = %s", (self.logged_in_username,))
        self.mydb.commit()

        # Show confirmation message
        messagebox.showinfo("Message Box", "All messages have been deleted.")

        # Refresh the message box view
        self.show_message_box()

    def view_user_info(self):
        # Retrieve user information from the users table
        self.cursor.execute(
            "SELECT username, first_name, last_name, city, state, zip_code FROM users WHERE username = %s",
            (self.logged_in_username,))
        user_info = self.cursor.fetchone()

        if user_info:
            # Extract user details
            username, first_name, last_name, city, state, zip_code = user_info

            # Retrieve card information from the credit_cards table
            self.cursor.execute("SELECT card_number, exp_date, card_type FROM credit_cards WHERE user_id = %s",
                                (self.logged_in_id,))
            card_info = self.cursor.fetchone()

            if card_info:
                card_number, exp_date, card_type = card_info
            else:
                card_number, exp_date, card_type = "N/A", "N/A", "N/A"

            # Create a new top-level window for displaying user information
            info_window = Toplevel(self.root)
            info_window.title("User Information")
            info_window.geometry("470x550")
            info_window.configure(bg="#2c3e50")

            # Define fonts
            title_font = ("Helvetica", 18, "bold")
            label_font = ("Helvetica", 14)
            value_font = ("Helvetica", 14, "italic")

            # Title Label
            title_label = tk.Label(info_window, text="User Information", font=title_font, bg="#2c3e50", fg="#ecf0f1")
            title_label.pack(pady=20)

            # User Info Frame
            info_frame = tk.Frame(info_window, bg="#34495e", bd=2, relief="groove")
            info_frame.pack(pady=10, padx=20, fill="both", expand=True)

            # Function to create labeled info rows
            def create_info_row(frame, label_text, value_text, row):
                tk.Label(frame, text=label_text, font=label_font, bg="#34495e", fg="#ecf0f1").grid(row=row, column=0,
                                                                                                   sticky="w", padx=10,
                                                                                                   pady=5)
                tk.Label(frame, text=value_text, font=value_font, bg="#34495e", fg="#bdc3c7").grid(row=row, column=1,
                                                                                                   sticky="w", padx=10,
                                                                                                   pady=5)

            # Display user information
            create_info_row(info_frame, "Username:", username, 0)
            create_info_row(info_frame, "First Name:", first_name, 1)
            create_info_row(info_frame, "Last Name:", last_name, 2)
            create_info_row(info_frame, "City:", city, 3)
            create_info_row(info_frame, "State:", state, 4)
            create_info_row(info_frame, "Zip Code:", zip_code, 5)
            create_info_row(info_frame, "Card Number:", card_number, 6)
            create_info_row(info_frame, "Exp Date:", exp_date, 7)
            create_info_row(info_frame, "Card Type:", card_type, 8)

            # Close Button
            close_button = tk.Button(info_window, text="Close", command=info_window.destroy, font=label_font,
                                     bg="#e74c3c", fg="white")
            close_button.pack(pady=20)

        else:
            messagebox.showerror("Error", "Failed to retrieve user information.")

    # def edit_user_info(self):
    #     # Clear the window
    #     self.clear_window()
    #
    #     # Create the edit page
    #     self.edit_selected_parameter_page()

    def edit_selected_parameter_page(self):
        self.clear_window()

        # Define fonts and colors
        title_font = ("Helvetica", 20, "bold")
        label_font = ("Helvetica", 14)
        button_font = ("Helvetica", 12, "bold")

        bg_color = "#ffffff"  # White background
        fg_color = "#2c3e50"  # Dark grey text
        button_bg = "#1abc9c"  # Teal button background
        button_fg = "#ffffff"  # White button text
        frame_bg = "#ecf0f1"  # Light grey frame background
        dropdown_bg = "#bdc3c7"  # Light grey dropdown background
        dropdown_fg = "#2c3e50"  # Dark grey dropdown text
        title_fg = "#2980b9"  # Blue title text

        # Main frame to center the content
        main_frame = tk.Frame(self.root, bg=bg_color, padx=20, pady=20)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        title_label = tk.Label(main_frame, text="Edit User Information", font=title_font, bg=bg_color, fg=title_fg)
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # List of parameters
        parameters = ["Password", "First Name", "Last Name", "City", "State", "Zip Code", "Card Number", "Exp Date",
                      "Card Type"]

        # Frame for parameter selection
        selection_frame = tk.Frame(main_frame, bg=frame_bg, padx=10, pady=10, relief=tk.RIDGE, bd=2)
        selection_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")

        # Prompt user to select a parameter to edit
        selected_parameter = tk.StringVar(value=parameters[0])  # Default selection
        parameter_label = tk.Label(selection_frame, text="Select parameter to edit:", font=label_font, bg=frame_bg,
                                   fg=fg_color)
        parameter_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        parameter_dropdown = tk.OptionMenu(selection_frame, selected_parameter, *parameters)
        parameter_dropdown.config(font=label_font, bg=dropdown_bg, fg=dropdown_fg, activebackground=dropdown_bg,
                                  activeforeground=dropdown_fg)
        parameter_dropdown.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # Frame for confirm button
        button_frame = tk.Frame(main_frame, bg=bg_color)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)

        # Button to confirm parameter selection
        confirm_button = tk.Button(button_frame, text="Confirm", font=button_font, bg=button_bg, fg=button_fg,
                                   command=lambda: self.edit_selected_parameter(selected_parameter.get()))
        confirm_button.pack(side=tk.LEFT, padx=10)

        # Create back button
        back_button = tk.Button(button_frame, text="Back", command=self.create_main_page,
                                font=button_font, bg="#e74c3c", fg=button_fg)
        back_button.pack(side=tk.LEFT, padx=10)

        # Center the widgets in the grid
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def edit_selected_parameter(self, parameter):
        # Clear the window
        self.clear_window()

        # Define fonts and colors
        title_font = ("Helvetica", 20, "bold")
        label_font = ("Helvetica", 14)
        entry_font = ("Helvetica", 12)
        button_font = ("Helvetica", 12, "bold")

        bg_color = "#ffffff"  # White background
        fg_color = "#2c3e50"  # Dark grey text
        button_bg = "#1abc9c"  # Teal button background
        button_fg = "#ffffff"  # White button text
        frame_bg = "#ecf0f1"  # Light grey frame background
        title_fg = "#2980b9"  # Blue title text

        # Main frame to center the content
        main_frame = tk.Frame(self.root, bg=bg_color)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title Label
        title_label = tk.Label(main_frame, text=f"Edit {parameter}", font=title_font, bg=bg_color, fg=title_fg)
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Frame for input fields
        input_frame = tk.Frame(main_frame, bg=frame_bg)
        input_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=20)

        # Create labels and entry fields for editing the selected parameter
        parameter_label = tk.Label(input_frame, text=f"New {parameter}:", font=label_font, bg=frame_bg, fg=fg_color)
        parameter_label.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        new_value_entry = tk.Entry(input_frame, font=entry_font, bd=2, relief="sunken")
        new_value_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # Button to confirm the new value
        confirm_button = tk.Button(main_frame, text="Confirm", font=button_font, bg=button_bg, fg=button_fg,
                                   command=lambda: self.update_parameter(parameter, new_value_entry.get()))
        confirm_button.grid(row=2, column=0, columnspan=2, pady=20)

        # Create back button
        back_button = tk.Button(main_frame, text="Back", command=self.edit_selected_parameter_page,
                                font=button_font, bg="#e74c3c", fg=button_fg)
        back_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Center the widgets in the grid
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)

    def update_parameter(self, parameter, new_value):
        try:
            # Update the parameter in the database
            if parameter.lower() in ["password", "first name", "last name", "city", "state", "zip code"]:
                # Update user information
                self.cursor.execute(f"UPDATE users SET {parameter.lower().replace(' ', '_')} = %s WHERE username = %s",
                                    (new_value, self.logged_in_username))
            elif parameter.lower() in ["card number", "exp date", "card type"]:
                # Update credit card information
                self.cursor.execute(
                    f"UPDATE credit_cards SET {parameter.lower().replace(' ', '_')} = %s WHERE user_id = %s",
                    (new_value, self.logged_in_id))

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
