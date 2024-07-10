import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path='/Users/oladmin/Desktop/CS-Y2/ASD RESIT/OscarLinehan21015730RESTUARANT_MANAGEMENT_SYSTEM/restaurant_management.db'):
        self.db_path = db_path
        print(f"Database path: {self.db_path}")
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            print(f"Connected to database at {self.db_path}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")



    def execute_query(self, query, params=()):
        try:
            if self.conn is None:
                self.connect()
            print(f"Executing query: {query} with params: {params}")
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None

    def fetch_one(self, query, params=()):
        try:
            self.connect()
            print(f"Fetching one: {query} with params: {params}")
            self.cursor.execute(query, params)
            result = self.cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        except Exception as e:
            print(f"Exception in fetch_one: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed")

    def fetch_all(self, query, parameters=None):
        self.connect()  # Ensure the connection is open
        if parameters is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, parameters)
        results = self.cursor.fetchall()
        self.close()  # Close the connection after fetching data
        return results

    def save_to_database(self, query, parameters=None):
        self.execute_query(query, parameters)

    def fetch_order_total_price(self, order_id):
        # Implement the logic to fetch and return the total price of the order
        query = "SELECT total_price FROM orders WHERE id = ?"
        self.cursor.execute(query, (order_id,))
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def fetch_discount_details(self, discount_id):
        # Implement the logic to fetch and return discount details
        query = "SELECT percentage, description, valid FROM discounts WHERE id = ?"
        self.cursor.execute(query, (discount_id,))
        return self.cursor.fetchone()  # Returns a tuple (percentage, description, valid)

    def save_payment_details(self, order_id, discount_id, final_price):
        # Implement the logic to save payment details
        query = "INSERT INTO payments (order_id, discount_id, total_price) VALUES (?, ?, ?)"
        self.cursor.execute(query, (order_id, discount_id, final_price))
        self.conn.commit()

class Branch:
    def __init__(self, location, name, branch_id=None):
        self.branch_id = branch_id
        self.location = location
        self.name = name
        self.reservations = []  # This would be a list of Reservation objects
        self.orders = []  # This would be a list of Order objects
        self.reports = []  # This would be a list of Report objects
        self.events = []  # This would be a list of Event objects
        self.inventory = Inventory(branch_id)  # This would be an instance of an Inventory class

    def get_reservations(self, db_manager):
        query = 'SELECT * FROM reservations WHERE branch_id = ?'
        parameters = (self.branch_id,)
        return db_manager.fetch_all(query, parameters)

    def get_inventory(self, db_manager):
        query = 'SELECT * FROM inventory WHERE branch_id = ?'
        parameters = (self.branch_id,)
        return db_manager.fetch_all(query, parameters)

    def get_events(self, db_manager):
        query = 'SELECT * FROM events WHERE branch_id = ?'
        parameters = (self.branch_id,)
        return db_manager.fetch_all(query, parameters)

    def get_reports(self, db_manager):
        query = 'SELECT * FROM reports WHERE branch_id = ?'
        parameters = (self.branch_id,)
        return db_manager.fetch_all(query, parameters)

    def get_orders(self, db_manager):
        query = 'SELECT * FROM orders WHERE branch_id = ?'
        parameters = (self.branch_id,)
        return db_manager.fetch_all(query, parameters)

    def add_order(self, order, db_manager):
        query = "INSERT INTO orders (user_id, branch_id) VALUES (?, ?)"
        parameters = (order.user_id, self.branch_id)
        db_manager.execute_query(query, parameters)

    # Add other methods for CRUD operations related to reservations, inventory, events, and reports

    def get_name(self) -> str:
        return self.name

    def get_location(self) -> str:
        return self.location

