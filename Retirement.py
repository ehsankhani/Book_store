import mysql.connector
from DataBase_Connection import get_database_connection
import tkinter as tk
from tkinter import messagebox
import datetime
class Retirement:
    def __init__(self, bookstore_app):
        # self.manager_id = None
        # Get the database connection
        self.mydb, self.cursor = get_database_connection()
        self.bookstore_app = bookstore_app

    def show_retire_manager_page(self, root):
        self.clear_window(root)
        root.title("Retire Manager")

        # Create a main frame to center the content
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a subframe for the form content
        content_frame = tk.Frame(main_frame, bg="#f0f0f0", padx=20, pady=20)
        content_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Add a title label with larger font and padding
        title_label = tk.Label(content_frame, text="Retire Manager and Add New Manager", fg="#2c3e50", bg="#f0f0f0",
                               font=("Helvetica", 20, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        # Define entry properties
        entry_bg = "#ecf0f1"
        entry_fg = "#2c3e50"
        entry_font = ("Helvetica", 14)

        # Create labels and entries with consistent styling
        fields = [
            ("Full Name:", "fullname_entry"),
            ("National ID:", "national_id_entry"),
            ("Password:", "password_entry", True),
            ("Date of Birth:", "dob_entry"),
            ("Phone Number:", "phone_entry")
        ]

        for i, field in enumerate(fields, start=1):
            label_text = field[0]
            entry_var_name = field[1]
            show_asterisk = field[2] if len(field) > 2 else False

            tk.Label(content_frame, text=label_text, bg="#f0f0f0", font=("Helvetica", 14)).grid(row=i, column=0,
                                                                                                padx=10, pady=5,
                                                                                                sticky=tk.E)
            entry_var = tk.Entry(content_frame, bg=entry_bg, fg=entry_fg, font=entry_font,
                                 show="*" if show_asterisk else None)
            entry_var.grid(row=i, column=1, padx=10, pady=5)
            setattr(self, entry_var_name, entry_var)

        # Define button styles
        button_bg = "#3498db"
        button_fg = "white"
        button_font = ("Helvetica", 14, "bold")
        button_hover_bg = "#2980b9"

        # Helper function to create styled buttons
        def create_button(text, command, row, col, colspan=1):
            button = tk.Button(content_frame, text=text, command=command, bg=button_bg, fg=button_fg, font=button_font)
            button.grid(row=row, column=col, columnspan=colspan, padx=10, pady=10, sticky="ew")

            # Add hover effect
            button.bind("<Enter>", lambda e: button.config(bg=button_hover_bg))
            button.bind("<Leave>", lambda e: button.config(bg=button_bg))
            return button

        # Add buttons for actions
        create_button("Retire and Add New Manager", lambda: self.retire_and_add_manager(root), len(fields) + 1, 0, 2)
        create_button("Back", self.bookstore_app.open_manager_page, len(fields) + 2, 0, 2)

    def retire_and_add_manager(self, root):
        fullname = self.fullname_entry.get()
        national_id = self.national_id_entry.get()
        password = self.password_entry.get()
        date_of_birth = self.dob_entry.get()
        phone_number = self.phone_entry.get()

        # manager_id = self.manager_id     # Implement this method to get the logged-in manager's ID

        self.retire_manager(fullname, national_id, password, date_of_birth, phone_number)
    def retire_manager(self, fullname, national_id, password, date_of_birth, phone_number):
        try:
            # Check if the manager exists and is active
            self.cursor.execute("SELECT * FROM manager WHERE date_out IS NULL")
            manager_id = self.cursor.fetchone()[0]
            if not manager_id:
                messagebox.showerror("Error", "Active manager not found.")
                return

            # Set the date_out for the current manager
            current_time = datetime.datetime.now()
            self.cursor.execute("UPDATE manager SET date_out = %s WHERE manager_id = %s", (current_time, manager_id))
            self.mydb.commit()

            # Insert the new manager
            self.cursor.execute("""
                INSERT INTO manager (msg_box,full_name, national_id, date_in, date_out, password, date_of_birth, phone_number)
                VALUES (NULL, %s, %s, %s, NULL, %s, %s, %s)
            """, (fullname, national_id, current_time, password, date_of_birth, phone_number))

            self.mydb.commit()

            messagebox.showinfo("Success", "Manager retired and new manager added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error retiring manager and adding new manager: {err}")

    def clear_window(self, root):
        for widget in root.winfo_children():
            widget.destroy()

    def show_retire_admin_page(self, root):
        self.clear_window(root)

        # Create a frame to hold the widgets
        frame = tk.Frame(root, bg="#E6E6FA", padx=20, pady=10)
        frame.pack(expand=True)

        # Labels and entry fields
        tk.Label(frame, text="User Name:", font=("Arial", 12), bg="#E6E6FA").grid(row=0, column=0, pady=5, sticky="e")
        self.username_entry = tk.Entry(frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame, text="Full Name:", font=("Arial", 12), bg="#E6E6FA").grid(row=1, column=0, pady=5, sticky="e")
        self.fullname_entry = tk.Entry(frame, font=("Arial", 12))
        self.fullname_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(frame, text="National ID:", font=("Arial", 12), bg="#E6E6FA").grid(row=2, column=0, pady=5, sticky="e")
        self.national_id_entry = tk.Entry(frame, font=("Arial", 12))
        self.national_id_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(frame, text="Password:", font=("Arial", 12), bg="#E6E6FA").grid(row=3, column=0, pady=5, sticky="e")
        self.password_entry = tk.Entry(frame, show="*", font=("Arial", 12))
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(frame, text="Date of Birth:", font=("Arial", 12), bg="#E6E6FA").grid(row=4, column=0, pady=5,
                                                                                      sticky="e")
        self.dob_entry = tk.Entry(frame, font=("Arial", 12))
        self.dob_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(frame, text="Phone Number:", font=("Arial", 12), bg="#E6E6FA").grid(row=5, column=0, pady=5,
                                                                                     sticky="e")
        self.phone_entry = tk.Entry(frame, font=("Arial", 12))
        self.phone_entry.grid(row=5, column=1, padx=10, pady=5)

        # Button for retiring and adding new admin
        retire_button = tk.Button(frame, text="Retire and Add New Admin", font=("Arial", 12), bg="#9370DB", fg="white",
                                  command=lambda: self.retire_and_add_admin(root))
        retire_button.grid(row=6, column=0, columnspan=4, padx=5, pady=5, sticky="ew")

        # Back button
        back_button = tk.Button(frame, text="Back", font=("Arial", 12), bg="#FF5733", fg="white",
                                command=self.bookstore_app.open_admin_page, width=20)
        back_button.grid(row=7, column=0, columnspan=2, padx=5, pady=0, sticky="ew")

        # Center the frame
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    def retire_and_add_admin(self, root):
        user_name = self.username_entry.get()
        fullname = self.fullname_entry.get()
        password = self.password_entry.get()
        national_id = self.national_id_entry.get()
        phone_number = self.phone_entry.get()
        date_of_birth = self.dob_entry.get()

        self.retire_admin(user_name, fullname, national_id, password, date_of_birth, phone_number)

    def retire_admin(self, username, fullname, national_id, password, date_of_birth, phone_number):
        try:
            # Check if the admin exists and is active
            self.cursor.execute("SELECT * FROM admin WHERE date_out IS NULL")
            admin_id = self.cursor.fetchone()[0]
            if not admin_id:
                messagebox.showerror("Error", "Active admin not found.r")
                return
            current_time = datetime.datetime.now()
            # Insert the new admin
            self.cursor.execute("""
                INSERT INTO admin (username, full_name, password,msg_box, 
                national_id, phone_number, date_of_birth, date_in, date_out)
                VALUES (%s, %s, %s,NULL, %s, %s, %s, %s, NULL)
            """, (username, fullname, password, national_id, phone_number, date_of_birth, current_time))
            self.mydb.commit()

            # Set the date_out for the current admin

            self.cursor.execute("UPDATE admin SET date_out = %s WHERE admin_id = %s", (current_time, admin_id))
            self.mydb.commit()

            messagebox.showinfo("Success", "Admin retired and new admin added successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error retiring admin and adding new admin: {err}")
