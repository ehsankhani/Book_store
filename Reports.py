import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from DataBase_Connection import get_database_connection
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import decimal


class ManagerReports:
    def __init__(self,  parent):
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
        report_types = ["Report 1", "Report 2", "Report 3", "Report 4", "Report 5", "Report 6", "Report 7", "Report 8"]
        self.selected_report = tk.StringVar(self.reports_window)
        self.selected_report.set(report_types[0])  # Default selection
        report_dropdown = ttk.Combobox(self.reports_window, textvariable=self.selected_report, values=report_types, state="readonly")
        report_dropdown.pack(pady=5)

        # Button to generate selected report
        generate_button = tk.Button(self.reports_window, text="Generate Report", command=self.generate_report)
        generate_button.pack(pady=5)
        # Button to have the description
        generate_button = tk.Button(self.reports_window, text="Report description", command=self.report_description)
        generate_button.pack(pady=5)

        # Button for generating custom reports
        custom_report_button = tk.Button(self.reports_window, text="Custom Report", command=self.generate_custom_report)
        custom_report_button.pack(pady=5)

    def report_description(self):
        # Create a new window for report descriptions
        description_window = tk.Toplevel(self.parent)
        description_window.title("Report Descriptions")

        # Add labels for report descriptions
        report1_label = tk.Label(description_window,
                                 text="Report 1: Sum of each category in each month", font=("Helvetica", 16))
        report1_label.pack(anchor=tk.W)

        report2_label = tk.Label(description_window,
                                 text="Report 2: Sum of each category in store", font=("Helvetica", 16))
        report2_label.pack(anchor=tk.W)

        report3_label = tk.Label(description_window,
                                 text="Report 3: top 10 most purchased books", font=("Helvetica", 16))
        report3_label.pack(anchor=tk.W)

        report4_label = tk.Label(description_window,
                                 text="Report 4: most expensive books in each category", font=("Helvetica", 16))
        report4_label.pack(anchor=tk.W)

        report5_label = tk.Label(description_window,
                                 text="Report 5: List of the buyers who purchased from each category in each month",
                                 font=("Helvetica", 16))
        report5_label.pack(anchor=tk.W)

        report6_label = tk.Label(description_window,
                                 text="Report 6: avg sell price for each user in each month", font=("Helvetica", 16))
        report6_label.pack(anchor=tk.W)

        report7_label = tk.Label(description_window,
                                 text="Report 7: avg number of the books published", font=("Helvetica", 16))
        report7_label.pack(anchor=tk.W)

        report8_label = tk.Label(description_window,
                                 text="Report 8: avg number of the customers in daily", font=("Helvetica", 16))
        report8_label.pack(anchor=tk.W)

        # Add a button to close the window
        close_button = tk.Button(description_window, text="Close", command=description_window.destroy)
        close_button.pack(anchor=tk.CENTER)

        # Run the Tkinter event loop for the description_window
        description_window.mainloop()

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
        elif report_type == "Report 7":
            self.generate_report_7()
        elif report_type == "Report 8":
            self.generate_report_8()

    def generate_custom_report(self):
        mydb, cursor = get_database_connection()

        # Fetch data from the database
        cursor.execute("SELECT category FROM purchases")
        category_data = cursor.fetchall()

        cursor.execute("SELECT credit_card_type FROM purchases")
        credit_card_data = cursor.fetchall()

        cursor.execute("SELECT DISTINCT user_id FROM purchases")
        user_ids = cursor.fetchall()

        cursor.execute(
            "SELECT MONTH(purchase_date) AS month, COUNT(*) AS purchases FROM purchases GROUP BY MONTH(purchase_date)")
        monthly_purchases = cursor.fetchall()

        # Prepare data for plotting
        categories = [row[0] for row in category_data]
        credit_cards = [row[0] for row in credit_card_data]
        user_ids = [row[0] for row in user_ids]
        months = [row[0] for row in monthly_purchases]
        purchases = [row[1] for row in monthly_purchases]

        # Create a new window for reports
        reports_window = tk.Toplevel(self.parent)
        reports_window.title("Custom Reports")

        # Start window in full screen mode
        reports_window.attributes('-fullscreen', True)

        # Create a canvas with scrollbars
        canvas = tk.Canvas(reports_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(reports_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas
        reports_frame = tk.Frame(canvas)
        canvas.create_window((reports_window.winfo_width() / 2, 0), window=reports_frame, anchor="n")

        # Plot 1: Category of Books
        fig1 = plt.figure(figsize=(15, 8))
        pd.Series(categories).value_counts().plot(kind='bar', color='skyblue')
        plt.title('Category of Books in Purchases')
        plt.xlabel('Category')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=reports_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Plot 2: Type of Credit Cards
        fig2 = plt.figure(figsize=(8, 6))
        pd.Series(credit_cards).value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Type of Credit Cards in Purchases')
        plt.ylabel('')
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=reports_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Plot 3: User IDs with Purchases
        fig3 = plt.figure(figsize=(8, 6))
        plt.plot(user_ids, marker='o', linestyle='-', color='orange')
        plt.title('User IDs with Purchases')
        plt.xlabel('Index')
        plt.ylabel('User ID')
        plt.tight_layout()
        canvas3 = FigureCanvasTkAgg(fig3, master=reports_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Plot 4: Monthly Purchases
        fig4 = plt.figure(figsize=(8, 6))
        plt.bar(months, purchases, color='green')
        plt.title('Monthly Purchases')
        plt.xlabel('Month')
        plt.ylabel('Number of Purchases')
        plt.xticks(months)
        plt.tight_layout()
        canvas4 = FigureCanvasTkAgg(fig4, master=reports_frame)
        canvas4.draw()
        canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add a button to close the window
        close_button = tk.Button(reports_frame, text="Close", command=reports_window.destroy)
        close_button.pack(side=tk.BOTTOM)

        # Set the canvas as scrollable region
        canvas.config(scrollregion=canvas.bbox("all"))

        # Run the Tkinter event loop for the reports_window
        reports_window.mainloop()

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
        try:
            # Establish database connection
            mydb, cursor = get_database_connection()

            # Fetch distinct users from the purchase table
            cursor.execute("SELECT DISTINCT user_id FROM purchases")
            users = [row[0] for row in cursor.fetchall()]

            if not users:
                messagebox.showwarning("No Data", "There are no records in the purchases table.")
                return

            # Function to calculate and display the average purchase for the selected user
            def display_average_purchase():
                try:
                    selected_user = selected_username.get()

                    # Retrieve the total quantity and total cost of purchases made by the selected user
                    cursor.execute("""
                        SELECT SUM(quantity), SUM(quantity * price)
                        FROM purchases
                        WHERE user_id = %s AND purchase_status = 'Accepted'
                    """, (selected_user,))
                    # Inside display_average_purchase function
                    total_quantity, total_cost = cursor.fetchone()

                    # Convert total_cost and total_quantity to float or decimal.Decimal
                    total_cost = float(total_cost) if total_cost else 0
                    total_quantity = float(total_quantity) if total_quantity else 0

                    # Calculate the average purchase
                    if total_quantity != 0:
                        average_purchase = total_cost / total_quantity
                        messagebox.showinfo("Average Purchase",
                                            f"Average purchase for user '{selected_user}': {average_purchase:.2f}")
                    else:
                        messagebox.showinfo("Average Purchase",
                                            f"No purchase data available for user '{selected_user}'.")

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Failed to fetch data from the database: {err}")
                finally:
                    # Close the connection
                    mydb.close()

            # Create a new window to prompt the manager to choose a user
            input_window = tk.Toplevel(self.reports_window)
            input_window.title("Select User")

            # Prompt manager to choose a user
            selected_username = tk.StringVar()
            username_label = tk.Label(input_window, text="Select a user:")
            username_label.pack(pady=5)
            username_dropdown = ttk.Combobox(input_window, textvariable=selected_username, values=users,
                                             state="readonly")
            username_dropdown.pack(pady=5)
            username_dropdown.current(0)  # Default selection

            # Button to display the average purchase
            display_button = tk.Button(input_window, text="Display Average Purchase", command=display_average_purchase)
            display_button.pack(pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {err}")

    def generate_report_7(self):
        try:
            # Establish database connection
            mydb, cursor = get_database_connection()

            # Query to calculate the total number of books sold and the total number of purchases
            cursor.execute("SELECT SUM(quantity), COUNT(*) FROM purchases")
            total_books_sold, total_purchases = cursor.fetchone()

            if not total_books_sold or not total_purchases:
                messagebox.showwarning("No Data", "There are no records in the purchases table.")
                return

            # Calculate the average number of books sold per purchase
            average_books_per_purchase = total_books_sold / total_purchases

            # Display the average number of books sold per purchase
            messagebox.showinfo("Average Books Sold per Purchase",
                                f"Average number of books sold per purchase: {average_books_per_purchase:.2f}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {err}")

    def generate_report_8(self):
        try:
            # Establish database connection
            mydb, cursor = get_database_connection()

            # Query to fetch the oldest purchase date
            cursor.execute("SELECT MIN(purchase_date) FROM purchases")
            oldest_purchase_date = cursor.fetchone()[0]

            if not oldest_purchase_date:
                messagebox.showwarning("No Data", "There are no records in the purchases table.")
                return

            # Calculate the number of days between the oldest purchase date and the current date
            current_date = datetime.now().date()
            days_difference = (current_date - oldest_purchase_date.date()).days

            # Query to fetch the total number of customers
            cursor.execute("SELECT COUNT(DISTINCT user_id) FROM purchases")
            total_customers = cursor.fetchone()[0]

            # Calculate the average number of customers per day
            average_customers_per_day = total_customers / days_difference if days_difference > 0 else 0

            # Display the average number of customers per day
            messagebox.showinfo("Average Customers per Day",
                                f"Average number of customers per day: {average_customers_per_day:.2f}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {err}")


class AdminReports:
    def __init__(self, parent):
        self.parent = parent

    def create_report_window(self):
        # Create a new window for reports
        self.reports_window = tk.Toplevel(self.parent)
        self.reports_window.title("Admin Reports")

        # Set initial dimensions of the window
        window_width = 600
        window_height = 400
        screen_width = self.reports_window.winfo_screenwidth()
        screen_height = self.reports_window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        self.reports_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Configure window background color
        self.reports_window.configure(bg="#F0F0F0")

        # Add GUI elements for reports
        tk.Label(self.reports_window, text="Reports", font=("Helvetica", 24), bg="#F0F0F0").pack(pady=20)

        # Dropdown menu for selecting report type
        report_types = ["Admin Report 1", "Admin Report 2", "Admin Report 3", "Admin Report 4", "Admin Report 5",
                        "Admin Report 6", "Admin Report 7", "Admin Report 8"]
        self.selected_report = tk.StringVar(self.reports_window)
        self.selected_report.set(report_types[0])  # Default selection
        report_dropdown = ttk.Combobox(self.reports_window, textvariable=self.selected_report, values=report_types,
                                       state="readonly", font=("Helvetica", 14))
        report_dropdown.pack(pady=10)

        # Button to generate selected report
        generate_button = tk.Button(self.reports_window, text="Generate Report", command=self.generate_report,
                                    font=("Helvetica", 14), bg="#4CAF50", fg="white", bd=0)
        generate_button.pack(pady=10)

        # Button to display report description
        description_button = tk.Button(self.reports_window, text="Report Description", command=self.report_description,
                                       font=("Helvetica", 14), bg="#3498DB", fg="white", bd=0)
        description_button.pack(pady=10)

        # Button for generating custom reports
        custom_report_button = tk.Button(self.reports_window, text="Custom Report", command=self.generate_custom_report,
                                         font=("Helvetica", 14), bg="#FF5733", fg="white", bd=0)
        custom_report_button.pack(pady=10)

    def report_description(self):
        # Create a new window for report descriptions
        description_window = tk.Toplevel(self.parent)
        description_window.title("Report Descriptions")

        # Set initial dimensions of the window
        window_width = 900
        window_height = 650
        screen_width = description_window.winfo_screenwidth()
        screen_height = description_window.winfo_screenheight()
        x_coordinate = int((screen_width - window_width) / 2)
        y_coordinate = int((screen_height - window_height) / 2)
        description_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Configure window background color and border
        description_window.configure(bg="#F0F0F0")
        description_window.attributes("-alpha", 0.95)  # Set transparency level

        # Add title label
        title_label = tk.Label(description_window, text="Report Descriptions", font=("Helvetica", 24), bg="#3498DB",
                               fg="white")
        title_label.pack(fill=tk.X, pady=20)

        # Add labels for report descriptions
        reports = [
            "Report 1: Sum of each category in each month",
            "Report 2: Sum of each category in store",
            "Report 3: Top 10 most purchased books",
            "Report 4: Most expensive books in each category",
            "Report 5: List of the buyers who purchased from each category in each month",
            "Report 6: Average sell price for each user in each month",
            "Report 7: Average number of the books published",
            "Report 8: Average number of customers daily",
        ]

        for i, report in enumerate(reports, 1):
            report_label = tk.Label(description_window, text=report, font=("Helvetica", 16), bg="#F0F0F0")
            report_label.pack(anchor=tk.W, padx=20, pady=10)

        # Add a button to close the window
        close_button = tk.Button(description_window, text="Close", command=description_window.destroy,
                                 font=("Helvetica", 14), bg="#E74C3C", fg="white", bd=0)
        close_button.pack(pady=20)

    def generate_report(self):
        report_type = self.selected_report.get()
        if report_type == "Admin Report 1":
            self.generate_admin_report_1()
        elif report_type == "Admin Report 2":
            self.generate_admin_report_2()
        elif report_type == "Admin Report 3":
            self.generate_admin_report_3()
        elif report_type == "Admin Report 4":
            self.generate_admin_report_4()
        elif report_type == "Admin Report 5":
            self.generate_admin_report_5()
        elif report_type == "Admin Report 6":
            self.generate_admin_report_6()
        elif report_type == "Admin Report 7":
            self.generate_admin_report_7()
        elif report_type == "Admin Report 8":
            self.generate_admin_report_8()

    def generate_custom_report(self):
        mydb, cursor = get_database_connection()

        # Fetch data from the database
        cursor.execute("SELECT category FROM purchases")
        category_data = cursor.fetchall()

        cursor.execute("SELECT credit_card_type FROM purchases")
        credit_card_data = cursor.fetchall()

        cursor.execute("SELECT DISTINCT user_id FROM purchases")
        user_ids = cursor.fetchall()

        cursor.execute(
            "SELECT MONTH(purchase_date) AS month, COUNT(*) AS purchases FROM purchases GROUP BY MONTH(purchase_date)")
        monthly_purchases = cursor.fetchall()

        # Prepare data for plotting
        categories = [row[0] for row in category_data]
        credit_cards = [row[0] for row in credit_card_data]
        user_ids = [row[0] for row in user_ids]
        months = [row[0] for row in monthly_purchases]
        purchases = [row[1] for row in monthly_purchases]

        # Create a new window for reports
        reports_window = tk.Toplevel(self.parent)
        reports_window.title("Custom Reports")

        # Start window in full screen mode
        reports_window.attributes('-fullscreen', True)

        # Create a canvas with scrollbars
        canvas = tk.Canvas(reports_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(reports_window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Create a frame inside the canvas
        reports_frame = tk.Frame(canvas)
        canvas.create_window((reports_window.winfo_width() / 2, 0), window=reports_frame, anchor="n")

        # Plot 1: Category of Books
        fig1 = plt.figure(figsize=(15, 8))
        pd.Series(categories).value_counts().plot(kind='bar', color='skyblue')
        plt.title('Category of Books in Purchases')
        plt.xlabel('Category')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=reports_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Plot 2: Type of Credit Cards
        fig2 = plt.figure(figsize=(8, 6))
        pd.Series(credit_cards).value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Type of Credit Cards in Purchases')
        plt.ylabel('')
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=reports_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Plot 3: User IDs with Purchases
        fig3 = plt.figure(figsize=(8, 6))
        plt.plot(user_ids, marker='o', linestyle='-', color='orange')
        plt.title('User IDs with Purchases')
        plt.xlabel('Index')
        plt.ylabel('User ID')
        plt.tight_layout()
        canvas3 = FigureCanvasTkAgg(fig3, master=reports_frame)
        canvas3.draw()
        canvas3.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Plot 4: Monthly Purchases
        fig4 = plt.figure(figsize=(8, 6))
        plt.bar(months, purchases, color='green')
        plt.title('Monthly Purchases')
        plt.xlabel('Month')
        plt.ylabel('Number of Purchases')
        plt.xticks(months)
        plt.tight_layout()
        canvas4 = FigureCanvasTkAgg(fig4, master=reports_frame)
        canvas4.draw()
        canvas4.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Add a button to close the window
        close_button = tk.Button(reports_frame, text="Close", command=reports_window.destroy)
        close_button.pack(side=tk.BOTTOM)

        # Set the canvas as scrollable region
        canvas.config(scrollregion=canvas.bbox("all"))

    def generate_admin_report_1(self):
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

    def generate_admin_report_2(self):
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

    def generate_admin_report_3(self):
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

    def generate_admin_report_4(self):
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

    def generate_admin_report_5(self):
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

    def generate_admin_report_6(self):
        try:
            # Establish database connection
            mydb, cursor = get_database_connection()

            # Fetch distinct users from the purchase table
            cursor.execute("SELECT DISTINCT user_id FROM purchases")
            users = [row[0] for row in cursor.fetchall()]

            if not users:
                messagebox.showwarning("No Data", "There are no records in the purchases table.")
                return

            # Function to calculate and display the average purchase for the selected user
            def display_average_purchase():
                try:
                    selected_user = selected_username.get()

                    # Retrieve the total quantity and total cost of purchases made by the selected user
                    cursor.execute("""
                        SELECT SUM(quantity), SUM(quantity * price)
                        FROM purchases
                        WHERE user_id = %s AND purchase_status = 'Accepted'
                    """, (selected_user,))
                    # Inside display_average_purchase function
                    total_quantity, total_cost = cursor.fetchone()

                    # Convert total_cost and total_quantity to float or decimal.Decimal
                    total_cost = float(total_cost) if total_cost else 0
                    total_quantity = float(total_quantity) if total_quantity else 0

                    # Calculate the average purchase
                    if total_quantity != 0:
                        average_purchase = total_cost / total_quantity
                        messagebox.showinfo("Average Purchase",
                                            f"Average purchase for user '{selected_user}': {average_purchase:.2f}")
                    else:
                        messagebox.showinfo("Average Purchase",
                                            f"No purchase data available for user '{selected_user}'.")

                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Failed to fetch data from the database: {err}")
                finally:
                    # Close the connection
                    mydb.close()

            # Create a new window to prompt the manager to choose a user
            input_window = tk.Toplevel(self.reports_window)
            input_window.title("Select User")

            # Prompt manager to choose a user
            selected_username = tk.StringVar()
            username_label = tk.Label(input_window, text="Select a user:")
            username_label.pack(pady=5)
            username_dropdown = ttk.Combobox(input_window, textvariable=selected_username, values=users,
                                             state="readonly")
            username_dropdown.pack(pady=5)
            username_dropdown.current(0)  # Default selection

            # Button to display the average purchase
            display_button = tk.Button(input_window, text="Display Average Purchase", command=display_average_purchase)
            display_button.pack(pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {err}")

    def generate_admin_report_7(self):
        try:
            # Establish database connection
            mydb, cursor = get_database_connection()

            # Query to calculate the total number of books sold and the total number of purchases
            cursor.execute("SELECT SUM(quantity), COUNT(*) FROM purchases")
            total_books_sold, total_purchases = cursor.fetchone()

            if not total_books_sold or not total_purchases:
                messagebox.showwarning("No Data", "There are no records in the purchases table.")
                return

            # Calculate the average number of books sold per purchase
            average_books_per_purchase = total_books_sold / total_purchases

            # Display the average number of books sold per purchase
            messagebox.showinfo("Average Books Sold per Purchase",
                                f"Average number of books sold per purchase: {average_books_per_purchase:.2f}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {err}")

    def generate_admin_report_8(self):
        try:
            # Establish database connection
            mydb, cursor = get_database_connection()

            # Query to fetch the oldest purchase date
            cursor.execute("SELECT MIN(purchase_date) FROM purchases")
            oldest_purchase_date = cursor.fetchone()[0]

            if not oldest_purchase_date:
                messagebox.showwarning("No Data", "There are no records in the purchases table.")
                return

            # Calculate the number of days between the oldest purchase date and the current date
            current_date = datetime.now().date()
            days_difference = (current_date - oldest_purchase_date.date()).days

            # Query to fetch the total number of customers
            cursor.execute("SELECT COUNT(DISTINCT user_id) FROM purchases")
            total_customers = cursor.fetchone()[0]

            # Calculate the average number of customers per day
            average_customers_per_day = total_customers / days_difference if days_difference > 0 else 0

            # Display the average number of customers per day
            messagebox.showinfo("Average Customers per Day",
                                f"Average number of customers per day: {average_customers_per_day:.2f}")

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to connect to the database: {err}")



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
