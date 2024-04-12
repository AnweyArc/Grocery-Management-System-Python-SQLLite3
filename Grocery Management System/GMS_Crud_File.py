import sqlite3

# Define the name of your SQLite database file
database_name = "grocery_database.db"

# Create the database table if it does not exist
def create_database():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, quantity INTEGER, price REAL)")
    connection.commit()
    connection.close()

# Function to add an item to the database
def add_item(item_name, item_quantity, item_price):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO items (name, quantity, price) VALUES (?, ?, ?)", (item_name, item_quantity, item_price))
    connection.commit()
    connection.close()

# Function to update the quantity of an existing item in the database
def update_item_quantity(item_name, new_quantity):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("UPDATE items SET quantity=? WHERE name=?", (new_quantity, item_name))
    connection.commit()
    connection.close()

# Function to get an item by name from the database
def get_item_by_name(item_name):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items WHERE name=?", (item_name,))
    item = cursor.fetchone()
    connection.close()
    return item

# Function to fetch all items from the database
def fetch_items():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")  # Fetch all items without excluding based on quantity
    items = cursor.fetchall()
    connection.close()
    return items

# Function to delete an item from the database
def delete_item(item_id):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    connection.commit()
    connection.close()

# Function to update the quantity of sold items
def sell_item(item_name, sold_quantity):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT id, quantity, price FROM items WHERE name=?", (item_name,))
    item = cursor.fetchone()
    if item:
        item_id, current_quantity, price = item
        if current_quantity >= sold_quantity:
            new_quantity = current_quantity - sold_quantity
            cursor.execute("UPDATE items SET quantity=? WHERE id=?", (new_quantity, item_id))
            # Add sold item to sold_items table
            cursor.execute("INSERT INTO sold_items (name, quantity, price) VALUES (?, ?, ?)", (item_name, sold_quantity, price))
            connection.commit()
        else:
            print("Error: Insufficient quantity to sell.")
    else:
        print("Error: Item not found in database.")
    connection.close()

# Function to clear the entire database
def clear_database():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM items")
    connection.commit()
    connection.close()

# Function to edit an item in the database
def edit_item(item_id, new_name, new_quantity, new_price):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("UPDATE items SET name=?, quantity=?, price=? WHERE id=?", (new_name, new_quantity, new_price, item_id))
    connection.commit()
    connection.close()
    
# Function to clear only the item inventory
def clear_inventory():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("UPDATE items SET quantity=0")  # Set quantity of all items to 0
    connection.commit()
    connection.close()
