import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from DataBase_Connection import get_database_connection


class ManagerReports:
    def __init__(self, parent):
        self.parent = parent
        # # Get the database connection
        # self.mydb, self.cursor = get_database_connection()

    def create_report_window(self):
        # Create a new window for reports
        self.reports_window = tk.Toplevel(self.parent)
        self.reports_window.title("Manager Reports")

        # Add GUI elements for reports
        tk.Label(self.reports_window, text="Reports", font=("Helvetica", 16)).pack(pady=10)

        # Dropdown menu for selecting report type
        report_types = ["Report 1", "Report 2", "Report 3", "Report 4", "Report 5", "Report 6"]
        self.selected_report = tk.StringVar(self.reports_window)
        self.selected_report.set(report_types[0])  # Default selection
        report_dropdown = ttk.Combobox(self.reports_window, textvariable=self.selected_report, values=report_types, state="readonly")
        report_dropdown.pack(pady=5)

        # Button to generate selected report
        generate_button = tk.Button(self.reports_window, text="Generate Report", command=self.generate_report)
        generate_button.pack(pady=5)

        # Button for generating custom reports
        custom_report_button = tk.Button(self.reports_window, text="Custom Report", command=self.generate_custom_report)
        custom_report_button.pack(pady=5)

    def generate_report(self):
        report_type = self.selected_report.get()
        if report_type == "Report 1":
            self.generate_report_1()
        elif report_type == "Report 2":
            self.generate_report_2()
        elif report_type == "Report 3":
            self.generate_report_3()
        elif report_type == "Report 4":
            self.generate_report_4()
        elif report_type == "Report 5":
            self.generate_report_5()
        elif report_type == "Report 6":
            self.generate_report_6()

    def generate_custom_report(self):
        # Implement functionality to generate custom reports
        pass

    def generate_report_1(self):
        try:
            mydb, cursor = get_database_connection()

            # Fetch distinct categories from purchases table
            cursor.execute("SELECT DISTINCT category FROM purchases WHERE purchase_status = 'Accepted';")
            categories = [row[0] for row in cursor.fetchall()]

            if not categories:
                messagebox.showwarning("No Data", "There are no records in the purchases table.")
                return

            # Prompt manager to choose category
            category_var = tk.StringVar()
            category_dropdown = ttk.Combobox(self.reports_window, textvariable=category_var, values=categories,
                                             state="readonly")
            category_dropdown.pack(pady=5)
            category_dropdown.current(0)  # Default selection

            # Fetch distinct months from purchases table
            cursor.execute("SELECT DISTINCT MONTH(submit_date) FROM purchases WHERE purchase_status = 'Accepted';")
            months = [row[0] for row in cursor.fetchall()]

            if not months:
                messagebox.showwarning("No Data", "There are no records with valid months in the purchases table.")
                return

            # Prompt manager to choose month
            month_var = tk.StringVar()
            month_dropdown = ttk.Combobox(self.reports_window, textvariable=month_var, values=months, state="readonly")
            month_dropdown.pack(pady=5)
            month_dropdown.current(0)  # Default selection

            # Function to calculate sum of books sold
            def calculate_sum():
                try:
                    # Re-establish the database connection
                    mydb, cursor = get_database_connection()

                    selected_category = category_var.get()
                    selected_month = int(month_var.get())

                    # Calculate sum of quantity and price for selected category and month
                    cursor.execute(
                        "SELECT SUM(quantity), SUM(price) FROM purchases WHERE category=%s AND MONTH(submit_date)=%s",
                        (selected_category, selected_month))

                    # Fetch the result
                    result = cursor.fetchone()
                    total_quantity = result[0]
                    total_price = result[1]

                    # Display the result
                    messagebox.showinfo("Report Result",
                                        f"Total quantity of {selected_category} sold in month {selected_month}: {total_quantity}\nTotal price: {total_price}")

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Failed to fetch data from the database: {err}")

            # Button to calculate sum
            calculate_button = tk.Button(self.reports_window, text="Calculate Sum", command=calculate_sum)
            calculate_button.pack(pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {err}")

    def generate_report_2(self):
        try:
            # Function to calculate sum of present stock for the selected category
            def calculate_sum():
                try:
                    # Establish the database connection
                    mydb, cursor = get_database_connection()

                    category = selected_category.get()

                    # Calculate sum of present stock for the selected category
                    cursor.execute("SELECT SUM(present_stock) FROM books WHERE category=%s", (category,))
                    total_present_stock = cursor.fetchone()[0]

                    # Display the result
                    messagebox.showinfo("Report Result",
                                        f"Total present stock for category {category}: {total_present_stock}")

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Failed to fetch data from the database: {err}")
            # Re-establish the database connection
            mydb, cursor = get_database_connection()

            # Fetch all possible categories from the books table
            cursor.execute("SELECT DISTINCT category FROM books")
            categories = [row[0] for row in cursor.fetchall()]

            if not categories:
                messagebox.showwarning("No Data", "There are no records in the books table.")
                return

            # Create a new window for selecting category
            category_window = tk.Toplevel(self.reports_window)
            category_window.title("Select Category")

            # Prompt manager to choose category
            selected_category = tk.StringVar()
            category_label = tk.Label(category_window, text="Select a category:")
            category_label.pack(pady=5)
            category_dropdown = ttk.Combobox(category_window, textvariable=selected_category, values=categories,
                                             state="readonly")
            category_dropdown.pack(pady=5)
            category_dropdown.current(0)  # Default selection

            # Button to calculate sum
            calculate_button = tk.Button(category_window, text="Calculate Sum", command=calculate_sum)
            calculate_button.pack(pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch data from the database: {err}")

    def generate_report_3(self):
        try:
            # Re-establish the database connection
            mydb, cursor = get_database_connection()

            # Fetch the first 10 books with the most purchases
            cursor.execute("""
                SELECT book_name, SUM(quantity) AS total_purchases
                FROM purchases
                WHERE purchase_status = 'Accepted'
                GROUP BY book_name
                ORDER BY total_purchases DESC
                LIMIT 10
            """)
            top_books = cursor.fetchall()

            if not top_books:
                messagebox.showwarning("No Data", "There are no records in the purchases table.")
                return

            # Create a new window to display the report
            report_window = tk.Toplevel(self.reports_window)
            report_window.title("Top 10 Books by Purchases")

            # Display the top books in a listbox
            listbox = tk.Listbox(report_window, width=100)
            listbox.pack(padx=20, pady=20)

            # Add the top books to the listbox
            for book in top_books:
                book_id = book[0]
                total_purchases = book[1]
                listbox.insert(tk.END, f"book name: {book_id}, Total Purchases: {total_purchases}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch data from the database: {err}")

    def generate_report_4(self):
        try:
            # Re-establish the database connection
            mydb, cursor = get_database_connection()

            # Fetch all existing categories from the books table
            cursor.execute("SELECT DISTINCT category FROM books")
            categories = [row[0] for row in cursor.fetchall()]

            if not categories:
                messagebox.showwarning("No Data", "There are no records in the books table.")
                return

            # Create a new window to prompt the manager to choose a category
            category_window = tk.Toplevel(self.reports_window)
            category_window.title("Select Category")

            # Prompt manager to choose category
            selected_category = tk.StringVar()
            category_label = tk.Label(category_window, text="Select a category:")
            category_label.pack(pady=5)
            category_dropdown = ttk.Combobox(category_window, textvariable=selected_category, values=categories,
                                             state="readonly")
            category_dropdown.pack(pady=5)
            category_dropdown.current(0)  # Default selection

            # Function to display the list of most expensive books in the selected category
            def display_most_expensive_books():
                try:
                    # Establish the database connection
                    mydb, cursor = get_database_connection()

                    category = selected_category.get()

                    # Retrieve the books belonging to the selected category and order them by price in descending order
                    cursor.execute("""
                        SELECT book_id, title, price
                        FROM books
                        WHERE category=%s
                        ORDER BY price DESC
                    """, (category,))
                    books = cursor.fetchall()

                    if not books:
                        messagebox.showinfo("No Data", f"There are no records for category '{category}'.")
                        return

                    # Create a new window to display the list of most expensive books
                    result_window = tk.Toplevel(self.reports_window)
                    result_window.title(f"Most Expensive Books in Category '{category}'")

                    # Display the list of most expensive books in a listbox
                    listbox = tk.Listbox(result_window, width=100)
                    listbox.pack(padx=10, pady=10)

                    # Add the most expensive books to the listbox
                    for book in books:
                        book_id = book[0]
                        title = book[1]
                        price = book[2]
                        listbox.insert(tk.END, f"Book ID: {book_id}, Title: {title}, Price: {price}")

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Failed to fetch data from the database: {err}")
            # Button to display the list of most expensive books
            display_button = tk.Button(category_window, text="Display Most Expensive Books",
                                       command=display_most_expensive_books)
            display_button.pack(pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to fetch data from the database: {err}")

    def generate_report_5(self):
        try:
            # Establish database connection
            mydb, cursor = get_database_connection()

            # Fetch distinct months from the purchases table
            cursor.execute("SELECT DISTINCT MONTH(submit_date) FROM purchases")
            months = [str(row[0]) for row in cursor.fetchall()]

            if not months:
                messagebox.showwarning("No Data", "There are no records in the purchases table.")
                return

            # Fetch distinct categories from the purchases table
            cursor.execute("SELECT DISTINCT category FROM purchases")
            categories = [row[0] for row in cursor.fetchall()]

            if not categories:
                messagebox.showwarning("No Data", "There are no records in the purchases table.")
                return

            # Function to display the number of buyers for the selected category and month
            def display_buyers():
                try:
                    month = selected_month.get()
                    category = selected_category.get()

                    # Retrieve the number of unique buyers who purchased from the selected category in the selected month
                    cursor.execute("""
                        SELECT COUNT(DISTINCT user())
                        FROM purchases
                        WHERE category = %s AND MONTH(submit_date) = %s AND purchase_status = 'Accepted'
                    """, (category, month))
                    num_buyers = cursor.fetchone()[0]

                    # Display the number of buyers
                    messagebox.showinfo("Number of Buyers",
                                        f"Number of buyers for category '{category}' in month {month}: {num_buyers}")

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Failed to fetch data from the database: {err}")
                finally:
                    # Close the connection
                    mydb.close()

            # Create a new window to prompt the manager to choose a month and category
            input_window = tk.Toplevel(self.reports_window)
            input_window.title("Select Month and Category")

            # Prompt manager to choose month
            selected_month = tk.StringVar()
            month_label = tk.Label(input_window, text="Select a month:")
            month_label.pack(pady=5)
            month_dropdown = ttk.Combobox(input_window, textvariable=selected_month, values=months, state="readonly")
            month_dropdown.pack(pady=5)
            month_dropdown.current(0)  # Default selection

            # Prompt manager to choose category
            selected_category = tk.StringVar()
            category_label = tk.Label(input_window, text="Select a category:")
            category_label.pack(pady=5)
            category_dropdown = ttk.Combobox(input_window, textvariable=selected_category, values=categories,
                                             state="readonly")
            category_dropdown.pack(pady=5)
            category_dropdown.current(0)  # Default selection

            # Button to display the number of buyers
            display_button = tk.Button(input_window, text="Display Number of Buyers", command=display_buyers)
            display_button.pack(pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {err}")

    def generate_report_6(self):
        pass


# # Example usage:
# root = tk.Tk()
# manager_reports = ManagerReports(root)
# manager_reports.create_report_window()
#
# # For admin reports
# # admin_reports = AdminReports(root)
# # admin_reports.create_report_window()
#
# root.mainloop()
