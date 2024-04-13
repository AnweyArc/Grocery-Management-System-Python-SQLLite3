import sqlite3

# Define the name of your SQLite database file
database_name = "grocery_database.db"

# Create the database table if it does not exist
def create_database():
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, price REAL)")
        connection.commit()
    except sqlite3.Error as e:
        print("Error creating database table:", e)
    finally:
        if connection:
            connection.close()

# Function to add an item to the database
def add_item(item_name, item_quantity, item_price):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)", (item_name, item_quantity, item_price))
        connection.commit()
    except sqlite3.Error as e:
        print("Error adding item to database:", e)
    finally:
        if connection:
            connection.close()

# Function to update the quantity of an existing item in the database
def update_item_quantity(item_name, new_quantity):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("UPDATE items SET quantity=? WHERE name=?", (new_quantity, item_name))
        connection.commit()
    except sqlite3.Error as e:
        print("Error updating item quantity:", e)
    finally:
        if connection:
            connection.close()

# Function to get an item by name from the database
def get_item_by_name(item_name):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items WHERE name=?", (item_name,))
        item = cursor.fetchone()
        return item
    except sqlite3.Error as e:
        print("Error fetching item from database:", e)
    finally:
        if connection:
            connection.close()

# Function to fetch all items from the database
def fetch_items():
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM items")
        items = cursor.fetchall()
        return items
    except sqlite3.Error as e:
        print("Error fetching items from database:", e)
    finally:
        if connection:
            connection.close()

# Function to delete an item from the database
def delete_item(item_id):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
        connection.commit()
    except sqlite3.Error as e:
        print("Error deleting item from database:", e)
    finally:
        if connection:
            connection.close()

# Function to clear the entire database
def clear_database():
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM items")
        connection.commit()
    except sqlite3.Error as e:
        print("Error clearing database:", e)
    finally:
        if connection:
            connection.close()

# Function to edit an item in the database
def edit_item(item_id, new_name, new_quantity, new_price):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("UPDATE items SET name=?, quantity=?, price=? WHERE id=?", (new_name, new_quantity, new_price, item_id))
        connection.commit()
    except sqlite3.Error as e:
        print("Error editing item:", e)
    finally:
        if connection:
            connection.close()

# Function to clear only the item inventory
def clear_inventory():
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("UPDATE items SET quantity=0")
        connection.commit()
    except sqlite3.Error as e:
        print("Error clearing inventory:", e)
    finally:
        if connection:
            connection.close()

# Function to fetch all sold items from the database
def fetch_sold_items():
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT name, quantity, price FROM sold_items")
        sold_items = cursor.fetchall()
        return sold_items
    except sqlite3.Error as e:
        print("Error fetching sold items:", e)
    finally:
        if connection:
            connection.close()

# Create the database table for sold items if it does not exist
def create_sold_items_table():
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS sold_items (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, price REAL)")
        connection.commit()
    except sqlite3.Error as e:
        print("Error creating sold_items table:", e)
    finally:
        if connection:
            connection.close()

# Function to add a sold item to the database
def add_sold_item(item_name, sold_quantity, price_per_item):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO sold_items (name, quantity, price) VALUES (?, ?, ?)", (item_name, sold_quantity, price_per_item))
        connection.commit()
    except sqlite3.Error as e:
        print("Error adding sold item to database:", e)
    finally:
        if connection:
            connection.close()

# Function to clear the sold items from the database
def clear_sold_items():
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM sold_items")
        connection.commit()
    except sqlite3.Error as e:
        print("Error clearing sold items:", e)
    finally:
        if connection:
            connection.close()

# Function to sell an item
def sell_item(item_name, sold_quantity):
    try:
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("SELECT quantity, price FROM items WHERE name=?", (item_name,))
        item = cursor.fetchone()
        if item:
            current_quantity, price_per_item = item
            if current_quantity >= sold_quantity:
                new_quantity = current_quantity - sold_quantity
                cursor.execute("UPDATE items SET quantity=? WHERE name=?", (new_quantity, item_name))
                connection.commit()
                # Add the sold item to the sold items table
                add_sold_item(item_name, sold_quantity, price_per_item)
            else:
                print("Error: Insufficient quantity to sell.")
        else:
            print("Error: Item not found in database.")
    except sqlite3.Error as e:
        print("Error selling item:", e)
    finally:
        if connection:
            connection.close()
