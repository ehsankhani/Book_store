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
        report_types = ["Report 1", "Report 2", "Report 3"]
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
        # Add your implementation for Report 2 here
        pass

    def generate_report_3(self):
        # Add your implementation for Report 3 here
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
