import  csv
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, TclError
from CONTROLLER import *


class MockView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Restaurant Management - Login")


        # Setup the login frame
        self.login_frame = ttk.Frame(self.root)
        self.login_frame.pack(padx=10, pady=10)

        # Username and password labels and entries
        ttk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="w")
        self.username_entry = ttk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, sticky="ew")

        ttk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="w")
        self.password_entry = ttk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, sticky="ew")

        # Login button
        self.login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2)



        self.root.mainloop()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_role = self.controller.authenticate_user(username, password)

        if user_role:
            messagebox.showinfo("Login Success", "You have successfully logged in as " + user_role)
            self.user_role = user_role
            self.login_frame.destroy()
            self.load_main_interface()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def load_main_interface(self):
        print("Loading main interface for user role:", self.user_role)
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title("Restaurant Management - " + self.user_role)
        self.current_items_listbox = None
        self.menu_items_listbox = None
        self.add_items_listbox = None

        if self.user_role == "Admin":
            self.create_admin_interface()
        elif self.user_role == "Manager":
            self.create_manager_interface()
        elif self.user_role == "Staff":
            self.create_staff_interface()
        elif self.user_role == "Kitchen Staff":
            self.create_kitchen_staff_interface()
        elif self.user_role == "Chef":
            self.create_chef_interface()

        self.selected_menu_item_id = None
        self.update_name_entry = None
        self.update_price_entry = None
        self.update_available_entry = None
        self.update_description_entry = None
        self.update_allergens_entry = None

    def create_admin_interface(self):
        user_mgmt_button = ttk.Button(self.root, text="User Management", command=self.open_user_mgmt_window)
        user_mgmt_button.grid(row=11, column=0, padx=10, pady=10)
        self.create_manager_interface()
        self.create_staff_interface()
        self.create_kitchen_staff_interface()
        self.create_chef_interface()



    def create_manager_interface(self):
        discount_mgmt_button = ttk.Button(self.root, text="Discount Management", command=self.open_discount_mgmt_window)
        discount_mgmt_button.grid(row=5, column=0, padx=10, pady=10)

        reservation_mgmt_button = ttk.Button(self.root, text="Reservation Management",command=self.open_reservation_mgmt_window)
        reservation_mgmt_button.grid(row=6, column=0, padx=10, pady=10)

        event_mgmt_button = ttk.Button(self.root, text="Event Management", command=self.open_event_mgmt_window)
        event_mgmt_button.grid(row=3, column=0, padx=10, pady=10)

        report_mgmt_button = ttk.Button(self.root, text="Report Management", command=self.open_reports_mgmt_window)
        report_mgmt_button.grid(row=10, column=0, padx=10, pady=10)

        menu_mgmt_button = ttk.Button(self.root, text="Menu Management", command=self.open_menu_mgmt_window)
        menu_mgmt_button.grid(row=2, column=0, padx=10, pady=10)

        payment_mgmt_button = ttk.Button(self.root, text="Payment Management", command=self.open_payment_mgmt_window)
        payment_mgmt_button.grid(row=9, column=0, padx=10, pady=10)

        locations_button = ttk.Button(self.root, text="Locations", command=self.open_locations_window)
        locations_button.grid(row=3, column=1, padx=10, pady=10)

        quit_button = ttk.Button(self.root, text="Quit", command=self.root.destroy)
        quit_button.grid(row=1, column=0, columnspan=2, pady=10)


    def create_chef_interface(self):
        menu_mgmt_button = ttk.Button(self.root, text="Menu Management", command=self.open_menu_mgmt_window)
        menu_mgmt_button.grid(row=2, column=0, padx=10, pady=10)

        kitchen_mgmt_button = ttk.Button(self.root, text="Kitchen Functions", command=self.open_kitchen_mgmt_window)
        kitchen_mgmt_button.grid(row=8, column=0, padx=10, pady=10)

        quit_button = ttk.Button(self.root, text="Quit", command=self.root.destroy)
        quit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_staff_interface(self):
        reservation_mgmt_button = ttk.Button(self.root, text="Reservation Management",command=self.open_reservation_mgmt_window)
        reservation_mgmt_button.grid(row=6, column=0, padx=10, pady=10)

        order_mgmt_button = ttk.Button(self.root, text="Order Management", command=self.open_order_mgmt_window)
        order_mgmt_button.grid(row=7, column=0, padx=10, pady=10)

        inventory_mgmt_button = ttk.Button(self.root, text="Inventory Management",command=self.open_inventory_mgmt_window)
        inventory_mgmt_button.grid(row=4, column=0, padx=10, pady=10)

        payment_mgmt_button = ttk.Button(self.root, text="Payment Management", command=self.open_payment_mgmt_window)
        payment_mgmt_button.grid(row=9, column=0, padx=10, pady=10)

        quit_button = ttk.Button(self.root, text="Quit", command=self.root.destroy)
        quit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def create_kitchen_staff_interface(self):
        kitchen_mgmt_button = ttk.Button(self.root, text="Kitchen Functions", command=self.open_kitchen_mgmt_window)
        kitchen_mgmt_button.grid(row=8, column=0, padx=10, pady=10)

        quit_button = ttk.Button(self.root, text="Quit", command=self.root.destroy)
        quit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def open_user_mgmt_window(self):
        # Create a new window for user management
        self.user_mgmt_window = tk.Toplevel(self.root)
        self.user_mgmt_window.title("User Management")

        # Add input fields for user details
        ttk.Label(self.user_mgmt_window, text="User_ID:").pack()
        self.user_id_mgmt_entry = ttk.Entry(self.user_mgmt_window)
        self.user_id_mgmt_entry.pack()

        ttk.Label(self.user_mgmt_window, text="Username:").pack()
        self.username_mgmt_entry = ttk.Entry(self.user_mgmt_window)
        self.username_mgmt_entry.pack()

        ttk.Label(self.user_mgmt_window, text="Password:").pack()
        self.password_mgmt_entry = ttk.Entry(self.user_mgmt_window, show="*")
        self.password_mgmt_entry.pack()

        ttk.Label(self.user_mgmt_window, text="Role:").pack()
        self.role_mgmt_entry = ttk.Entry(self.user_mgmt_window)
        self.role_mgmt_entry.pack()

        # Buttons for user actions
        ttk.Button(self.user_mgmt_window, text="Create User", command=self.create_user).pack()
        ttk.Button(self.user_mgmt_window, text="Update User", command=self.update_user).pack()
        ttk.Button(self.user_mgmt_window, text="Delete User", command=self.delete_user).pack()

    def create_user(self):
        username = self.username_mgmt_entry.get()
        password = self.password_mgmt_entry.get()
        role = self.role_mgmt_entry.get()
        if username and password and role:
            # Call the controller method to create a user
            self.controller.create_user(username, password, role)
            messagebox.showinfo("Success", "User created successfully")
        else:
            messagebox.showerror("Error", "All fields are required")

    def update_user(self):
        user_id = self.user_id_mgmt_entry.get()  # Assuming you have an entry field for user_id
        username = self.username_mgmt_entry.get()
        password = self.password_mgmt_entry.get()
        role = self.role_mgmt_entry.get()

        if user_id and username and role:
            self.controller.update_user(user_id, username, password, role)
            messagebox.showinfo("Success", "User updated successfully")
        else:
            messagebox.showerror("Error", "User ID, Username, and Role are required")

    def delete_user(self):
        user_id = self.user_id_mgmt_entry.get()  # Assuming you have an entry field for user_id

        if user_id:
            self.controller.delete_user(user_id)
            messagebox.showinfo("Success", "User deleted successfully")
        else:
            messagebox.showerror("Error", "User ID is required")
    def open_reports_mgmt_window(self):
        # Create a new window for report management
        self.reports_mgmt_window = tk.Toplevel(self.root)
        self.reports_mgmt_window.title("Reports Management")

        # Button to generate sales report
        generate_report_button = ttk.Button(self.reports_mgmt_window, text="Generate Sales Report",
                                            command=self.show_sales_report_ui)
        generate_report_button.pack()

        ttk.Button(self.reports_mgmt_window, text="Current Stock Report",
                   command=self.display_current_stock_report).pack()
        ttk.Button(self.reports_mgmt_window, text="Low Stock Report", command=self.display_low_stock_report).pack()

        order_report_button = ttk.Button(self.reports_mgmt_window, text="Generate Order Report",
                                         command=self.show_order_report_ui)
        order_report_button.pack()

        reservation_report_button = ttk.Button(self.reports_mgmt_window, text="Reservation Reports",
                                               command=self.show_reservation_report_ui)
        reservation_report_button.pack()
        # Add any other report-related UI components here

    def show_reservation_report_ui(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Reservation Reports")

        # Upcoming Reservations
        ttk.Label(report_window, text="Upcoming Reservations:").pack()
        upcoming_reservations_listbox = tk.Listbox(report_window, width=50)
        upcoming_reservations = self.controller.get_upcoming_reservations()
        for reservation in upcoming_reservations:
            upcoming_reservations_listbox.insert(tk.END, f"Date: {reservation[1]}, Table: {reservation[2]}")
        upcoming_reservations_listbox.pack()

        # Reservation Frequency
        ttk.Label(report_window, text="Reservation Frequency (Monthly):").pack()
        reservation_freq_listbox = tk.Listbox(report_window, width=50)
        reservation_freq = self.controller.get_reservation_frequency()
        for month, count in reservation_freq:
            reservation_freq_listbox.insert(tk.END, f"Month: {month}, Count: {count}")
        reservation_freq_listbox.pack()

        # Average Party Size
        avg_party_size = self.controller.get_average_party_size()
        ttk.Label(report_window, text=f"Average Party Size: {avg_party_size:.2f}").pack()

        # Save Report Button
        ttk.Button(report_window, text="Save Report", command=self.save_reservation_report).pack()

    def save_order_report(self):
        report_data = self.controller.get_order_report_data()
        if report_data:
            with open("order_report.txt", "w") as file:
                file.write("Order Report\n")
                file.write(f"Total Orders: {report_data[0]}\n")
                file.write(f"Average Order Value: {report_data[1]}\n")
                file.write(f"Pending Orders: {report_data[2]}\n")
                file.write(f"Preparing Orders: {report_data[3]}\n")
                file.write(f"Ready Orders: {report_data[4]}\n")
                file.write(f"Served Orders: {report_data[5]}\n")
            messagebox.showinfo("Success", "Order report saved as order_report.txt")
        else:
            messagebox.showerror("Error", "No data to save")

    def save_reservation_report(self):
        upcoming_reservations = self.controller.get_upcoming_reservations()
        reservation_freq = self.controller.get_reservation_frequency()
        avg_party_size = self.controller.get_average_party_size()

        with open("reservation_report.txt", "w") as file:
            file.write("Reservation Report\n")
            file.write("Upcoming Reservations:\n")
            for reservation in upcoming_reservations:
                file.write(f"Date: {reservation[1]}, Table: {reservation[2]}\n")
            file.write("\nReservation Frequency (Monthly):\n")
            for month, count in reservation_freq:
                file.write(f"Month: {month}, Count: {count}\n")
            file.write(f"\nAverage Party Size: {avg_party_size:.2f}\n")
        messagebox.showinfo("Success", "Reservation report saved as reservation_report.txt")

    def show_order_report_ui(self):
        report_data = self.controller.get_order_report_data()
        if not report_data:
            messagebox.showerror("Error", "No order data available.")
            return

        report_window = tk.Toplevel(self.reports_mgmt_window)
        report_window.title("Order Report")

        # Display Report Data
        tk.Label(report_window, text=f"Total Orders: {report_data[0]}").pack()
        tk.Label(report_window, text=f"Average Order Value: ${report_data[1]:.2f}").pack()
        tk.Label(report_window, text=f"Pending Orders: {report_data[2]}").pack()
        tk.Label(report_window, text=f"Preparing Orders: {report_data[3]}").pack()
        tk.Label(report_window, text=f"Ready Orders: {report_data[4]}").pack()
        tk.Label(report_window, text=f"Served Orders: {report_data[5]}").pack()

        # Save Report Button
        save_button = ttk.Button(report_window, text="Save Report", command=lambda: self.save_order_report())
        save_button.pack()

    def display_current_stock_report(self):
        branch_id = self.get_branch_id()  # Method to get the current branch ID
        report_data = self.controller.generate_current_stock_report(branch_id)
        self.show_report_in_listbox(report_data, "Current Stock Report")

    def display_low_stock_report(self):
        branch_id = self.get_branch_id()  # Method to get the current branch ID
        report_data = self.controller.generate_low_stock_report(branch_id)
        self.show_report_in_listbox(report_data, "Low Stock Report")

    def show_report_in_listbox(self, report_data, title):
        report_window = tk.Toplevel(self.reports_mgmt_window)
        report_window.title(title)

        listbox = tk.Listbox(report_window, width=50)
        listbox.pack()

        for item in report_data:
            listbox.insert(tk.END, f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}")

        save_button = ttk.Button(report_window, text="Save Report",
                                 command=lambda: self.save_report(report_data, title))
        save_button.pack()

    def save_report(self, report_data, report_title):
        # Implement logic to save the report data to a file
        filename = f"{report_title.replace(' ', '_')}.txt"
        with open(filename, 'w') as file:
            for item in report_data:
                file.write(f"ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}\n")
        messagebox.showinfo("Success", f"Report saved as {filename}")

    def get_branch_id(self):
        return 1

    def show_sales_report_ui(self):
        try:
            report_data = self.controller.generate_sales_report()
            self.display_report_data(report_data)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def display_report_data(self, report_data):
        report_window = tk.Toplevel(self.root)
        report_window.title("Sales Report")

        # Create a scrollbar
        scrollbar = tk.Scrollbar(report_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox to display the report with increased width
        report_listbox = tk.Listbox(report_window, yscrollcommand=scrollbar.set, width=50)
        total_amount_paid = 0
        for row in report_data:
            amount_paid = row[1]
            total_amount_paid += amount_paid
            report_listbox.insert(tk.END,
                                  f"Order ID: {row[0]}, Amount Paid: ${amount_paid:.2f}, Payment Method: {row[2]}")
        report_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        scrollbar.config(command=report_listbox.yview)

        # Display total amount paid
        total_label = tk.Label(report_window, text=f"Total Amount Paid: ${total_amount_paid:.2f}")
        total_label.pack()

        # Button to save the report
        save_button = ttk.Button(report_window, text="Save Report",
                                 command=lambda: self.save_report_to_file(report_data))
        save_button.pack()

    def save_report_to_file(self, report_data):
        # Save the report data to a file
        try:
            with open("sales_report.csv", "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Order ID", "Amount Paid", "Payment Method", "Order Date"])
                for row in report_data:
                    writer.writerow(row)
            messagebox.showinfo("Success", "Report saved as sales_report.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {str(e)}")

    def open_payment_mgmt_window(self):
        self.payment_mgmt_window = tk.Toplevel(self.root)
        self.payment_mgmt_window.title("Payment Management")

        # Listbox to display orders
        self.order_listbox = tk.Listbox(self.payment_mgmt_window)
        self.order_listbox.pack()
        self.refresh_order_list_for_payment()

        # Dropdown for selecting a discount
        self.discount_combobox = ttk.Combobox(self.payment_mgmt_window, state="readonly")
        self.discount_combobox.pack()
        self.populate_discounts_combobox()

        # Button for applying the selected discount
        ttk.Button(self.payment_mgmt_window, text="Apply Discount", command=self.apply_selected_discount).pack()

        # Buttons for processing payments
        ttk.Button(self.payment_mgmt_window, text="Process Cash Payment", command=self.process_cash_payment).pack()
        ttk.Button(self.payment_mgmt_window, text="Process Card Payment", command=self.process_card_payment).pack()

        ttk.Label(self.payment_mgmt_window, text="Name on Card:").pack()
        self.name_on_card_entry = ttk.Entry(self.payment_mgmt_window)
        self.name_on_card_entry.pack()

    def refresh_order_list_for_payment(self):
        # Clear the current list
        self.order_listbox.delete(0, tk.END)

        # Populate the Listbox with orders
        orders = self.controller.list_all_orders()
        for order in orders:
            self.order_listbox.insert(tk.END, f"Order ID: {order[0]}, Total: ${order[3]}")

    def populate_discounts_combobox(self):
        # Clear existing entries in the combobox
        self.discount_combobox['values'] = []

        # Fetch discount details and populate the combobox
        discounts = self.controller.list_all_discounts()
        discount_strings = [f"Discount ID: {discount[0]}, {discount[1]}% off" for discount in discounts]
        self.discount_combobox['values'] = discount_strings

    def apply_selected_discount(self):
        # Get the selected order and discount
        selected_order = self.order_listbox.get(tk.ACTIVE)
        if not selected_order:
            messagebox.showerror("Error", "No order selected")
            return

        order_id = int(selected_order.split(",")[0].split(":")[1].strip())

        selected_discount = self.discount_combobox.get()
        if not selected_discount:
            messagebox.showerror("Error", "No discount selected")
            return

        discount_id = int(selected_discount.split(",")[0].split(":")[1].strip())

        # Apply the discount
        self.controller.apply_discount_to_order(order_id, discount_id)
        messagebox.showinfo("Success", "Discount applied")
        self.refresh_order_list_for_payment()

    def process_cash_payment(self):
        self.process_payment("cash")

    def process_card_payment(self):
        # Fetch the name on the card from the input field
        name_on_card = self.name_on_card_entry.get()

        if not name_on_card:
            messagebox.showerror("Error", "Please enter the name on the card.")
            return

        # Process the payment with the name on card
        self.process_payment("card", name_on_card)

    def process_payment(self, payment_type, name_on_card=None):
        selected_order = self.order_listbox.get(tk.ACTIVE)
        if not selected_order:
            messagebox.showerror("Error", "No order selected")
            return

        order_id = int(selected_order.split(",")[0].split(":")[1].strip())

        # Process the payment
        if payment_type == "card" and name_on_card:
            self.controller.process_payment(order_id, payment_type, name_on_card=name_on_card)
        elif payment_type == "cash":
            self.controller.process_payment(order_id, payment_type)
        else:
            messagebox.showerror("Error", "Payment type not recognized or missing cardholder name.")
            return

        messagebox.showinfo("Payment Successful", f"Payment for Order ID {order_id} processed via {payment_type}")
        self.refresh_order_list_for_payment()

    def open_menu_mgmt_window(self):
        # Create a new window for menu management
        self.menu_mgmt_window = tk.Toplevel(self.root)
        self.menu_mgmt_window.title("Menu Management")

        # Add a Listbox to list all menu items
        self.menu_item_listbox = tk.Listbox(self.menu_mgmt_window)
        self.menu_item_listbox.pack()

        # Populate the Listbox with menu items
        self.refresh_menu_item_list()

        # Buttons for menu item actions
        ttk.Button(self.menu_mgmt_window, text="Create New Item", command=self.create_menu_item_ui).pack()
        ttk.Button(self.menu_mgmt_window, text="Update Selected Item", command=self.update_selected_item_ui).pack()
        ttk.Button(self.menu_mgmt_window, text="Delete Selected Item", command=self.delete_selected_item).pack()

    def open_event_mgmt_window(self):
        # Create a new window for event management
        self.event_mgmt_window = tk.Toplevel(self.root)
        self.event_mgmt_window.title("Event Management")

        # Add a Listbox to list all events
        self.event_listbox = tk.Listbox(self.event_mgmt_window)
        self.event_listbox.pack()

        # Populate the Listbox with events
        self.refresh_event_list()

        # Buttons for event actions
        ttk.Button(self.event_mgmt_window, text="Create New Event", command=self.create_event_ui).pack()
        ttk.Button(self.event_mgmt_window, text="Update Selected Event", command=self.update_selected_event_ui).pack()
        ttk.Button(self.event_mgmt_window, text="Delete Selected Event", command=self.delete_selected_event).pack()

    def open_inventory_mgmt_window(self):
        # Create a new window for inventory management
        self.inventory_mgmt_window = tk.Toplevel(self.root)
        self.inventory_mgmt_window.title("Inventory Management")

        # Add a Listbox to list all stock items
        self.stock_item_listbox = tk.Listbox(self.inventory_mgmt_window)
        self.stock_item_listbox.pack()

        # Populate the Listbox with stock items
        self.refresh_stock_item_list()

        # Buttons for stock item actions
        ttk.Button(self.inventory_mgmt_window, text="Add New Item", command=self.create_stock_item_ui).pack()
        ttk.Button(self.inventory_mgmt_window, text="Update Selected Item",
                   command=self.update_selected_stock_item_ui).pack()
        ttk.Button(self.inventory_mgmt_window, text="Delete Selected Item",
                   command=self.delete_selected_stock_item).pack()
        ttk.Button(self.inventory_mgmt_window, text="Reorder Selected Item",
                   command=self.reorder_selected_stock_item).pack()

    def open_discount_mgmt_window(self):
        self.discount_mgmt_window = tk.Toplevel(self.root)
        self.discount_mgmt_window.title("Discount Management")

        # Listbox to display discounts
        self.discount_listbox = tk.Listbox(self.discount_mgmt_window)
        self.discount_listbox.pack()

        # Refresh the list
        self.refresh_discount_list()

        # Buttons for discount actions
        ttk.Button(self.discount_mgmt_window, text="Create New Discount", command=self.create_discount_ui).pack()
        ttk.Button(self.discount_mgmt_window, text="Update Selected Discount",
                   command=self.update_selected_discount_ui).pack()
        ttk.Button(self.discount_mgmt_window, text="Delete Selected Discount",
                   command=self.delete_selected_discount).pack()

    def open_reservation_mgmt_window(self):
        # Create a new window for reservation management
        self.reservation_mgmt_window = tk.Toplevel(self.root)
        self.reservation_mgmt_window.title("Reservation Management")

        # Listbox to display reservations
        self.reservation_listbox = tk.Listbox(self.reservation_mgmt_window)
        self.reservation_listbox.pack()

        # Populate the Listbox with reservations
        self.refresh_reservation_list()

        # Buttons for reservation actions
        ttk.Button(self.reservation_mgmt_window, text="Add New Reservation", command=self.create_reservation_ui).pack()
        ttk.Button(self.reservation_mgmt_window, text="Update Selected Reservation",
                   command=self.update_selected_reservation_ui).pack()
        ttk.Button(self.reservation_mgmt_window, text="Delete Selected Reservation",
                   command=self.delete_selected_reservation).pack()

    def open_order_mgmt_window(self):
        self.order_mgmt_window = tk.Toplevel(self.root)
        self.order_mgmt_window.title("Order Management")

        self.order_listbox = tk.Listbox(self.order_mgmt_window)
        self.order_listbox.pack()

        self.refresh_order_list()

        ttk.Button(self.order_mgmt_window, text="Add New Order", command=self.create_order_ui).pack()
        ttk.Button(self.order_mgmt_window, text="Update Selected Order", command=self.update_selected_order_ui).pack()
        ttk.Button(self.order_mgmt_window, text="Delete Selected Order", command=self.delete_selected_order).pack()

    def populate_categories_combobox(self):
        categories = self.controller.get_categories()  # Fetch categories from the controller
        self.category_combobox['values'] = categories

    def on_category_selected(self):
        selected_category = self.category_combobox.get()
        if selected_category:
            self.filter_menu_items(selected_category)

    def filter_menu_items(self, category):
        if self.menu_items_listbox:
            self.menu_items_listbox.delete(0, tk.END)
            filtered_items = self.controller.filter_menu_items_by_category(category)
            for item in filtered_items:
                self.menu_items_listbox.insert(tk.END, f"{item.id}: {item.name} - ${item.price}")

    def refresh_order_list(self):
        # Clear the current list
        self.order_listbox.delete(0, tk.END)

        # Populate the Listbox with orders
        try:
            orders = self.controller.list_all_orders()
            for order in orders:
                self.order_listbox.insert(tk.END, f"Order ID: {order[0]}, User ID: {order[1]}, Branch ID: {order[2]}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list orders: {str(e)}")

    def create_order_ui(self):
        add_order_window = tk.Toplevel(self.root)
        add_order_window.title("Add New Order")

        # User ID Entry
        ttk.Label(add_order_window, text="User ID:").pack()
        user_id_entry = ttk.Entry(add_order_window)
        user_id_entry.pack()

        # Branch ID Entry
        ttk.Label(add_order_window, text="Branch ID:").pack()
        branch_id_entry = ttk.Entry(add_order_window)
        branch_id_entry.pack()

        # Menu Items Listbox
        ttk.Label(add_order_window, text="Select Menu Items:").pack()
        self.menu_items_listbox = tk.Listbox(add_order_window, selectmode='multiple')
        self.menu_items_listbox.pack()

        # Populate the Listbox with menu items
        self.menu_items_listbox.delete(0, tk.END)
        menu_items = self.controller.list_all_menu_items()
        for item in menu_items:
            self.menu_items_listbox.insert(tk.END, f"{item.id}: {item.name} - ${item.price}")

        ttk.Label(add_order_window, text="Filter by Category:").pack()
        self.category_combobox = ttk.Combobox(add_order_window, state="readonly")
        self.category_combobox.pack()
        self.populate_categories_combobox()

        filter_button = ttk.Button(add_order_window, text="Filter", command=self.on_category_selected)
        filter_button.pack()

        # Add Order Button
        add_order_button = ttk.Button(add_order_window, text="Add Order",
                                      command=lambda: self.add_order(user_id_entry.get(), branch_id_entry.get()))
        add_order_button.pack()

    def add_order(self, user_id, branch_id):
        selected_menu_items = self.get_selected_menu_item_ids()
        # Check if user_id and branch_id are provided and non-negative
        try:
            # Convert user_id and branch_id to integers
            user_id = int(user_id)
            branch_id = int(branch_id)

            # Check if user_id and branch_id are non-negative
            if user_id < 0 or branch_id < 0:
                messagebox.showerror("Error", "User ID and Branch ID must be non-negative")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid User ID or Branch ID. Please enter valid numbers.")
            return

        # Check if any menu items are selected
        if not selected_menu_items:
            messagebox.showerror("Error", "No menu items selected for the order")
            return

        # Create an Order object
        order = Order(None, user_id, branch_id, self.controller.db_manager)

        # Add selected menu items to the order
        for item_id in selected_menu_items:
            menu_item = self.controller.read_menu_item(item_id)
            if menu_item is not None:
                order.add_menu_item(menu_item)

        # Call the controller to create the order
        self.controller.create_order(order)

        # Show total price to the user
        total_price = sum(item.price for item in order.menu_items if item)  # Assuming each item has a price attribute
        messagebox.showinfo("Total Price", f"Total price of the order: ${total_price}")

    def get_selected_menu_item_ids(self):
        selected_indices = self.menu_items_listbox.curselection()
        selected_item_ids = []
        for i in selected_indices:
            item_text = self.menu_items_listbox.get(i)
            item_id = int(item_text.split(":")[0])  # Assuming the format is 'id: name - price'
            selected_item_ids.append(item_id)
        return selected_item_ids

    def create_order(self, order, order_items):
        # Assuming you have fields like user_id, branch_id in your Order class
        user_id = order.user_id
        branch_id = order.branch_id
        for item in order_items:
            order.add_menu_item(item)
        order.save_to_database()

    def update_selected_order_ui(self):
        selected_index = self.order_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No order selected")
            return

        selected_order = self.order_listbox.get(selected_index)
        order_id = int(selected_order.split(",")[0].split(":")[1].strip())
        order = self.controller.read_order(order_id)

        # Debug print
        print("Debug - Order Menu Items:", order.menu_items if order else "Order not found")

        update_window = tk.Toplevel(self.order_mgmt_window)
        update_window.title("Update Order")

        self.current_items_listbox = tk.Listbox(update_window)
        self.current_items_listbox.pack()

        if order and order.menu_items:
            for menu_item in order.menu_items:
                self.current_items_listbox.insert(tk.END, f"{menu_item.id}: {menu_item.name} - ${menu_item.price}")
        else:
            messagebox.showinfo("Information", "This order has no menu items.")
            print("Debug - No menu items found for this order.")

        ttk.Label(update_window, text="Filter by Category:").pack()
        category_combobox = ttk.Combobox(update_window, state="readonly")
        category_combobox.pack()
        category_combobox[
            'values'] = self.controller.get_categories()  # Assuming get_categories method returns a list of categories
        category_combobox.bind('<<ComboboxSelected>>',
                               lambda event: self.filter_menu_items_for_order_update(category_combobox.get(), order_id))

        # Add/Remove Menu Items
        ttk.Label(update_window, text="Select Menu Items to Add:").pack()
        self.add_items_listbox = tk.Listbox(update_window, selectmode='multiple')  # Create the Listbox
        self.add_items_listbox.pack()

        menu_items = self.controller.list_all_menu_items()

        for item in menu_items:
            self.add_items_listbox.insert(tk.END, f"{item.id}: {item.name} - ${item.price}")

        add_items_button = ttk.Button(update_window, text="Add Selected Items",
                                      command=lambda: self.add_items_to_order(order_id,
                                                                              self.add_items_listbox.curselection()))
        add_items_button.pack()

        remove_items_button = ttk.Button(update_window, text="Remove Selected Items",
                                         command=lambda: self.remove_items_from_order(order_id,
                                                                                      self.current_items_listbox.curselection()))
        remove_items_button.pack()

        # Update button
        update_button = ttk.Button(update_window, text="Update Order",
                                   command=lambda: self.refresh_order(order_id, update_window))
        update_button.pack()

    def filter_menu_items_for_order_update(self, category, order_id):
        self.add_items_listbox.delete(0, tk.END)  # Clear existing items
        filtered_items = self.controller.filter_menu_items_by_category(category)
        for item in filtered_items:
            self.add_items_listbox.insert(tk.END, f"{item.id}: {item.name} - ${item.price}")

    def add_items_to_order(self, order_id, selected_indices):
        try:
            if self.add_items_listbox is None:
                messagebox.showerror("Error", "Item selection box not initialized.")
                return

            # Check if any items are selected
            if not selected_indices:
                messagebox.showerror("Error", "No items selected to add to the order.")
                return

            # Retrieve selected menu item IDs from the Listbox
            menu_items_to_add = [int(self.add_items_listbox.get(i).split(":")[0]) for i in selected_indices]

            # Update the order with new items
            self.controller.update_order(order_id, new_menu_items=menu_items_to_add)

            # Update the current_items_listbox to reflect the new items
            for item_id in menu_items_to_add:
                item = self.controller.read_menu_item(item_id)
                self.current_items_listbox.insert(tk.END, f"{item.id}: {item.name} - ${item.price}")
        except TclError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def remove_items_from_order(self, order_id, selected_indices):
        try:
            # Debug print to check selected indices
            print("Selected indices for removal:", selected_indices)

            # Retrieve selected menu item IDs from the Listbox
            menu_items_to_remove = [int(self.current_items_listbox.get(i).split(":")[0]) for i in selected_indices]

            # Debug print to check the IDs of the items to be removed
            print("Menu item IDs to remove:", menu_items_to_remove)

            # Check if any items are selected for removal
            if menu_items_to_remove:
                # Update the order by removing items
                self.controller.update_order(order_id, menu_items_to_remove=menu_items_to_remove)

                # Re-fetch and refresh the Listbox with updated menu items
                updated_order = self.controller.read_order(order_id)
                self.current_items_listbox.delete(0, tk.END)
                for menu_item in updated_order.menu_items:
                    self.current_items_listbox.insert(tk.END, f"{menu_item.id}: {menu_item.name} - ${menu_item.price}")
            else:
                messagebox.showinfo("Information", "No items selected to remove.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove items: {str(e)}")

    def refresh_order(self, order_id, window):
        try:
            order = self.controller.read_order(order_id)
            if order:
                # Pass the order_id instead of the order object
                self.controller.update_order(order.order_id)

                # Refresh the Listbox with updated order items
                self.current_items_listbox.delete(0, tk.END)
                for menu_item in order.menu_items:
                    self.current_items_listbox.insert(tk.END, f"{menu_item.id}: {menu_item.name} - ${menu_item.price}")

                messagebox.showinfo("Success", "Order updated successfully!")
                window.destroy()
                self.refresh_order_list()
            else:
                messagebox.showerror("Error", "Failed to find the updated order.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update order: {str(e)}")

    def delete_selected_order(self):
        selected_index = self.order_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No order selected")
            return
        selected_order = self.order_listbox.get(selected_index)
        order_id = int(selected_order.split(",")[0].split(":")[1].strip())

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this order?")
        if confirm:
            try:
                self.controller.delete_order(order_id)
                messagebox.showinfo("Success", "Order deleted successfully!")
                self.refresh_order_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete order: {str(e)}")

    def open_kitchen_mgmt_window(self):
        self.kitchen_window = tk.Toplevel(self.root)
        self.kitchen_window.title("Kitchen Order Management")
        self.kitchen_order_management_ui()

    def kitchen_order_management_ui(self):
        # Listbox to display orders
        self.order_listbox = tk.Listbox(self.kitchen_window)
        self.order_listbox.pack()
        self.order_listbox.bind('<<ListboxSelect>>', self.order_selected)

        ttk.Label(self.kitchen_window, text="Menu Items in Order:").pack()
        self.menu_items_listbox = tk.Listbox(self.kitchen_window)
        self.menu_items_listbox.pack()
        # self.menu_items_listbox = tk.Listbox(self.kitchen_window, selectmode=tk.SINGLE)
        self.menu_items_listbox.bind('<<ListboxSelect>>', self.mark_item_unavailable)

        # Populate the Listbox with orders
        self.refresh_order_list_for_kitchen()

        # Buttons for order actions
        ttk.Button(self.kitchen_window, text="Mark as Preparing", command=self.mark_order_preparing).pack()
        ttk.Button(self.kitchen_window, text="Mark as Ready", command=self.mark_order_ready).pack()
        ttk.Button(self.kitchen_window, text="Mark Item Unavailable", command=self.mark_item_unavailable).pack()
        # self.menu_items_listbox = tk.Listbox(self.kitchen_window)
        # self.menu_items_listbox.pack()

    def order_selected(self, event):
        # Clear the menu items listbox
        self.menu_items_listbox.delete(0, tk.END)

        # Get the index of the selected order
        selected_index = self.order_listbox.curselection()
        if not selected_index:  # No order is selected
            self.selected_order_id = None
            return

        # Extract order_id and store it
        selected_order = self.order_listbox.get(selected_index[0])
        self.selected_order_id = int(selected_order.split(',')[0].split(':')[1].strip())

        # Fetch the menu items for the selected order using the stored order ID
        menu_items = self.controller.get_menu_items_for_order(self.selected_order_id)

        # Populate the menu items listbox
        for item in menu_items:
            menu_item_id = item[1]
            item_name = item[2]
            self.menu_items_listbox.insert(tk.END, f"Item ID: {menu_item_id}, Name: {item_name}")

    def mark_item_unavailable(self, event=None):
        if self.selected_order_id is None:
            messagebox.showerror("Error", "No order selected")
            return

        selected_menu_item_indices = self.menu_items_listbox.curselection()
        if not selected_menu_item_indices:
            messagebox.showerror("Error", "No menu item selected")
            return

        selected_menu_item_id = int(
            self.menu_items_listbox.get(selected_menu_item_indices[0]).split(",")[0].split(":")[1].strip())

        confirm = messagebox.askyesno("Confirm", "Mark this item as unavailable?")
        if confirm:
            # Mark the item as unavailable
            self.controller.handle_unavailable_item(self.selected_order_id, selected_menu_item_id)
            messagebox.showinfo("Success", "Item marked as unavailable")

            # Suggest a replacement item
            self.suggest_replacement_item(selected_menu_item_id)

            # Refresh the menu items for the selected order
            self.refresh_menu_items_for_selected_order(self.selected_order_id)

        replacement_item_id = self.suggest_replacement_item(selected_menu_item_id)

        if replacement_item_id:
            # Call the method with the correct number of arguments
            self.controller.replace_menu_item(self.selected_order_id, selected_menu_item_id, replacement_item_id)
            # Refresh the UI
            self.refresh_menu_items_for_selected_order(self.selected_order_id)

    def suggest_replacement_item(self, unavailable_item_id):
        available_items = self.controller.get_all_available_menu_items()

        for item_tuple in available_items:
            item_id, item_name = item_tuple[0], item_tuple[1]
            if item_id != unavailable_item_id:
                confirm = messagebox.askyesno("Replacement Suggestion",
                                              f"Replace with Item ID: {item_id}, Name: {item_name}?")
                if confirm:
                    return item_id  # Return the ID of the item to replace with
                else:
                    break  # Break the loop if user clicks "No"
        return None

    def refresh_order_list_for_kitchen(self):
        self.order_listbox.delete(0, tk.END)  # Clear existing items

        orders = self.controller.list_all_orders()
        for order in orders:
            order_id = order[0]
            order_status = order[4]
            self.order_listbox.insert(tk.END, f"Order ID: {order_id}, Status: {order_status}")
        self.menu_items_listbox.delete(0, tk.END)

    def refresh_menu_items_for_selected_order(self, order_id):
        # Clear the current menu items listbox
        self.menu_items_listbox.delete(0, tk.END)

        # Fetch the menu items for the selected order
        menu_items = self.controller.get_menu_items_for_order(order_id)

        # Populate the menu items listbox with the fetched menu items
        for menu_item_id, name in menu_items:
            self.menu_items_listbox.insert(tk.END, f"Item ID: {menu_item_id}, Name: {name}")

    def mark_order_preparing(self):
        selected_index = self.order_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No order selected")
            return

        order_id = int(self.order_listbox.get(selected_index).split(",")[0].split(":")[1].strip())
        self.controller.mark_order_as_preparing(order_id)
        messagebox.showinfo("Success", "Order marked as preparing")
        self.refresh_order_list_for_kitchen()

    def mark_order_ready(self):
        selected_index = self.order_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No order selected")
            return
        order_id = int(self.order_listbox.get(selected_index).split(",")[0].split(":")[1].strip())
        self.controller.mark_order_as_ready(order_id)
        messagebox.showinfo("Success", "Order marked as ready")
        self.refresh_order_list_for_kitchen()

    def refresh_reservation_list(self):
        # Clear the current list
        self.reservation_listbox.delete(0, tk.END)

        # Populate the Listbox with reservations
        reservations = self.controller.list_all_reservations()
        for reservation in reservations:
            self.reservation_listbox.insert(tk.END,
                                            f"Reservation ID: {reservation[0]}, Date: {reservation[1]}, Table: {reservation[2]}")

    def create_reservation_ui(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Reservation")

        ttk.Label(add_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = ttk.Entry(add_window)
        date_entry.pack()

        ttk.Label(add_window, text="Table Number:").pack()
        table_number_entry = ttk.Entry(add_window)
        table_number_entry.pack()

        submit_button = ttk.Button(add_window, text="Add Reservation",
                                   command=lambda: self.add_reservation(date_entry.get(), table_number_entry.get(),
                                                                        add_window))
        submit_button.pack()

    def add_reservation(self, date, table_number, window):
        # Prompt for branch ID
        branch_id = simpledialog.askinteger("Input", "Enter branch ID", parent=self.root)
        if branch_id is None:
            return  # User cancelled or entered invalid input

        # Check if all fields are filled
        if not date or table_number is None:
            messagebox.showerror("Error", "All fields must be filled")
            return

        # Validate the date format
        try:
            parsed_date = datetime.strptime(date, '%Y/%m/%d')  # Assuming the desired format is YYYY/MM/DD
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY/MM/DD format")
            return

        try:
            table_number = int(table_number)
            if table_number < 0:
                messagebox.showerror("Error", "Table number must be a non-negative integer")
                return

            self.controller.create_reservation(None, date, table_number, branch_id)
            messagebox.showinfo("Success", "Reservation added successfully!")
            window.destroy()
            self.refresh_reservation_list()  # Refresh the list to show the new reservation
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid table number.")

    def update_selected_reservation_ui(self):
        selected_index = self.reservation_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No reservation selected")
            return

        selected_reservation = self.reservation_listbox.get(selected_index)
        reservation_id = int(selected_reservation.split(",")[0].split(":")[1].strip())

        reservation = self.controller.read_reservation(reservation_id)

        update_window = tk.Toplevel(self.root)
        update_window.title("Update Reservation")

        ttk.Label(update_window, text="Date (YYYY-MM-DD):").pack()
        date_entry = ttk.Entry(update_window)
        date_entry.insert(0, reservation.date)
        date_entry.pack()

        ttk.Label(update_window, text="Table Number:").pack()
        table_number_entry = ttk.Entry(update_window)
        table_number_entry.insert(0, reservation.table_number)
        table_number_entry.pack()

        update_button = ttk.Button(update_window, text="Update Reservation",
                                   command=lambda: self.update_reservation(reservation_id, date_entry.get(),
                                                                           table_number_entry.get(), update_window))
        update_button.pack()

    def update_reservation(self, reservation_id, date, table_number, window):
        # Prompt for branch ID
        branch_id = simpledialog.askinteger("Input", "Enter branch ID", parent=self.root)
        if branch_id is None:
            return  # User cancelled or entered invalid input

        # Check if all fields are filled
        if not date or table_number is None:
            messagebox.showerror("Error", "All fields must be filled")
            return

        # Validate the date format
        try:
            parsed_date = datetime.strptime(date, '%Y/%m/%d')  # Assuming the desired format is YYYY/MM/DD
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY/MM/DD format")
            return

        try:
            table_number = int(table_number)
            if table_number < 0:
                messagebox.showerror("Error", "Table number must be a non-negative integer")
                return

            self.controller.update_reservation(reservation_id, date, table_number, branch_id)
            messagebox.showinfo("Success", "Reservation updated successfully!")
            window.destroy()
            self.refresh_reservation_list()  # Refresh the list to show updated reservation
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid table number.")

    def delete_selected_reservation(self):
        selected_index = self.reservation_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No reservation selected")
            return

        selected_reservation = self.reservation_listbox.get(selected_index)
        reservation_id = int(selected_reservation.split(",")[0].split(":")[1].strip())

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this reservation?")
        if confirm:
            self.controller.delete_reservation(reservation_id)
            messagebox.showinfo("Success", "Reservation deleted successfully!")
            self.refresh_reservation_list()

    def refresh_discount_list(self):
        # Clear the current list
        self.discount_listbox.delete(0, tk.END)

        # Populate the Listbox with discounts
        discounts = self.controller.list_all_discounts()
        for discount in discounts:
            discount_id = discount[0]
            percentage = discount[1]
            description = discount[2]
            self.discount_listbox.insert(tk.END, f"Discount ID: {discount_id}, {percentage}% - {description}")

    def create_discount_ui(self):
        add_window = tk.Toplevel(self.discount_mgmt_window)
        add_window.title("Add New Discount")

        ttk.Label(add_window, text="Discount Percentage:").pack()
        percentage_entry = ttk.Entry(add_window)
        percentage_entry.pack()

        ttk.Label(add_window, text="Description:").pack()
        description_entry = ttk.Entry(add_window)
        description_entry.pack()

        submit_button = ttk.Button(add_window, text="Add Discount",
                                   command=lambda: self.add_discount(percentage_entry.get(), description_entry.get(),
                                                                     add_window))
        submit_button.pack()

    def add_discount(self, percentage, description, window):
        # Check if all fields are filled
        if percentage is None or description == "":
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            percentage = float(percentage)
            if percentage <= 0 or percentage > 100:
                messagebox.showerror("Error", "Percentage must be a positive number less than or equal to 100")
                return

            self.controller.create_discount(None, percentage, description)
            messagebox.showinfo("Success", "Discount added successfully!")
            window.destroy()
            self.refresh_discount_list()
        except ValueError:
            messagebox.showerror("Error", "Invalid percentage entered")

    def update_selected_discount_ui(self):
        selected_index = self.discount_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No discount selected")
            return

        selected_discount = self.discount_listbox.get(selected_index)
        discount_id = int(selected_discount.split(",")[0].split(":")[1].strip())

        discount = self.controller.read_discount(discount_id)

        update_window = tk.Toplevel(self.discount_mgmt_window)
        update_window.title("Update Discount")

        ttk.Label(update_window, text="Discount Percentage:").pack()
        percentage_entry = ttk.Entry(update_window)
        percentage_entry.insert(0, discount.percentage)
        percentage_entry.pack()

        ttk.Label(update_window, text="Description:").pack()
        description_entry = ttk.Entry(update_window)
        description_entry.insert(0, discount.description)
        description_entry.pack()

        update_button = ttk.Button(update_window, text="Update Discount",
                                   command=lambda: self.update_discount(discount_id, percentage_entry.get(),
                                                                        description_entry.get(), update_window))
        update_button.pack()

    def update_discount(self, discount_id, percentage, description, window):
        # Check if all fields are filled
        if percentage is None or description == "":
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            percentage = float(percentage)
            if percentage <= 0 or percentage > 100:
                messagebox.showerror("Error", "Percentage must be a positive number less than or equal to 100")
                return

            self.controller.update_discount(discount_id, percentage, description)
            messagebox.showinfo("Success", "Discount updated successfully!")
            window.destroy()
            self.refresh_discount_list()
        except ValueError:
            messagebox.showerror("Error", "Invalid percentage entered")

    def delete_selected_discount(self):
        selected_index = self.discount_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No discount selected")
            return

        selected_discount = self.discount_listbox.get(selected_index)
        discount_id = int(selected_discount.split(",")[0].split(":")[1].strip())

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this discount?")
        if confirm:
            self.controller.delete_discount(discount_id)
            messagebox.showinfo("Success", "Discount deleted successfully!")
            self.refresh_discount_list()

    def refresh_stock_item_list(self):
        # Clear the current list
        self.stock_item_listbox.delete(0, tk.END)

        # Populate the Listbox with stock items
        stock_items = self.controller.list_all_stock_items()
        for item in stock_items:
            self.stock_item_listbox.insert(tk.END, f"{item[0]}: {item[1]} - Quantity: {item[2]}")

        # Method to open UI for creating a new stock item

    def create_stock_item_ui(self):
        add_window = tk.Toplevel(self.inventory_mgmt_window)
        add_window.title("Add Stock Item")

        # Add input fields for stock item details
        ttk.Label(add_window, text="Name:").pack()
        name_entry = ttk.Entry(add_window)
        name_entry.pack()

        ttk.Label(add_window, text="Quantity:").pack()
        quantity_entry = ttk.Entry(add_window)
        quantity_entry.pack()

        ttk.Label(add_window, text="Reorder Level:").pack()
        reorder_level_entry = ttk.Entry(add_window)
        reorder_level_entry.pack()

        # Button to submit the new stock item
        submit_button = ttk.Button(add_window, text="Add Item",
                                   command=lambda: self.add_stock_item(name_entry.get(), quantity_entry.get(),
                                                                       reorder_level_entry.get(), add_window))
        submit_button.pack()

    def add_stock_item(self, name, quantity, reorder_level, window):
        branch_id = simpledialog.askinteger("Input", "Enter branch ID", parent=self.root)
        if branch_id is None:
            return  # User cancelled or entered invalid input

        # Check if all fields are filled
        if not name or quantity is None or reorder_level is None:
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            quantity = int(quantity)
            reorder_level = int(reorder_level)
            if quantity < 0 or reorder_level < 0:
                messagebox.showerror("Error", "Quantity and reorder level must be non-negative")
                return

            self.controller.create_stock_item(branch_id, name, quantity, reorder_level)
            messagebox.showinfo("Success", "Stock item added successfully!")
            window.destroy()
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for quantity and reorder level.")

        # Method to open UI for updating a selected stock item

    def update_selected_stock_item_ui(self):
        selected_index = self.stock_item_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected")
            return

        selected_item = self.stock_item_listbox.get(selected_index)
        item_id = int(selected_item.split(":")[0])
        stock_item = self.controller.read_stock_item(item_id)

        update_window = tk.Toplevel(self.inventory_mgmt_window)
        update_window.title("Update Stock Item")

        ttk.Label(update_window, text="Name:").pack()
        name_entry = ttk.Entry(update_window)
        name_entry.insert(0, stock_item.name)
        name_entry.pack()

        ttk.Label(update_window, text="Quantity:").pack()
        quantity_entry = ttk.Entry(update_window)
        quantity_entry.insert(0, stock_item.quantity)
        quantity_entry.pack()

        ttk.Label(update_window, text="Reorder Level:").pack()
        reorder_level_entry = ttk.Entry(update_window)
        reorder_level_entry.insert(0, stock_item.reorder_level)
        reorder_level_entry.pack()

        update_button = ttk.Button(update_window, text="Update Item",
                                   command=lambda: self.update_stock_item(item_id, name_entry.get(),
                                                                          quantity_entry.get(),
                                                                          reorder_level_entry.get(), update_window))
        update_button.pack()

        # Method to handle updating a stock item

    def update_stock_item(self, item_id, name, quantity, reorder_level, window):
        branch_id = simpledialog.askinteger("Input", "Enter branch ID", parent=self.root)
        if branch_id is None:
            return  # User cancelled or entered invalid input

        # Check if all fields are filled
        if not name or quantity is None or reorder_level is None:
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            quantity = int(quantity)
            reorder_level = int(reorder_level)
            if quantity < 0 or reorder_level < 0:
                messagebox.showerror("Error", "Quantity and reorder level must be non-negative")
                return

            self.controller.update_stock_item(item_id, name, quantity, reorder_level, branch_id)
            messagebox.showinfo("Success", "Stock item updated successfully!")
            window.destroy()
            self.refresh_stock_item_list()  # Refresh the list
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers for quantity and reorder level.")

        # Method to delete a selected stock item

    def delete_selected_stock_item(self):
        selected_index = self.stock_item_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected")
            return

        selected_item = self.stock_item_listbox.get(selected_index)
        item_id = int(selected_item.split(":")[0])

        branch_id = simpledialog.askinteger("Input", "Enter branch ID", parent=self.root)
        if branch_id is None:
            return

        self.controller.delete_stock_item(item_id, branch_id)
        messagebox.showinfo("Success", "Stock item deleted successfully!")
        self.refresh_stock_item_list()

        # Method to reorder a selected stock item

    def reorder_selected_stock_item(self):
        selected_index = self.stock_item_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected")
            return

        selected_item = self.stock_item_listbox.get(selected_index)
        item_id = int(selected_item.split(":")[0])

        self.controller.reorder_stock_item(item_id)
        messagebox.showinfo("Success", "Stock item reordered successfully!")
        self.refresh_stock_item_list()

    def refresh_event_list(self):
        # Clear the current list
        self.event_listbox.delete(0, tk.END)

        # Populate the Listbox with event data
        events = self.controller.list_all_events()
        for event in events:
            # Assuming the event tuple is structured as (event_id, event_name, event_date, ...)
            event_id, event_name, event_date = event[:3]
            self.event_listbox.insert(tk.END, f"{event_id}: {event_name} - {event_date}")

    def create_event_ui(self):
        add_event_window = tk.Toplevel(self.root)
        add_event_window.title("Add New Event")

        ttk.Label(add_event_window, text="Event Name:").pack()
        event_name_entry = ttk.Entry(add_event_window)
        event_name_entry.pack()

        ttk.Label(add_event_window, text="Event Date:").pack()
        event_date_entry = ttk.Entry(add_event_window)
        event_date_entry.pack()

        ttk.Label(add_event_window, text="Event Type:").pack()
        event_type_entry = ttk.Entry(add_event_window)
        event_type_entry.pack()

        submit_button = ttk.Button(add_event_window, text="Add Event",
                                   command=lambda: self.add_event(event_name_entry.get(), event_date_entry.get(),
                                                                  event_type_entry.get(), add_event_window))
        submit_button.pack()

    def add_event(self, name, date, event_type, window):
        branch_id = 1  # Assuming a default branch ID for simplicity

        # Check if all fields are filled
        if not name or not date or not event_type:
            messagebox.showerror("Error", "All fields must be filled")
            return

        # Validate the date format
        try:
            parsed_date = datetime.strptime(date, '%Y/%m/%d')
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY/MM/DD format")
            return

        try:
            self.controller.create_event(None, name, date, event_type, branch_id)
            messagebox.showinfo("Success", "Event added successfully!")
            window.destroy()
            self.refresh_event_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_selected_event_ui(self):
        selected_index = self.event_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No event selected")
            return

        selected_event = self.event_listbox.get(selected_index)
        event_id = int(selected_event.split(":")[0])
        event = self.controller.read_event(event_id)

        update_event_window = tk.Toplevel(self.root)
        update_event_window.title("Update Event")

        ttk.Label(update_event_window, text="Event Name:").pack()
        event_name_entry = ttk.Entry(update_event_window)
        event_name_entry.insert(0, event.get_event_name())
        event_name_entry.pack()

        ttk.Label(update_event_window, text="Event Date:").pack()
        event_date_entry = ttk.Entry(update_event_window)
        event_date_entry.insert(0, event.get_event_date())
        event_date_entry.pack()

        ttk.Label(update_event_window, text="Event Type:").pack()
        event_type_entry = ttk.Entry(update_event_window)
        event_type_entry.insert(0, event.get_event_type())
        event_type_entry.pack()

        update_button = ttk.Button(update_event_window, text="Update Event",
                                   command=lambda: self.update_event(event_id, event_name_entry.get(),
                                                                     event_date_entry.get(), event_type_entry.get(),
                                                                     update_event_window))
        update_button.pack()

    def update_event(self, event_id, name, date, event_type, window):
        # Check if all fields are filled
        if not name or not date or not event_type:
            messagebox.showerror("Error", "All fields must be filled")
            return

        # Validate the date format
        try:
            parsed_date = datetime.strptime(date, '%Y/%m/%d')
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY/MM/DD format")
            return

        # If date format is correct, proceed to update the event
        try:
            self.controller.update_event(event_id, name, date, event_type)
            messagebox.showinfo("Success", "Event updated successfully!")
            window.destroy()
            self.refresh_event_list()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def delete_selected_event(self):
        selected_index = self.event_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No event selected")
            return

        selected_event = self.event_listbox.get(selected_index)
        event_id = int(selected_event.split(":")[0])

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this event?")
        if confirm:
            try:
                self.controller.delete_event(event_id)
                messagebox.showinfo("Success", "Event deleted successfully!")
                self.refresh_event_list()  # Refresh the event list
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def refresh_menu_item_list(self):
        # Clear the current list
        self.menu_item_listbox.delete(0, tk.END)

        # Populate the Listbox with menu items
        menu_items = self.controller.list_all_menu_items()
        for item in menu_items:
            self.menu_item_listbox.insert(tk.END, f"{item.id}: {item.name} - ${item.price}")

    def list_all_menu_items(self):
        try:
            menu_items = self.controller.list_all_menu_items()
            items_str = "\n".join([f"Item: {item.name}, Price: {item.price}" for item in menu_items])
            messagebox.showinfo("Menu Items", items_str)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list menu items: {str(e)}")

    def create_menu_item_ui(self):
        # Create a new window for adding a menu item
        add_window = tk.Toplevel(self.menu_mgmt_window)
        add_window.title("Add Menu Item")

        # Add input fields for menu item details
        ttk.Label(add_window, text="Name:").pack()
        name_entry = ttk.Entry(add_window)
        name_entry.pack()

        ttk.Label(add_window, text="Price:").pack()
        price_entry = ttk.Entry(add_window)
        price_entry.pack()

        ttk.Label(add_window, text="Description:").pack()
        description_entry = ttk.Entry(add_window)
        description_entry.pack()

        ttk.Label(add_window, text="Allergens:").pack()
        allergens_entry = ttk.Entry(add_window)
        allergens_entry.pack()

        # Category selection
        ttk.Label(add_window, text="Category:").pack()
        category_entry = ttk.Entry(add_window)
        category_entry.pack()
        # Availability
        ttk.Label(add_window, text="Availability:").pack()
        availability_entry = ttk.Entry(add_window)
        availability_entry.pack()

        # Button to submit the new menu item
        submit_button = ttk.Button(add_window, text="Add Item",
                                   command=lambda: self.add_menu_item(name_entry.get(), price_entry.get(),
                                                                      description_entry.get(), allergens_entry.get(),
                                                                      category_entry.get(), availability_entry.get(),
                                                                      add_window))
        submit_button.pack()

    def filter_menu_items_by_category_ui(self):
        # UI logic for filtering menu items by category
        pass

    def add_menu_item(self, name, price, description, allergens, category, availability, window):
        if not name or not price or not description or not allergens or not category or not availability:
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            price = float(price)
            if price <= 0:
                messagebox.showerror("Error", "Price must be positive")
                return

            availability = int(availability)
            if availability < 0:
                messagebox.showerror("Error", "Availability must be a non-negative integer")
                return

            # Pass the details to the controller's method
            self.controller.create_menu_item(None, price, availability, name, description, allergens, 1, category)
            messagebox.showinfo("Success", "Menu item added successfully!")
            window.destroy()
            self.refresh_menu_item_list()
        except ValueError:
            messagebox.showerror("Error", "Invalid price or availability entered")

    def update_selected_item_ui(self):
        selected_index = self.menu_item_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected")
            return

        selected_item = self.menu_item_listbox.get(selected_index)
        item_id = int(selected_item.split(":")[0])
        item = self.controller.read_menu_item(item_id)

        # Create update window
        update_window = tk.Toplevel(self.menu_mgmt_window)
        update_window.title("Update Menu Item")

        # Add input fields prefilled with item details
        ttk.Label(update_window, text="Name:").pack()
        name_entry = ttk.Entry(update_window)
        name_entry.insert(0, item.name)
        name_entry.pack()

        ttk.Label(update_window, text="Price:").pack()
        price_entry = ttk.Entry(update_window)
        price_entry.insert(0, item.price)
        price_entry.pack()

        ttk.Label(update_window, text="Description:").pack()
        description_entry = ttk.Entry(update_window)
        description_entry.insert(0, item.description)
        description_entry.pack()

        ttk.Label(update_window, text="Allergens:").pack()
        allergens_entry = ttk.Entry(update_window)
        allergens_entry.insert(0, item.allergens)
        allergens_entry.pack()

        # Category
        ttk.Label(update_window, text="Category:").pack()
        category_entry = ttk.Entry(update_window)
        category_value = str(item.category)  # Convert to string if not already
        category_entry.insert(0, category_value)  # Insert the string value
        category_entry.pack()

        # Availability
        ttk.Label(update_window, text="Availability:").pack()
        availability_entry = ttk.Entry(update_window)
        availability_entry.insert(0, item.availability)  # Assuming item has an availability attribute
        availability_entry.pack()

        # Button to submit updates
        update_button = ttk.Button(update_window, text="Update Item",
                                   command=lambda: self.update_menu_item(item_id, name_entry.get(), price_entry.get(),
                                                                         description_entry.get(), allergens_entry.get(),
                                                                         category_entry.get(), availability_entry.get(),
                                                                         update_window))
        update_button.pack()

    def update_menu_item(self, item_id, name, price, description, allergens, category, availability, window):
        # Check if all fields are filled
        if not name or not price or not description or not allergens or not category or not availability:
            messagebox.showerror("Error", "All fields must be filled")
            return

        try:
            price = float(price)
            availability = int(availability)
            if price <= 0:
                messagebox.showerror("Error", "Price must be positive")
                return
            if availability < 0:
                messagebox.showerror("Error", "Availability must be a non-negative integer")
                return

            # Pass the details to the controller's method for updating
            self.controller.update_menu_item(item_id, name, price, availability, description, allergens, category)
            messagebox.showinfo("Success", "Menu item updated successfully!")
            window.destroy()
            self.refresh_menu_item_list()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def delete_selected_item(self):
        selected_index = self.menu_item_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "No item selected")
            return

        selected_item = self.menu_item_listbox.get(selected_index)
        item_id = int(selected_item.split(":")[0])

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?")
        if confirm:
            self.controller.delete_menu_item(item_id)
            messagebox.showinfo("Success", "Menu item deleted successfully!")
            self.refresh_menu_item_list()



    #RESIT CODE
    def open_locations_window(self):
        self.locations_window = tk.Toplevel(self.root)
        self.locations_window.title("Manage Locations")

        locations = self.controller.get_branches()

        self.locations_listbox = tk.Listbox(self.locations_window)
        self.locations_listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.update_locations_listbox(locations)

        add_button = ttk.Button(self.locations_window, text="Add Location", command=self.add_location)
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        remove_button = ttk.Button(self.locations_window, text="Remove Selected", command=self.remove_selected_location)
        remove_button.pack(side=tk.LEFT, padx=10, pady=10)

    def update_locations_listbox(self, locations):
        self.locations_listbox.delete(0, tk.END)
        for location in locations:
            self.locations_listbox.insert(tk.END, f"{location[0]}: {location[1]}, {location[2]}")

    def add_location(self):
        location = simpledialog.askstring("Location", "Enter the location (e.g., 'Country, City'):")
        name = simpledialog.askstring("Name", "Enter the branch name:")

        if location and name:
            self.controller.add_branch(location, name)
            self.update_locations_listbox(self.controller.get_branches())
        else:
            messagebox.showwarning("Invalid Input", "Location and Name cannot be empty.")

    def remove_selected_location(self):
        selected = self.locations_listbox.curselection()
        if selected:
            branch_id = int(self.locations_listbox.get(selected).split(":")[0])
            self.controller.remove_branch(branch_id)
            self.update_locations_listbox(self.controller.get_branches())
        else:
            messagebox.showwarning("No Selection", "Please select a location to remove.")

    #RESIT CODE END
            
            
    def run(self):
        self.root.mainloop()

# Example usage:
db_name = 'restaurant_management.db'
controller = RestaurantController(db_name)
view = MockView(controller)
view.run()