class Menu:
    def __init__(self, restaurant_management_id, db_manager):
        self.menu_items = []
        self.restaurant_management_id = restaurant_management_id
        self.db_manager = db_manager

    def add_menu_item(self, menu_item):
        query = '''
            INSERT INTO menu_items (price, available, name, description, allergens, menu_id, category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        '''
        # Include the category in the parameters
        parameters = (menu_item.price, menu_item.available, menu_item.name, menu_item.description, menu_item.allergens,self.restaurant_management_id, menu_item.category)
        self.db_manager.save_to_database(query, parameters)

    def remove_menu_item(self, menu_item):
        query = 'DELETE FROM menu_items WHERE id = ?'
        parameters = (menu_item.id,)
        self.db_manager.save_to_database(query, parameters)

    def get_menu_item_id(self, menu_item_id):
        query = 'SELECT * FROM menu_items WHERE id = ?'
        parameters = (menu_item_id,)
        result = self.db_manager.fetch_all(query, parameters)
        if result:
            item_data = result[0]
            return MenuItem(item_data[0], item_data[1], item_data[2], item_data[3], item_data[4], item_data[5], item_data[6], item_data[7], self.db_manager)
        else:
            return None

    def get_all_menu_items(self):
        query = 'SELECT * FROM menu_items WHERE menu_id = ?'
        parameters = (self.restaurant_management_id,)
        result = self.db_manager.fetch_all(query, parameters)
        menu_items = []
        for item in result:
            # Assuming the item tuple includes all necessary fields for MenuItem
            # Update to match the structure of your database
            menu_item = MenuItem(item[0], item[1], item[2], item[3], item[4], item[5], self.restaurant_management_id,
                                 item[6], self.db_manager)
            menu_items.append(menu_item)
        return menu_items


class RestaurantManagement:
    def __init__(self, user_id, username, password, role, db_manager):
        self.user_id = user_id
        self.username = username
        self.password = password  # In a real system, you'd want to hash this!
        self.role = role
        self.branches = []  # This will be a list of Branch instances
        self.menu = Menu(self.user_id, db_manager)  # Pass the user_id to the Menu constructor

    def login(self):
        # Logic for user login
        pass

    def logout(self):
        # Logic for user logout
        pass

    def add_branch(self, location, name):
        branch_id = len(self.branches) + 1  # Assign a unique ID for the branch
        self.db_manager.execute_query("INSERT INTO branches (id, location, name) VALUES (?, ?, ?)",
                                      (branch_id, location, name))
        self.branches.append((branch_id, location, name))  # Update the internal list

    def remove_branch(self, branch_id):
        self.db_manager.execute_query("DELETE FROM branches WHERE id = ?", (branch_id,))
        self.branches = [branch for branch in self.branches if branch[0] != branch_id]

    def get_branches(self):
        query = 'SELECT * FROM branches'
        return self.db_manager.fetch_all(query)

    def get_menu(self):
        return self.menu

class MenuItem:
    def __init__(self, id, price, availability, name, description, allergens, menu_id, category, db_manager):
        self.id = id
        self.price = price
        self.availability = availability
        self.name = name
        self.description = description
        self.allergens = allergens
        self.menu_id = menu_id
        self.category = category
        self.db_manager = db_manager

    def update(self, price=None, available=None, name=None, description=None, allergens=None, category=None):
        # Update object attributes if new values provided
        if price is not None:
            self.price = price
        if available is not None:
            self.available = available
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        if allergens is not None:
            self.allergens = allergens
        if category is not None:
            self.category = category

        # Update SQL query to include all fields
        query = '''UPDATE menu_items SET price=?, available=?, name=?, description=?, allergens=?, category=? WHERE id=?'''
        parameters = (self.price, self.available, self.name, self.description, self.allergens, self.category, self.id)
        self.db_manager.execute_query(query, parameters)

    def delete_from_database(self):
        query = "DELETE FROM menu_items WHERE id=?"
        parameters = (self.id,)
        self.db_manager.execute_query(query, parameters)

    def get_menu_item_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def is_available(self):
        return self.available

    def update_price(self, price):
        self.price = price
        query = '''
            UPDATE menu_items
            SET price = ?
            WHERE id = ?
        '''
        parameters = (self.price, self.id)
        self.db_manager.execute_query(query, parameters)

    def set_price(self, price):
        self.price = price
        query = '''
            UPDATE menu_items
            SET price = ?
            WHERE id = ?
        '''
        parameters = (self.price, self.id)
        self.db_manager.execute_query(query, parameters)

