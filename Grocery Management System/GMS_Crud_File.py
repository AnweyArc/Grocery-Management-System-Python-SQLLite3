import sqlite3

# Define the name of your SQLite database file
database_name = "your_database_name.db"

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

# Function to fetch all items from the database
def fetch_items():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM items")
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
    cursor.execute("SELECT id, quantity FROM items WHERE name=?", (item_name,))
    item = cursor.fetchone()
    if item:
        item_id, current_quantity = item
        new_quantity = current_quantity - sold_quantity
        if new_quantity >= 0:
            cursor.execute("UPDATE items SET quantity=? WHERE id=?", (new_quantity, item_id))
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
