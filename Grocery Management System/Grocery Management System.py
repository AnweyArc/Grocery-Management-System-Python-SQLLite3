import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import GMS_Crud_File


# FUNCTIONALITIES ----------------------------------------------------------
# Functionality for adding items
def add_items():
    def add_new_item_to_database():
        item_name = new_item_name_entry.get()
        item_quantity = int(new_item_quantity_entry.get())
        item_price = float(new_item_price_entry.get())  # Get the item price
        GMS_Crud_File.add_item(item_name, item_quantity, item_price)  # Add new item to the database
        add_window.destroy()
        # Refresh the view by calling both view_items() and view_item_inventory() functions
        view_items()
        view_item_inventory()

    def add_existing_item_to_database():
        item_name = existing_item_name_entry.get()
        item_quantity = int(existing_item_quantity_entry.get())
        item = GMS_Crud_File.get_item_by_name(item_name)
        if item:
            current_quantity = item[2]
            new_quantity = current_quantity + item_quantity
            GMS_Crud_File.update_item_quantity(item_name, new_quantity)  # Update existing item quantity
            add_window.destroy()
            view_items()
        else:
            messagebox.showerror("Item Not Found", "The item does not exist in the database.")


    add_window = tk.Toplevel(root)
    add_window.title("Add Item")    

    new_item_frame = ttk.LabelFrame(add_window, text="Add New Item")
    new_item_frame.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    new_item_name_label = ttk.Label(new_item_frame, text="Item Name:")
    new_item_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    new_item_name_entry = ttk.Entry(new_item_frame)
    new_item_name_entry.grid(row=0, column=1, padx=10, pady=5)

    new_item_quantity_label = ttk.Label(new_item_frame, text="Item Quantity:")
    new_item_quantity_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    new_item_quantity_entry = ttk.Entry(new_item_frame)
    new_item_quantity_entry.grid(row=1, column=1, padx=10, pady=5)

    new_item_price_label = ttk.Label(new_item_frame, text="Price/Item:")  # Label for item price
    new_item_price_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    new_item_price_entry = ttk.Entry(new_item_frame)
    new_item_price_entry.grid(row=2, column=1, padx=10, pady=5)

    add_new_item_button = ttk.Button(new_item_frame, text="Add New Item", command=add_new_item_to_database)
    add_new_item_button.grid(row=3, column=0, columnspan=2, pady=10)

    existing_item_frame = ttk.LabelFrame(add_window, text="Add Existing Item")
    existing_item_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    existing_item_name_label = ttk.Label(existing_item_frame, text="Item Name:")
    existing_item_name_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
    existing_item_name_entry = ttk.Entry(existing_item_frame)
    existing_item_name_entry.grid(row=0, column=1, padx=10, pady=5)

    existing_item_quantity_label = ttk.Label(existing_item_frame, text="Item Quantity:")
    existing_item_quantity_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
    existing_item_quantity_entry = ttk.Entry(existing_item_frame)
    existing_item_quantity_entry.grid(row=1, column=1, padx=10, pady=5)

    add_existing_item_button = ttk.Button(existing_item_frame, text="Add Existing Item", command=add_existing_item_to_database)
    add_existing_item_button.grid(row=2, column=0, columnspan=2, pady=10)


# Functionality for selling items
def sell_items():
    if not GMS_Crud_File.fetch_items():
        messagebox.showinfo("No Items", "There are no items in the inventory!")
    else:
        def sell_from_database():
            selected_item = item_listbox.get(tk.ACTIVE)  # Get the selected item from the listbox
            if selected_item:
                item_name = selected_item
                sold_quantity = int(sold_quantity_entry.get())  # Get the quantity sold
                GMS_Crud_File.sell_item(item_name, sold_quantity)  # Assuming a function to update the quantity sold
                
                # Record the sold item in the sold items listbox
                sold_items_listbox.insert(tk.END, f"Sold {sold_quantity} Pieces of {item_name}")
                
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

        # Create a listbox to display sold items
        sold_items_listbox = tk.Listbox(sell_window, height=10, width=40)
        sold_items_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

def view_item_inventory():
    if not GMS_Crud_File.fetch_items():
        messagebox.showinfo("No Items", "There are no items in the inventory!")
    else:
        item_listbox.delete(0, tk.END)
        items = GMS_Crud_File.fetch_items()
        for item in items:
            item_listbox.insert(tk.END, f"Item Name: {item[1]} \tQuantity: {item[2]} \tPrice: {item[3]}")  # Include item price in the display


# Functionality for viewing items
def view_items():
    # Clear the listbox before updating
    item_listbox.delete(0, tk.END)
    
    # Fetch added items
    added_items = GMS_Crud_File.fetch_items()
    item_listbox.insert(tk.END, "Added Items:")
    for item in added_items:
        item_listbox.insert(tk.END, f"Item Name: {item[1]} \tQuantity: {item[2]} \tPrice: {item[3]}")  # Include item price in the display

# Functionality for viewing sold items
def view_sold_items():
    # Fetch sold items from the database
    sold_items = GMS_Crud_File.fetch_items()

    if sold_items:
        # Create a new window to display sold items
        sold_items_window = tk.Toplevel(root)
        sold_items_window.title("Sold Items")

        # Create a listbox to display sold items
        sold_items_listbox = tk.Listbox(sold_items_window, height=20, width=40)
        sold_items_listbox.pack(padx=20, pady=20)

        # Display sold items in the listbox
        for item in sold_items:
            sold_items_listbox.insert(tk.END, item)
    else:
        messagebox.showinfo("No Sold Items", "There are no sold items to display.")