class Report:
    def __init__(self, report_id, report_type, duration, branch_location, branch_id, db_manager):
        self.report_id = report_id
        self.type = report_type
        self.duration = duration
        self.branch_location = branch_location
        self.branch_id = branch_id
        self.db_manager = db_manager

    def generate_report(self):
        # Logic to generate the report
        pass

    def print_report(self):
        # Logic to print the report
        pass

    def download_report(self):
        # Logic to download the report
        pass

    def get_report_id(self):
        return self.report_id

    def get_type(self):
        return self.type

    def save_to_database(self):
        query = '''
            INSERT INTO reports (report_type, duration, branch_location, branch_id)
            VALUES (?, ?, ?, ?)
        '''
        parameters = (self.type, self.duration, self.branch_location, self.branch_id)
        self.db_manager.execute_query(query, parameters)

    def get_sales_report(self):
        query = """
        SELECT p.order_id, COALESCE(ccp.amount_paid, p.total_price) AS amount_paid, 
               CASE WHEN ccp.amount_paid IS NOT NULL THEN 'Credit Card' ELSE 'Cash' END AS payment_method
        FROM payments p
        LEFT JOIN credit_card_payments ccp ON p.order_id = ccp.order_id;
        """
        self.db_manager.execute_query(query)
        return self.db_manager.cursor.fetchall()
    def update(self, report_type, duration, branch_location, branch_id):
        self.type = report_type
        self.duration = duration
        self.branch_location = branch_location
        self.branch_id = branch_id
        query = "UPDATE reports SET report_type=?, duration=?, branch_location=?, branch_id=? WHERE report_id=?"
        parameters = (self.type, self.duration, self.branch_location, self.branch_id, self.report_id)
        self.db_manager.execute_query(query, parameters)

    def delete_from_database(self):
        query = "DELETE FROM reports WHERE report_id=?"
        parameters = (self.report_id,)
        self.db_manager.execute_query(query, parameters)
class Event:
    def __init__(self, event_id, event_name, event_date, event_type, branch_id, db_manager):
        self.event_id = event_id
        self.event_name = event_name
        self.event_date = event_date
        self.event_type = event_type
        self.branch_id = branch_id
        self.db_manager = db_manager

    def get_event_id(self):
        return self.event_id

    def get_event_name(self):
        return self.event_name

    def get_event_date(self):
        return self.event_date

    def get_event_type(self):
        return self.event_type

    def save_to_database(self):
        query = '''
            INSERT INTO events (event_name, event_date, event_type, branch_id)
            VALUES (?, ?, ?, ?)
        '''
        parameters = (self.event_name, self.event_date, self.event_type, self.branch_id)
        self.db_manager.execute_query(query, parameters)

    def update(self, event_name=None, event_date=None, event_type=None, branch_id=None):
        # Update the event's attributes if new values are provided
        if event_name is not None:
            self.event_name = event_name
        if event_date is not None:
            self.event_date = event_date
        if event_type is not None:
            self.event_type = event_type
        if branch_id is not None:
            self.branch_id = branch_id

        # Update the event record in the database
        query = '''
            UPDATE events 
            SET event_name = ?, event_date = ?, event_type = ?, branch_id = ?
            WHERE event_id = ?
        '''
        parameters = (self.event_name, self.event_date, self.event_type, self.branch_id, self.event_id)
        self.db_manager.execute_query(query, parameters)

    # Delete the event from the database
    def delete_from_database(self):
        query = "DELETE FROM events WHERE event_id = ?"
        parameters = (self.event_id,)
        self.db_manager.execute_query(query, parameters)
