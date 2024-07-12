from MODEL import *


class RestaurantController:
    def __init__(self, db_name):
        self.db_manager = DatabaseManager(db_name)
        self.menu = Menu(1, self.db_manager)
        self.branches = []



    def create_menu_item(self, id, price, available, name, description, allergens, menu_id, category):
        menu_item = MenuItem(id, price, available, name, description, allergens, menu_id, category, self.db_manager)
        self.menu.add_menu_item(menu_item)
        # Add to inventory
        self.create_stock_item(menu_id, name, available, available // 2)

    def read_menu_item(self, menu_item_id):
        return self.menu.get_menu_item_id(menu_item_id)

    def list_all_menu_items(self):
        return self.menu.get_all_menu_items()

    def update_menu_item(self, item_id, name, price, available, description, allergens, category):
        menu_item = self.menu.get_menu_item_id(item_id)
        if menu_item:
            # Update the menu item details
            menu_item.update(price=price, available=available, name=name, description=description, allergens=allergens,category=category)

            # Update corresponding stock item in inventory
            # Assuming each menu item is linked to a unique stock item
            # and using menu_item.id as the stock_item_id for simplicity
            self.update_stock_item(menu_item.id, name, available)

    def delete_menu_item(self, menu_item_id):
        menu_item = self.menu.get_menu_item_id(menu_item_id)
        if menu_item:
            menu_item.delete_from_database()
        else:
            raise ValueError(f"Menu item with ID {menu_item_id} not found.")
        self.delete_stock_item(menu_item.id , 1)


    def create_user(self, username, password, role):
        # Hash the password for security
        #hashed_password = self.hash_password(password)
        query = "INSERT INTO restaurant_management (username, password, role) VALUES (?, ?, ?)"
        self.db_manager.execute_query(query, (username, password, role))
        self.db_manager.conn.commit()

    def update_user(self, user_id, username, password, role):
        #hashed_password = self.hash_password(password)
        query = "UPDATE restaurant_management SET username = ?, password = ?, role = ? WHERE id = ?"
        self.db_manager.execute_query(query, (username, password, role, user_id))
        self.db_manager.conn.commit()

    def delete_user(self, user_id):
        query = "DELETE FROM restaurant_management WHERE id = ?"
        self.db_manager.execute_query(query, (user_id,))
        self.db_manager.conn.commit()

    def list_users(self):
        query = "SELECT id, username, role FROM restaurant_management"
        self.db_manager.execute_query(query)
        return self.db_manager.cursor.fetchall()

    def authenticate_user(self, username, password):
        query = "SELECT role FROM restaurant_management WHERE username = ? AND password = ?"
        self.db_manager.execute_query(query, (username, password))
        user = self.db_manager.cursor.fetchone()

        if user:
            return user[0]  # This will return the role of the user
        else:
            return None  # This will be returned if no user is found



    def create_report(self, report_id, report_type, duration, branch_location, branch_id):
        report = Report(report_id, report_type, duration, branch_location, branch_id, self.db_manager)
        report.save_to_database()

    def read_report(self, report_id):
        return Report.get_report_id(report_id, self.db_manager)

    def update_report(self, report_id, report_type=None, duration=None, branch_location=None, branch_id=None):
        report = Report.get_report_id(report_id, self.db_manager)
        if report:
            report.update(report_type, duration, branch_location, branch_id)
            report.save_to_database()
        else:
            raise ValueError(f"Report with ID {report_id} not found.")

    def delete_report(self, report_id):
        report = Report.get_report_id(report_id, self.db_manager)
        if report:
            report.delete_from_database()
        else:
            raise ValueError(f"Report with ID {report_id} not found.")

    def read_event(self, event_id):
        # Fetch the event from the database and return it
        query = 'SELECT * FROM events WHERE event_id = ?'
        parameters = (event_id,)
        result = self.db_manager.fetch_all(query, parameters)
        if result:
            # Assuming the event tuple is structured as (event_id, event_name, event_date, event_type, branch_id)
            return Event(*result[0], self.db_manager)
        else:
            return None
    def create_event(self, event_id, event_name, event_date, event_type, branch_id):
        event = Event(event_id, event_name, event_date, event_type, branch_id, self.db_manager)
        event.save_to_database()

    def list_all_events(self):
        query = 'SELECT * FROM events'
        return self.db_manager.fetch_all(query)

    # Update the event details
    def update_event(self, event_id, event_name=None, event_date=None, event_type=None, branch_id=None):
        event = self.read_event(event_id)
        if event:
            event.update(event_name, event_date, event_type, branch_id)
        else:
            raise ValueError(f"Event with ID {event_id} not found.")

    # Delete an event
    def delete_event(self, event_id):
        event = self.read_event(event_id)
        if event:
            event.delete_from_database()

    def create_stock_item(self, branch_id, name, quantity, reorder_level):
        stock_item = StockItem(None, name, quantity, reorder_level, branch_id, self.db_manager)
        inventory = Inventory(branch_id, self.db_manager)
        inventory.create_stock_item(stock_item)

    def update_stock_item(self, stock_item_id, name=None, quantity=None, reorder_level=None, branch_id=None):
        inventory = Inventory(branch_id, self.db_manager)
        stock_item = inventory.get_stock_item_by_id(stock_item_id)
        if stock_item:
            stock_item.name = name if name is not None else stock_item.name
            stock_item.quantity = quantity if quantity is not None else stock_item.quantity
            stock_item.reorder_level = reorder_level if reorder_level is not None else stock_item.reorder_level
            inventory.update_stock_item(stock_item)
        else:
            raise ValueError(f"Stock Item with ID {stock_item_id} not found.")

    def delete_stock_item(self, stock_item_id, branch_id):
        inventory = Inventory(branch_id, self.db_manager)
        inventory.delete_stock_item(stock_item_id)

    def read_stock_item(self, stock_item_id, branch_id=None):
        inventory = Inventory(branch_id, self.db_manager)  # Ensure branch_id is correctly provided
        return inventory.get_stock_item_by_id(stock_item_id)
    def reorder_stock_item(self, stock_item_id):
        stock_item = self.read_stock_item(stock_item_id)
        if stock_item:
            new_quantity = stock_item.get_reorder_level()
            self.update_stock_item(stock_item_id, name=stock_item.name, quantity=new_quantity, reorder_level=stock_item.reorder_level)
        else:
            raise ValueError(f"Stock Item with ID {stock_item_id} not found.")

    def list_all_stock_items(self):
        query = "SELECT * FROM inventory_items"
        return self.db_manager.fetch_all(query)

    def list_all_orders(self):
        query = "SELECT * FROM orders"
        return self.db_manager.fetch_all(query)

    def create_order(self, order):
        order.calculate_total_price()
        order.save_to_database()

    def read_order(self, order_id):
        return Order.get_order_id(order_id, self.db_manager)

    def update_order(self, order_id, user_id=None, branch_id=None, new_menu_items=None, menu_items_to_remove=None):
        order = self.read_order(order_id)
        if order is None:
            raise ValueError(f"Order with ID {order_id} not found.")

        # Update order details if provided
        if user_id is not None:
            order.user_id = user_id
        if branch_id is not None:
            order.branch_id = branch_id

        # Add new menu items if provided
        if new_menu_items:
            for item_id in new_menu_items:
                menu_item = self.read_menu_item(int(item_id))
                if menu_item:
                    order.add_menu_item(menu_item)

        # Remove menu items if provided
        if menu_items_to_remove:
            for item_id in menu_items_to_remove:
                menu_item = self.read_menu_item(int(item_id))
                if menu_item:
                    order.remove_menu_item(menu_item)

        # Save the updated order to the database
        order.save_to_database()

    def mark_order_as_preparing(self, order_id):
        order = self.read_order(order_id)
        if order:
            order.mark_as_preparing()

    def mark_order_as_ready(self, order_id):
        order = self.read_order(order_id)
        if order:
            order.mark_as_ready()

    def handle_unavailable_item(self, order_id, menu_item_id):
        order = self.read_order(order_id)
        query = "UPDATE menu_items SET available = 0 WHERE id = ?"
        self.db_manager.execute_query(query, (menu_item_id,))
        self.db_manager.conn.commit()
        if order:
            menu_item = self.read_menu_item(menu_item_id)
            if menu_item:
                order.remove_menu_item(menu_item)

    def get_all_available_menu_items(self):
        query = "SELECT id, name FROM menu_items WHERE available >= 1"
        return self.db_manager.fetch_all(query)

    def replace_menu_item(self, order_id, old_item_id, new_item_id):
        order = self.read_order(order_id)
        if order:
            old_item = self.read_menu_item(old_item_id)
            new_item = self.read_menu_item(new_item_id)
            if old_item and new_item:
                order.remove_menu_item(old_item)
                order.add_menu_item(new_item)
                order.save_to_database()

    def get_menu_items_for_order(self, order_id):
        query = """
        SELECT oi.order_id, oi.menu_item_id, mi.name
        FROM order_items AS oi
        JOIN menu_items AS mi ON oi.menu_item_id = mi.id
        WHERE oi.order_id = ?;
        """
        self.db_manager.execute_query(query, (order_id,))
        return self.db_manager.cursor.fetchall()
    def add_menu_item(self, order_id, menu_item_id):
        order = self.read_order(order_id)
        if order:
            menu_item = self.read_menu_item(menu_item_id)
            order.add_menu_item(menu_item)

    def remove_menu_item(self, order_id, menu_item_id):
        order = self.read_order(order_id)
        if order:
            menu_item = self.read_menu_item(menu_item_id)
            order.remove_menu_item(menu_item)

    def delete_order(self, order_id):
        order = self.read_order(order_id)
        if order:
            order.delete_from_database()

    def list_all_discounts(self):
        query = "SELECT * FROM discounts"
        return self.db_manager.fetch_all(query)
    def create_discount(self, discount_id, percentage, description, valid=True):
        discount = Discount(discount_id, percentage, description, valid, self.db_manager)
        discount.save_to_database()

    def read_discount(self, discount_id):
        return Discount.get_discount_by_id(discount_id, self.db_manager)

    def update_discount(self, discount_id, percentage=None, description=None, valid=None):
        discount = self.read_discount(discount_id)
        if discount:
            discount.update(percentage, description, valid)
            discount.save_to_database()
        else:
            raise ValueError(f"Discount with ID {discount_id} not found.")

    def delete_discount(self, discount_id):
        discount = self.read_discount(discount_id)
        if discount:
            discount.delete_from_database()
        else:
            raise ValueError(f"Discount with ID {discount_id} not found.")


    def create_payment(self, order_id, invoice_id, payment_type, name_on_card=None):
        if payment_type == 'Cash':
            payment = CashPayment(order_id, invoice_id, self.db_manager)
        elif payment_type == 'CreditCard':
            payment = CreditCard(order_id, invoice_id, name_on_card, self.db_manager)
        else:
            raise ValueError("Invalid payment type")

        payment.make_payment()

    def list_all_reservations(self):
        query = "SELECT * FROM reservations"
        return self.db_manager.fetch_all(query)

    def create_reservation(self, reservation_id, date, table_number, branch_id):
        reservation = Reservation(reservation_id, date, table_number, branch_id, self.db_manager)
        reservation.save_to_database()

    def read_reservation(self, reservation_id):
        return Reservation.get_reservation_id(reservation_id, self.db_manager)

    def update_reservation(self, reservation_id, date, table_number, branch_id):
        reservation = self.read_reservation(reservation_id)
        if reservation:
            reservation.update(date, table_number, branch_id)
        else:
            raise ValueError(f"Reservation with ID {reservation_id} not found.")

    def delete_reservation(self, reservation_id):
        reservation = Reservation.get_reservation_id(reservation_id,self.db_manager)
        if reservation:
            reservation.delete_from_database()
        else:
            raise ValueError(f"Reservation with ID {reservation_id} not found.")

    def get_order_total_price(self, order_id):
        return self.db_manager.fetch_order_total_price(order_id)

    def get_discount_details(self, discount_id):
        return self.db_manager.fetch_discount_details(discount_id)

    def process_payment(self, order_id, payment_type, discount_id=None, name_on_card=None):
        order_details = self.fetch_order_details(order_id)
        print(f"Order details fetched for order_id {order_id}: {order_details}")  # Debug print

        if order_details:
            branch_id = order_details[2]  # Adjust the index according to your order details structure
            # Assuming order_details is a tuple and branch_id is the third element

            # Process the payment based on the payment type
            if payment_type == 'cash':
                payment = CashPayment(order_id, order_details[1], self.db_manager)  # Adjust indexes as needed
            elif payment_type == 'card':
                if not name_on_card:
                    raise ValueError("Name on card is required for credit card payments.")
                payment = CreditCard(order_id, order_details[1], name_on_card,self.db_manager)  # Adjust indexes as needed
            else:
                raise ValueError("Invalid payment type")

            # Add a discount if applicable
            if discount_id:
                discount_details = self.db_manager.fetch_discount_details(discount_id)
                if discount_details:
                    payment.add_discount(Discount(*discount_details))

            payment.make_payment()
            return payment.get_total_price()
        else:
            print(f"No details found for order_id {order_id}.")  # More informative debug print
            # Handle the case where order details are not found
            return "Order not found or missing details."  # Return an informative message

    def get_order_details(self, order_id):
        # Implement a method to fetch order details from the database
        # This is a placeholder for the actual database call
        query = "SELECT * FROM orders WHERE id = ?"
        result = self.db_manager.execute_query(query, (order_id,))
        return result.fetchone() if result else None

    def fetch_order_details(self, order_id):
        # Implement a method to fetch order details from the database
        query = "SELECT * FROM orders WHERE id = ?"
        self.db_manager.execute_query(query, (order_id,))
        return self.db_manager.cursor.fetchone()
    def apply_discount_to_order(self, order_id, discount_id):
        # Fetch the order and discount objects
        order = self.read_order(order_id)
        discount = self.read_discount(discount_id)

        if not order or not discount:
            raise ValueError("Order or Discount not found.")

        # Fetch the total price of the order from the database
        total_price = self.get_order_total_price(order_id)

        # Calculate the discounted price
        discounted_price = total_price * (1 - discount.percentage / 100.0)

        # Update the order's total price in the database
        self.update_order_total_price(order_id, discounted_price)

        # Optionally, save the discount applied to the order
        #self.save_discount_to_order(order_id, discount_id)

    def update_order_total_price(self, order_id, new_price):
        # Implement the logic to update the order's total price in the database
        query = "UPDATE orders SET total_price = ? WHERE id = ?"
        self.db_manager.execute_query(query, (new_price, order_id))
        self.db_manager.conn.commit()

    def get_categories(self):
        query = "SELECT DISTINCT category FROM menu_items"
        result = self.db_manager.fetch_all(query)
        categories = [row[0] for row in result if row[0] is not None]
        return categories

    def filter_menu_items_by_category(self, category):
        query = "SELECT * FROM menu_items WHERE category = ?"
        result = self.db_manager.fetch_all(query, (category,))
        menu_items = []
        for item in result:
            # Assuming the item tuple is structured as (id, price, available, name, description, allergens, menu_id, category)
            menu_items.append(MenuItem(*item, self.db_manager))
        return menu_items

    def generate_sales_report(self):
        report = Report(None, None, None, None, None, self.db_manager)  # Adjust parameters as needed
        return report.get_sales_report()

    def generate_current_stock_report(self, branch_id):
        inventory = Inventory(branch_id, self.db_manager)
        return inventory.get_current_stock_report()

    def generate_low_stock_report(self, branch_id):
        inventory = Inventory(branch_id, self.db_manager)
        return inventory.get_low_stock_report()

    def get_order_report_data(self):
        order_instance = Order(None, None, None, self.db_manager)  # Adjust the parameters as needed for your Order class
        return order_instance.fetch_order_report_data()
    def get_upcoming_reservations(self):
        reservation = Reservation(None, None, None, None, self.db_manager)
        return reservation.fetch_upcoming_reservations()

    def get_reservation_frequency(self):
        reservation = Reservation(None, None, None, None, self.db_manager)
        return reservation.fetch_reservation_frequency()

    def get_average_party_size(self):
        reservation = Reservation(None, None, None, None, self.db_manager)
        return reservation.fetch_average_party_size()

        #RESIT
    
    def get_branches(self):
        # Return the list of branches
        return self.branches

    def add_branch(self, location, name):
        # Add a new branch to the list
        branch_id = len(self.branches) + 1
        self.branches.append((branch_id, name, location))

    def remove_branch(self, branch_id):
        # Remove a branch by ID
        self.branches = [branch for branch in self.branches if branch[0] != branch_id]