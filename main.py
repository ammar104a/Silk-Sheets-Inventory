import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from prettytable import PrettyTable

# Initialize Database
def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Update Inventory
def update_inventory(item, increment=True):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    
    # Check if the item exists in the database
    c.execute('SELECT id FROM inventory WHERE item_name = ?', (item,))
    item_exists = c.fetchone()

    if item_exists:
        if increment:
            # Update the quantity by increasing it
            c.execute('UPDATE inventory SET quantity = quantity + 1 WHERE item_name = ?', (item,))
        else:
            # Update the quantity by decreasing it
            c.execute('UPDATE inventory SET quantity = quantity - 1 WHERE item_name = ? AND quantity > 0', (item,))
    else:
        if increment:
            # Insert the new item since it doesn't exist
            c.execute('INSERT INTO inventory (item_name, quantity) VALUES (?, 1)', (item,))
    
    conn.commit()
    conn.close()


# Clear Inventory
def clear_inventory():
    response = messagebox.askyesno("Clear Inventory", "Are you sure you want to clear the entire inventory?")
    if response:
        conn = sqlite3.connect('inventory.db')
        c = conn.cursor()
        c.execute('DELETE FROM inventory')
        conn.commit()
        conn.close()
        messagebox.showinfo("Inventory Cleared", "The inventory has been cleared.")

# View Inventory
def view_inventory():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('SELECT item_name, quantity FROM inventory')
    items = c.fetchall()
    conn.close()

    table = PrettyTable(["Item Name", "Quantity"])
    for item in items:
        table.add_row(item)
    
    messagebox.showinfo("Inventory", table.get_string())

# Create Tkinter Window
def create_window():
    window = tk.Tk()
    window.title("Inventory Management")

    items = ["White Satin", "White Plain", "Black", "Silver", "Charcoal", "Green", "Navy", "White Pure", "Waffle"]
    
    # Dropdown Menu
    selected_item = tk.StringVar()
    drop_down = ttk.Combobox(window, textvariable=selected_item, values=items, state="readonly")
    drop_down.pack()

    # Add and Remove Buttons
    tk.Button(window, text="Add Selected Item", command=lambda: update_inventory(selected_item.get())).pack()
    tk.Button(window, text="Remove Selected Item", command=lambda: update_inventory(selected_item.get(), increment=False)).pack()

    # Add button to view inventory
    tk.Button(window, text="View Inventory", command=view_inventory).pack()

    # Clear database button
    tk.Button(window, text="Clear Inventory", command=clear_inventory).pack()

    # Close button
    tk.Button(window, text="Close", command=window.destroy).pack()

    window.mainloop()

# Main function
if __name__ == "__main__":
    init_db()
    create_window()