class Inventory:
    def __init__(self, branch_id, db_manager):
        self.stock_items = []
        self.branch_id = branch_id
        self.db_manager = db_manager

    def get_stock_item_by_id(self, item_id):
        query = "SELECT * FROM inventory_items WHERE id = ?"
        parameters = (item_id,)
        result = self.db_manager.fetch_all(query, parameters)

        # Check if the item is found
        if result:
            # Assuming the columns in your database table are id, name, quantity, reorder_level, branch_id
            item_data = result[0]  # Get the first row of the result
            return StockItem(item_data[0], item_data[1], item_data[2], item_data[3], item_data[4], self.db_manager)
        else:
            # Return None if no item is found
            return None
    def get_all_stock_items(self):
        query = "SELECT * FROM inventory_items WHERE branch_id = ?"
        parameters = (self.branch_id,)
        result = self.db_manager.fetch_all(query, parameters)
        return [StockItem(item[0], item[1], item[2], item[3], self.branch_id, self.db_manager) for item in result]
    def create_stock_item(self, stock_item):
        query = '''
            INSERT INTO inventory_items (name, quantity, reorder_level, branch_id)
            VALUES (?, ?, ?, ?)
        '''
        parameters = (stock_item.get_name(), stock_item.get_quantity(), stock_item.get_reorder_level(), self.branch_id)
        self.db_manager.execute_query(query, parameters)
        self.stock_items.append(stock_item)

    def update_stock_item(self, stock_item):
        query = '''
            UPDATE inventory_items
            SET name=?, quantity=?, reorder_level=?
            WHERE id=?
        '''
        parameters = (stock_item.get_name(), stock_item.get_quantity(), stock_item.get_reorder_level(), stock_item.get_item_id())
        self.db_manager.execute_query(query, parameters)

        for item in self.stock_items:
            if item.get_item_id() == stock_item.get_item_id():
                item = stock_item
                break

    def delete_stock_item(self, stock_item_id):
        query = "DELETE FROM inventory_items WHERE id=?"
        parameters = (stock_item_id,)  # Use stock_item_id directly
        self.db_manager.execute_query(query, parameters)

        # Update the stock_items list if necessary
        self.stock_items = [item for item in self.stock_items if item.get_item_id() != stock_item_id]

    def reorder_notification(self):
        for item in self.stock_items:
            if item.get_quantity() <= item.get_reorder_level():
                print(f"Item {item.get_name()} with ID {item.get_item_id()} needs to be reordered.")

    def get_current_stock_report(self):
        query = "SELECT id, name, quantity FROM inventory_items WHERE branch_id = ?"
        return self.db_manager.fetch_all(query, (self.branch_id,))

    def get_low_stock_report(self):
        query = "SELECT id, name, quantity FROM inventory_items WHERE quantity <= reorder_level AND branch_id = ?"
        return self.db_manager.fetch_all(query, (self.branch_id,))

class StockItem:
    def __init__(self, item_id, name, quantity, reorder_level, branch_id, db_manager):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.reorder_level = reorder_level
        self.branch_id = branch_id
        self.db_manager = db_manager

    def update_quantity(self, amount):
        self.quantity += amount
        query = '''
            UPDATE inventory_items
            SET quantity=?
            WHERE id=?
        '''
        parameters = (self.quantity, self.item_id)
        self.db_manager.execute_query(query, parameters)

    def get_item_id(self):
        return self.item_id

    def get_name(self):
        return self.name

    def get_quantity(self):
        return self.quantity

    def get_reorder_level(self):
        return self.reorder_level

