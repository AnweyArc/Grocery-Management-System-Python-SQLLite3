import tkinter as tk
from tkinter import ttk
import GMS_Crud_File

# Functionality for adding items
def add_items():
    def add_to_database():
        item_name = item_name_entry.get()
        item_quantity = int(item_quantity_entry.get())
        item_price = float(item_price_entry.get())  # Get the item price
        GMS_Crud_File.add_item(item_name, item_quantity, item_price)  # Pass the item price to the add_item function
        add_window.destroy()
        # Refresh the view by calling both view_items() and view_item_inventory() functions
        view_items()
        view_item_inventory()

    add_window = tk.Toplevel(root)
    add_window.title("Add Item")

    item_name_label = ttk.Label(add_window, text="Item Name:")
    item_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    item_name_entry = ttk.Entry(add_window)
    item_name_entry.grid(row=0, column=1, padx=10, pady=5)

    item_quantity_label = ttk.Label(add_window, text="Item Quantity:")
    item_quantity_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    item_quantity_entry = ttk.Entry(add_window)
    item_quantity_entry.grid(row=1, column=1, padx=10, pady=5)

    item_price_label = ttk.Label(add_window, text="Item Price:")  # Label for item price
    item_price_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    item_price_entry = ttk.Entry(add_window)
    item_price_entry.grid(row=2, column=1, padx=10, pady=5)

    add_button = ttk.Button(add_window, text="Add", command=add_to_database)
    add_button.grid(row=3, column=0, columnspan=2, pady=10)


# Functionality for selling items
def sell_items():
    def sell_from_database():
        selected_item = item_listbox.get(tk.ACTIVE)  # Get the selected item from the listbox
        if selected_item:
            item_name = selected_item
            sold_quantity = int(sold_quantity_entry.get())  # Get the quantity sold
            GMS_Crud_File.sell_item(item_name, sold_quantity)  # Assuming a function to update the quantity sold
            sell_window.destroy()
            view_items()  # Refresh the view
        else:
            status_label.config(text="Please select an item to sell.", foreground="red")

    sell_window = tk.Toplevel(root)
    sell_window.title("Sell Item")

    item_label = ttk.Label(sell_window, text="Select Item to Sell:")
    item_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

    item_listbox = tk.Listbox(sell_window, height=10, width=40)
    item_listbox.grid(row=0, column=1, padx=10, pady=5)
    items = GMS_Crud_File.fetch_items()
    for item in items:
        item_listbox.insert(tk.END, f"{item[1]}")

    sold_quantity_label = ttk.Label(sell_window, text="Quantity Sold:")
    sold_quantity_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    sold_quantity_entry = ttk.Entry(sell_window)
    sold_quantity_entry.grid(row=1, column=1, padx=10, pady=5)

    sell_button = ttk.Button(sell_window, text="Sell", command=sell_from_database)
    sell_button.grid(row=2, column=0, columnspan=2, pady=10)

    status_label = ttk.Label(sell_window, text="", foreground="black")
    status_label.grid(row=3, column=0, columnspan=2)

def view_item_inventory():
    # Clear the listbox before updating
    item_listbox.delete(0, tk.END)
    items = GMS_Crud_File.fetch_items()
    for item in items:
        item_listbox.insert(tk.END, f"Item Name: {item[1]} \tQuantity: {item[2]} \tPrice: {item[3]}")  # Include item price in the display


# Functionality for viewing items
def view_items():
    # Clear the listbox before updating
    item_listbox.delete(0, tk.END)
    items = GMS_Crud_File.fetch_items()
    for item in items:
        item_listbox.insert(tk.END, f"Item Name: {item[1]} \tQuantity: {item[2]} \tPrice: {item[3]}")  # Include item price in the display

# Functionality for viewing sold items
def view_sold_items():
    # Placeholder function for viewing sold items
    pass

