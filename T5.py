import tkinter as tk
from tkinter import messagebox
import sqlite3

# Connect to SQLite database (creates a new database if not exists)
conn = sqlite3.connect('visitor_management.db')
cursor = conn.cursor()

# Create a table for visitors
cursor.execute('''
    CREATE TABLE IF NOT EXISTS visitors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        phone TEXT NOT NULL,
        datetime TEXT NOT NULL,
        offices TEXT NOT NULL
    )
''')
conn.commit()

class VisitorManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Visitor Management System")
        self.root.geometry("400x300")

        self.font_size = 24

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Visitor Management System", font=("Helvetica", self.font_size + 4))
        title_label.pack(pady=10)

        add_button = tk.Button(self.root, text="Add Visitor", command=self.add_visitor, font=("Helvetica", self.font_size))
        add_button.pack(pady=10)

        view_button = tk.Button(self.root, text="View Visitors", command=self.view_visitors, font=("Helvetica", self.font_size))
        view_button.pack(pady=10)

        exit_button = tk.Button(self.root, text="Exit", command=self.root.destroy, font=("Helvetica", self.font_size))
        exit_button.pack(pady=10)

    def add_visitor(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Visitor")
        add_window.geometry("300x200")

        name_label = tk.Label(add_window, text="Visitor's Name:", font=("Helvetica", self.font_size))
        name_label.pack(pady=5)

        name_entry = tk.Entry(add_window, font=("Helvetica", self.font_size))
        name_entry.pack(pady=5)

        phone_label = tk.Label(add_window, text="Phone Number:", font=("Helvetica", self.font_size))
        phone_label.pack(pady=5)

        phone_entry = tk.Entry(add_window, font=("Helvetica", self.font_size))
        phone_entry.pack(pady=5)

        datetime_label = tk.Label(add_window, text="In-time and Date (YYYY-MM-DD HH:MM):", font=("Helvetica", self.font_size))
        datetime_label.pack(pady=5)

        datetime_entry = tk.Entry(add_window, font=("Helvetica", self.font_size))
        datetime_entry.pack(pady=5)

        offices_label = tk.Label(add_window, text="Offices Visited (comma-separated):", font=("Helvetica", self.font_size))
        offices_label.pack(pady=5)

        offices_entry = tk.Entry(add_window, font=("Helvetica", self.font_size))
        offices_entry.pack(pady=5)

        submit_button = tk.Button(add_window, text="Submit", command=lambda: self.submit_visitor(name_entry.get(), phone_entry.get(), datetime_entry.get(), offices_entry.get(), add_window), font=("Helvetica", self.font_size))
        submit_button.pack(pady=10)

    def submit_visitor(self, name, phone, datetime, offices, add_window):
        try:
            cursor.execute('''
                INSERT INTO visitors (name, phone, datetime, offices) VALUES (?, ?, ?, ?)
            ''', (name, phone, datetime, offices))
            conn.commit()
            messagebox.showinfo("Success", "Visitor added successfully!")
            add_window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to add visitor. Error: {e}")

    def view_visitors(self):
        view_window = tk.Toplevel(self.root)
        view_window.title("View Visitors")
        view_window.geometry("600x400")

        cursor.execute('SELECT * FROM visitors')
        visitors = cursor.fetchall()

        if not visitors:
            no_visitors_label = tk.Label(view_window, text="No visitors found.", font=("Helvetica", self.font_size))
            no_visitors_label.pack(pady=10)
        else:
            for visitor in visitors:
                visitor_info = f"ID: {visitor[0]}, Name: {visitor[1]}, Phone: {visitor[2]}, In-time and Date: {visitor[3]}, Offices: {visitor[4]}"
                visitor_label = tk.Label(view_window, text=visitor_info, font=("Helvetica", self.font_size))
                visitor_label.pack(pady=5)

                delete_button = tk.Button(view_window, text="Delete", command=lambda v=visitor[0]: self.delete_visitor(v), font=("Helvetica", self.font_size))
                delete_button.pack(pady=5)

    def delete_visitor(self, visitor_id):
        try:
            cursor.execute('DELETE FROM visitors WHERE id = ?', (visitor_id,))
            conn.commit()
            messagebox.showinfo("Success", "Visitor deleted successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to delete visitor. Error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VisitorManagementApp(root)
    root.mainloop()