class Order:
    def __init__(self, order_id, user_id, branch_id, db_manager):
        self.order_id = order_id
        self.user_id = user_id
        self.branch_id = branch_id
        self.menu_items = []  # Holds MenuItem objects
        self.db_manager = db_manager
        self.items_to_add = set()  # To keep track of items to add
        self.items_to_remove = set()  # To keep track of items to remove
        self.status = 'Pending'  # Possible statuses: Pending, Preparing, Ready, Served
        self.preparation_start_time = None
        self.preparation_end_time = None

    def mark_as_preparing(self):
        self.status = 'Preparing'
        self.preparation_start_time = datetime.now()
        self.update_order_status()

    def mark_as_ready(self):
        self.status = 'Ready'
        self.preparation_end_time = datetime.now()
        self.update_order_status()

    def calculate_preparation_time(self):
        if self.preparation_start_time and self.preparation_end_time:
            return (self.preparation_end_time - self.preparation_start_time).total_seconds()
        else:
            return None

    def update_order_status(self):
        query = "UPDATE orders SET status=?, preparation_start_time=?, preparation_end_time=? WHERE id=?"
        parameters = (self.status, self.preparation_start_time, self.preparation_end_time, self.order_id)
        self.db_manager.execute_query(query, parameters)

    def fetch_total_price(self):
        # Fetch total price from the database
        return self.db_manager.fetch_order_total_price(self.order_id)

    def get_order_id(order_id, db_manager):
        # Fetch basic order details
        order_query = 'SELECT * FROM orders WHERE id = ?'
        order_result = db_manager.fetch_all(order_query, (order_id,))
        if not order_result:
            return None

        order_data = order_result[0]
        order = Order(order_data[0], order_data[1], order_data[2], db_manager)

        # Fetch associated menu items
        menu_items_query = """
        SELECT mi.id, mi.price, mi.available, mi.name, mi.description, mi.allergens, mi.menu_id, mi.category
        FROM order_items AS oi
        JOIN menu_items AS mi ON oi.menu_item_id = mi.id
        WHERE oi.order_id = ?;
        """
        menu_items_result = db_manager.fetch_all(menu_items_query, (order_id,))
        for item_data in menu_items_result:
            menu_item = MenuItem(*item_data,
                                 db_manager)  # Ensure the number of elements in item_data matches the constructor
            order.menu_items.append(menu_item)

        return order

    def add_menu_item(self, menu_item):
        if menu_item not in self.menu_items:
            self.menu_items.append(menu_item)
            # No need for items_to_add set unless specifically required elsewhere

    def remove_menu_item(self, menu_item):
        print(f"Attempting to remove item ID: {menu_item.id}")
        for existing_item in self.menu_items:
            if existing_item.id == menu_item.id:
                self.menu_items.remove(existing_item)
                print(f"Removed item: {menu_item.id}")
                break
            # No need for items_to_remove set unless specifically required elsewhere


    def calculate_total_price(self):
        self.total_price = sum(item.price for item in self.menu_items)

    def save_to_database(self):
        # Update or insert the order
        if self.order_id is None:
            insert_query = 'INSERT INTO orders (user_id, branch_id) VALUES (?, ?)'
            self.db_manager.execute_query(insert_query, (self.user_id, self.branch_id))
            self.order_id = self.db_manager.fetch_all('SELECT last_insert_rowid()')[0][0]
        else:
            update_query = "UPDATE orders SET user_id=?, branch_id=? WHERE id=?"
            self.db_manager.execute_query(update_query, (self.user_id, self.branch_id, self.order_id))

        # Debug: print current state of menu_items
        print(f"Current menu items in order: {[item.id for item in self.menu_items]}")

        # Synchronize the menu items with the database
        # First, remove all items from the database for this order
        self.db_manager.execute_query("DELETE FROM order_items WHERE order_id=?", (self.order_id,))

        # Then, add current items from the menu_items list
        for item in self.menu_items:
            insert_item_query = 'INSERT INTO order_items (order_id, menu_item_id) VALUES (?, ?)'
            self.db_manager.execute_query(insert_item_query, (self.order_id, item.id))

    def delete_from_database(self):
        query = "DELETE FROM orders WHERE id=?"
        parameters = (self.order_id,)
        self.db_manager.execute_query(query, parameters)

    def update(self, user_id=None, branch_id=None):
        if user_id is not None:
            self.user_id = user_id
        if branch_id is not None:
            self.branch_id = branch_id

        query = "UPDATE orders SET user_id=?, branch_id=? WHERE id=?"
        parameters = (self.user_id, self.branch_id, self.order_id)
        self.db_manager.execute_query(query, parameters)
    def fetch_order_report_data(self):
        query = """
            SELECT COUNT(*), AVG(total_price), 
                   SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending,
                   SUM(CASE WHEN status = 'Preparing' THEN 1 ELSE 0 END) as preparing,
                   SUM(CASE WHEN status = 'Ready' THEN 1 ELSE 0 END) as ready,
                   SUM(CASE WHEN status = 'Served' THEN 1 ELSE 0 END) as served
            FROM orders;
        """
        self.db_manager.execute_query(query)
        return self.db_manager.cursor.fetchone()