# Functionality for deleting an item
def delete_item():
    def delete_from_database():
        search_item_name = search_entry.get()
        if search_item_name:
            items = GMS_Crud_File.fetch_items()
            item_found = False
            for item in items:
                if item[1] == search_item_name:
                    GMS_Crud_File.delete_item(item[0])
                    item_found = True
                    break
            if item_found:
                status_label.config(text=f"Item '{search_item_name}' deleted successfully.", foreground="green")
            else:
                status_label.config(text=f"Item '{search_item_name}' not found.", foreground="red")

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Item")

    search_label = ttk.Label(delete_window, text="Enter Item Name to Delete:")
    search_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    search_entry = ttk.Entry(delete_window)
    search_entry.grid(row=0, column=1, padx=10, pady=5)

    search_button = ttk.Button(delete_window, text="Delete", command=delete_from_database)
    search_button.grid(row=1, column=0, columnspan=2, pady=10)

    status_label = ttk.Label(delete_window, text="", foreground="black")
    status_label.grid(row=2, column=0, columnspan=2)


# Functionality for clearing the entire database
def clear_database():
    GMS_Crud_File.clear_database()
    view_items()

# Functionality for viewing item inventory
def view_item_inventory():
    # Placeholder function for viewing item inventory
    pass

# Functionality for clearing item inventory
def clear_item_inventory():
    # Placeholder function for clearing item inventory
    pass

# Create main window
root = tk.Tk()
root.title("Grocery Management System")

# Set window size to 800x600
root.geometry("800x600")

# Add background color
root.configure(bg="#008080")  # Updated background color

# Create header label
header_label = ttk.Label(root, text="Arcenas' Grocery", font=("Helvetica", 20), background="#008080", foreground="white")
header_label.grid(row=0, column=0, columnspan=2, pady=20)

# Create frame for buttons and listbox
frame_buttons = ttk.Frame(root)
frame_buttons.grid(row=1, column=0, sticky="ns")

# Configure style for the frame
style = ttk.Style()
style.configure("TFrame", background="#008080")

# Create buttons with some styling
button_style = ttk.Style()
button_style.configure('TButton', font=('Helvetica', 14), foreground="#4169e1", background="#4169e1", padding=10)

# Initialize database
GMS_Crud_File.create_database()

add_items_button = ttk.Button(frame_buttons, text="Add Item/s", command=add_items)
add_items_button.grid(row=0, column=0, sticky="ew", padx=20, pady=5)

sell_items_button = ttk.Button(frame_buttons, text="Sell Item/s", command=sell_items)
sell_items_button.grid(row=0, column=1, sticky="ew", padx=20, pady=5)

view_items_button = ttk.Button(frame_buttons, text="View Item/s", command=view_items)
view_items_button.grid(row=1, column=0, sticky="ew", padx=20, pady=5)

view_sold_items_button = ttk.Button(frame_buttons, text="Sold Items", command=view_sold_items)
view_sold_items_button.grid(row=1, column=1, sticky="ew", padx=20, pady=5)

delete_item_button = ttk.Button(frame_buttons, text="Delete Item", command=delete_item)
delete_item_button.grid(row=2, column=0, sticky="ew", padx=20, pady=5)

item_inventory_button = ttk.Button(frame_buttons, text="Item Inventory", command=view_item_inventory)
item_inventory_button.grid(row=2, column=1, sticky="ew", padx=20, pady=5)

clear_database_button = ttk.Button(frame_buttons, text="Clear Database", command=clear_database)
clear_database_button.grid(row=3, column=0, sticky="ew", padx=20, pady=5)

clear_inventory_button = ttk.Button(frame_buttons, text="Clear Inventory", command=clear_item_inventory)
clear_inventory_button.grid(row=3, column=1, sticky="ew", padx=20, pady=5)

# Create a listbox
item_listbox = tk.Listbox(root, height=20, width=40)
item_listbox.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

# Set column weight to make the buttons take half the width of the window
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

# Run the application
root.mainloop()