# Functionality for editing an item
def edit_item():
    if not GMS_Crud_File.fetch_items():
        messagebox.showinfo("No Items", "There are no items in the inventory!")
    else:
        def apply_edit():
            selected_item = item_listbox.get(tk.ACTIVE)  # Get the selected item from the listbox
            new_name = edit_name_entry.get()
            new_quantity = int(edit_quantity_entry.get())
            new_price = float(edit_price_entry.get())
            if selected_item and new_name and new_quantity and new_price:
                item_id = selected_item.split(':')[0]  # Extract the item ID from the selected item string
                GMS_Crud_File.edit_item(int(item_id), new_name, new_quantity, new_price)

                edit_window.destroy()
                view_items()  # Refresh the view
            else:
                status_label.config(text="Please fill all fields.", foreground="red")

        def delete_item():
            selected_item = item_listbox.get(tk.ACTIVE)  # Get the selected item from the listbox
            if selected_item:
                item_id = selected_item.split(':')[0]  # Extract the item ID from the selected item string
                GMS_Crud_File.delete_item(int(item_id))  # Delete the selected item from the database
                edit_window.destroy()
                view_items()  # Refresh the view
            else:
                status_label.config(text="Please select an item to delete.", foreground="red")

        edit_window = tk.Toplevel(root)
        edit_window.title("Edit Item")

        item_label = ttk.Label(edit_window, text="Select Item to Edit:")
        item_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        item_listbox = tk.Listbox(edit_window, height=10, width=40)
        item_listbox.grid(row=0, column=1, padx=10, pady=5)
        items = GMS_Crud_File.fetch_items()
        for item in items:
            item_listbox.insert(tk.END, f"{item[0]}: {item[1]}")

        edit_name_label = ttk.Label(edit_window, text="Edit Name:")
        edit_name_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        edit_name_entry = ttk.Entry(edit_window)
        edit_name_entry.grid(row=1, column=1, padx=10, pady=5)

        edit_quantity_label = ttk.Label(edit_window, text="Edit Quantity:")
        edit_quantity_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        edit_quantity_entry = ttk.Entry(edit_window)
        edit_quantity_entry.grid(row=2, column=1, padx=10, pady=5)

        edit_price_label = ttk.Label(edit_window, text="Edit Price:")
        edit_price_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        edit_price_entry = ttk.Entry(edit_window)
        edit_price_entry.grid(row=3, column=1, padx=10, pady=5)

        apply_button = ttk.Button(edit_window, text="Apply Edit", command=apply_edit)
        apply_button.grid(row=4, column=0, pady=10)

        delete_button = ttk.Button(edit_window, text="Delete Item", command=delete_item)
        delete_button.grid(row=4, column=1, pady=10)

        status_label = ttk.Label(edit_window, text="", foreground="black")
        status_label.grid(row=5, column=0, columnspan=2)



# Functionality for clearing the entire database
def clear_database():
    GMS_Crud_File.clear_database()
    view_items()


# Functionality for clearing item inventory
def clear_item_inventory():
    # Call the function to clear only the items from the inventory
    GMS_Crud_File.clear_inventory()
    # Refresh the view to reflect the changes
    view_items()


# MAIN WINDOW / DESIGN ----------------------------------------------------------


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

# BUTTONS ----------------------------------------------------------

add_items_button = ttk.Button(frame_buttons, text="Add Item/s", command=add_items)
add_items_button.grid(row=0, column=0, sticky="ew", padx=20, pady=5)

sell_items_button = ttk.Button(frame_buttons, text="Sell Item/s", command=sell_items)
sell_items_button.grid(row=0, column=1, sticky="ew", padx=20, pady=5)

edit_item_button = ttk.Button(frame_buttons, text="Edit Item", command=edit_item)
edit_item_button.grid(row=2, column=0, sticky="ew", padx=20, pady=5)

view_items_button = ttk.Button(frame_buttons, text="View Database", command=view_items)
view_items_button.grid(row=2, column=1, sticky="ew", padx=20, pady=5)

view_sold_items_button = ttk.Button(frame_buttons, text="Sold Items", command=view_sold_items)
view_sold_items_button.grid(row=1, column=1, sticky="ew", padx=20, pady=5)

item_inventory_button = ttk.Button(frame_buttons, text="Item Inventory", command=view_item_inventory)
item_inventory_button.grid(row=1, column=0, sticky="ew", padx=20, pady=5)

clear_database_button = ttk.Button(frame_buttons, text="Clear Database", command=clear_database)
clear_database_button.grid(row=3, column=1, sticky="ew", padx=20, pady=5)

clear_inventory_button = ttk.Button(frame_buttons, text="Clear Inventory", command=clear_item_inventory)
clear_inventory_button.grid(row=3, column=0, sticky="ew", padx=20, pady=5)

# Create a listbox
item_listbox = tk.Listbox(root, height=20, width=40)
item_listbox.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)

# Set column weight to make the buttons take half the width of the window
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

# Run the application
root.mainloop()