class Discount:
    def __init__(self, discount_id, percentage, description, valid=True, db_manager=None):
        self.discount_id = discount_id
        self.percentage = percentage
        self.description = description
        self.valid = valid
        self.db_manager = db_manager

    def fetch_discount_details(self):
        # Fetch discount details from the database
        return self.db_manager.fetch_discount_details(self.discount_id)
    def get_discount_by_id(discount_id, db_manager):
        query = "SELECT * FROM discounts WHERE discount_id = ?"
        parameters = (discount_id,)
        result = db_manager.fetch_all(query, parameters)
        if result:
            discount_data = result[0]
            return Discount(discount_data[0], discount_data[1], discount_data[2], bool(discount_data[3]), db_manager)
        else:
            return None
    def apply_discount(self, amount):
        if self.valid:
            return amount * (self.percentage / 100)
        else:
            return 0

    def staff_discount(self):
        # Logic for staff discount
        pass

    def get_discount_id(self):
        return self.discount_id

    def get_percentage(self):
        return self.percentage

    def save_to_database(self):
        try:
            query = "INSERT INTO discounts (percentage, description, valid) VALUES (?, ?, ?)"
            parameters = (self.percentage, self.description, int(self.valid))
            self.db_manager.execute_query(query, parameters)
            self.db_manager.conn.commit()  # Commit the transaction
        except Exception as e:
            print(f"Error saving discount to database: {e}")

    def update(self, percentage, description, valid):
        self.percentage = percentage
        self.description = description
        self.valid = valid
        query = "UPDATE discounts SET percentage=?, description=?, valid=? WHERE discount_id=?"
        parameters = (self.percentage, self.description, self.valid, self.discount_id)
        self.db_manager.execute_query(query, parameters)

    def delete_from_database(self):
        query = "DELETE FROM discounts WHERE discount_id=?"
        parameters = (self.discount_id,)
        self.db_manager.execute_query(query, parameters)
class Payment:
    def __init__(self, order_id, invoice_id, db_manager):
        self.invoice_id = invoice_id
        self.order_id = order_id
        self.discount = None
        self.db_manager = db_manager
        self.total_price = self.fetch_total_price()  # Fetch the total price from the order
        self.final_price = self.calculate_final_price()  # Calculate the final price

    def fetch_total_price(self):
        # Fetch total price from the database
        return self.db_manager.fetch_order_total_price(self.order_id)

    def calculate_final_price(self):
        # Start with the total price of the order
        final_price = self.total_price
        # If there's a discount, apply it
        if self.discount:
            discount_amount = final_price * (self.discount.percentage / 100.0)
            final_price -= discount_amount
        # Round the final price to 2 decimal places
        return round(final_price, 2)

    def add_discount(self, discount):
        if not self.discount and discount.valid:
            self.discount = discount
            # Update total price after discount
            self.total_price -= discount.apply_discount(self.total_price)
            # Call save_to_database to update the database entry with the discount
            self.save_to_database()

    def remove_discount(self):
        self.discount = None
        # Recalculate total price as if no discount was applied
        self.save_to_database()  # Save the removal of discount to the database

    def has_discount(self):
        return self.discount is not None

    def get_discount(self):
        return self.discount

    def get_total_price(self):
        return self.total_price

    def print_invoice(self):
        # Implement invoice printing logic
        pass

    def process_payment(self):
        # Implement payment processing logic
        pass

    def make_payment(self):
        self.process_payment()

    def save_to_database(self):
        # Check if a payment record already exists for this order
        query = "SELECT * FROM payments WHERE order_id = ?"
        self.db_manager.execute_query(query, (self.order_id,))
        existing_record = self.db_manager.cursor.fetchone()

        if existing_record:
            # Update existing payment record
            update_query = '''
                UPDATE payments
                SET discount_id = ?, total_price = ?
                WHERE order_id = ?
            '''
            update_parameters = (self.discount.discount_id if self.discount else None,
                                 self.total_price, self.order_id)
            self.db_manager.execute_query(update_query, update_parameters)
        else:
            # Insert new payment record
            insert_query = '''
                INSERT INTO payments (order_id, discount_id, total_price)
                VALUES (?, ?, ?)
            '''
            insert_parameters = (self.order_id,
                                 self.discount.discount_id if self.discount else None,
                                 self.total_price)
            self.db_manager.execute_query(insert_query, insert_parameters)
