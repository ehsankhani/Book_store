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

        tk.Label(root, text="Full Name:").grid(row=0, column=0)
        self.fullname_entry = tk.Entry(root)
        self.fullname_entry.grid(row=0, column=1)

        tk.Label(root, text="National ID:").grid(row=1, column=0)
        self.national_id_entry = tk.Entry(root)
        self.national_id_entry.grid(row=1, column=1)

        tk.Label(root, text="Password:").grid(row=2, column=0)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=2, column=1)

        tk.Label(root, text="Date of Birth:").grid(row=3, column=0)
        self.dob_entry = tk.Entry(root)
        self.dob_entry.grid(row=3, column=1)

        tk.Label(root, text="Phone Number:").grid(row=4, column=0)
        self.phone_entry = tk.Entry(root)
        self.phone_entry.grid(row=4, column=1)

        tk.Button(root, text="Retire and Add New Manager", command=lambda: self.retire_and_add_manager(root)).grid(
            row=5, column=0, columnspan=2)
        # Button for Back
        tk.Button(root, text="Back", command=self.bookstore_app.open_manager_page).grid(row=5, column=2)

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