class CashPayment(Payment):
    def make_payment(self):
        # Logic specific to cash payment
        super().make_payment()
        self.save_to_database()  # Save the payment details to the database

    def get_total_price(self):
        return self.total_price
    def save_to_database(self):
        # Save payment details to the database using INSERT
        query = '''
            INSERT INTO payments (order_id, discount_id, total_price)
            VALUES (?, ?, ?)
        '''
        parameters = (
            self.order_id,
            self.discount.discount_id if self.discount else None,
            self.final_price,
        )
        self.db_manager.execute_query(query, parameters)

class CreditCard(Payment):
    def __init__(self, order_id, invoice_id, name_on_card, db_manager):
        super().__init__(order_id, invoice_id, db_manager)
        self.name_on_card = name_on_card

    def make_payment(self):
        # Logic specific to credit card payment
        super().make_payment()
        self.save_to_database()  # Save the payment details to the database

    def get_total_price(self):
        return self.total_price

    def save_to_database(self):
        # Save credit card payment details to the database
        query = '''
            INSERT INTO credit_card_payments (order_id, name_on_card, amount_paid)
            VALUES (?, ?, ?)
        '''
        parameters = (self.order_id, self.name_on_card, self.final_price)
        self.db_manager.execute_query(query, parameters)

class Reservation:
    def __init__(self, reservation_id, date, table_number, branch_id, db_manager):
        self.reservation_id = reservation_id
        self.table_number = table_number
        self.date = date
        self.branch_id = branch_id
        self.db_manager = db_manager

    def check_capacity(self):
        # Implement logic to check if there is capacity for the reservation
        pass

    def get_date(self):
        return self.date

    def get_table_number(self):
        return self.table_number

    def save_to_database(self):
        query = '''
            INSERT INTO reservations (id, date, table_number, branch_id)
            VALUES (?, ?, ?, ?)
        '''
        parameters = (self.reservation_id, self.date, self.table_number, self.branch_id)
        self.db_manager.execute_query(query, parameters)

    def update(self, date, table_number, branch_id):
        self.date = date
        self.table_number = table_number
        self.branch_id = branch_id
        query = "UPDATE reservations SET date=?, table_number=?, branch_id=? WHERE id=?"
        parameters = (self.date, self.table_number, self.branch_id, self.reservation_id)
        self.db_manager.execute_query(query, parameters)

    def delete_from_database(self):
        query = "DELETE FROM reservations WHERE id=?"
        parameters = (self.reservation_id,)
        self.db_manager.execute_query(query, parameters)

    def get_reservation_id(reservation_id, db_manager):
        query = "SELECT * FROM reservations WHERE id = ?"
        parameters = (reservation_id,)
        result = db_manager.fetch_all(query, parameters)
        if result:
            reservation_data = result[0]
            return Reservation(reservation_data[0], reservation_data[1], reservation_data[2], reservation_data[3],
                               db_manager)
        else:
            return None

    def fetch_upcoming_reservations(self):
        query = "SELECT * FROM reservations WHERE date >= CURRENT_DATE;"
        self.db_manager.execute_query(query)
        return self.db_manager.cursor.fetchall()

    def fetch_reservation_frequency(self):
        query = """
           SELECT strftime('%Y-%m', date) AS month, COUNT(*) AS reservation_count
           FROM reservations
           WHERE date >= CURRENT_DATE
           GROUP BY strftime('%Y-%m', date);
           """
        self.db_manager.execute_query(query)
        return self.db_manager.cursor.fetchall()

    def fetch_average_party_size(self):
        query = "SELECT AVG(table_number) FROM reservations WHERE date >= CURRENT_DATE;"
        self.db_manager.execute_query(query)
        return self.db_manager.cursor.fetchone()[0]