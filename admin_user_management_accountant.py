import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter.constants import RIGHT


class UserManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Kindergarten Fee Management System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        # Password visibility state
        self.password_visible = False

        # Create the navigation bar
        self.create_navigation_bar()

        # Create the main content
        self.create_main_content()

        # Create the table
        self.create_table()

        # Create the buttons
        self.create_buttons()

    def create_navigation_bar(self):
        nav_frame = tk.Frame(self.root, bg="#f0f0f0")
        nav_frame.pack(fill="x")

        # Home button
        home_btn = tk.Button(nav_frame, text="Home", bg="#CD853F", fg="white",
                             font=("Arial", 12, "bold"), bd=2)
        home_btn.pack(side="left", padx=10, pady=5)

        # Parent and Accountant buttons
        parent_btn = tk.Button(nav_frame, text="Parent", bg='#d3d3d3', fg="black",
                               font=("Arial", 12), bd=2, width=30)
        parent_btn.place(relx=0.4, rely=0, anchor='n')

        accountant_btn = tk.Button(nav_frame, text="Accountant", bg='#f0f0f0', fg="black",
                                   font=("Arial", 12), bd=2, width=30)
        accountant_btn.place(relx=0.6, rely=0, anchor='n')

        # Logout button
        logout_btn = tk.Button(nav_frame, text="Logout", font=("Arial", 12), bg="#CD853F", fg="white", bd=2,
                            command=self.logout)
        logout_btn.pack(side=RIGHT, padx=10, pady=5)

    def create_main_content(self):
        # Title
        title_label = tk.Label(self.root, text="USER MANAGEMENT",
                               font=("Arial", 24, "bold"), bg="#f0f0f0",
                               fg="#CD853F")
        title_label.pack(pady=20)

        # Create input fields frame
        input_frame = tk.Frame(self.root, bg="#f0f0f0")
        input_frame.pack(pady=20)

        # Accountant ID
        tk.Label(input_frame, text="Accountant ID", font=("Arial", 12, "bold"),
                 bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5)
        self.accountant_id_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.accountant_id_entry.grid(row=0, column=1, padx=10, pady=5)

        # Password with show/hide toggle
        tk.Label(input_frame, text="Password", font=("Arial", 12, "bold"),
                 bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5)

        # Create a frame for password field and toggle button
        password_frame = tk.Frame(input_frame, bg="#f0f0f0")
        password_frame.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Password entry
        self.password_entry = tk.Entry(password_frame, font=("Arial", 12), show="*", width=20)
        self.password_entry.pack(side="left", expand=True, fill="x")

        # Toggle button
        self.toggle_btn = tk.Button(password_frame, text="👁", command=self.toggle_password,
                                    bg="#f0f0f0", bd=0, font=("Arial", 10))
        self.toggle_btn.pack(side="right", padx=(5, 0))

        # Name field
        tk.Label(input_frame, text="Name", font=("Arial", 12, "bold"),
                 bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.name_entry.grid(row=2, column=1, padx=10, pady=5)

        # Contact and Email
        tk.Label(input_frame, text="Contact", font=("Arial", 12, "bold"),
                 bg="#f0f0f0").grid(row=1, column=2, padx=10, pady=5)
        self.contact_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.contact_entry.grid(row=1, column=3, padx=10, pady=5)

        tk.Label(input_frame, text="Email", font=("Arial", 12, "bold"),
                 bg="#f0f0f0").grid(row=2, column=2, padx=10, pady=5)
        self.email_entry = tk.Entry(input_frame, font=("Arial", 12))
        self.email_entry.grid(row=2, column=3, padx=10, pady=5)

    def toggle_password(self):
        """Toggle password visibility"""
        self.password_visible = not self.password_visible
        self.password_entry.config(show="" if self.password_visible else "*")

    # Rest of the class implementation remains the same
    def create_table(self):
        # Create table frame
        table_frame = tk.Frame(self.root)
        table_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Create Treeview
        columns = ("Accountant ID", "Password", "Name", "Contact", "Email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill="both", expand=True)

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)

        # Create button
        create_btn = tk.Button(button_frame, text="Create", bg="#5F9EA0", fg="white",
                               font=("Arial", 12), width=10,
                               command=self.create_record)
        create_btn.pack(side="left", padx=10)

        # Update button
        update_btn = tk.Button(button_frame, text="Update", bg="#5F9EA0", fg="white",
                               font=("Arial", 12), width=10,
                               command=self.update_record)
        update_btn.pack(side="left", padx=10)

        # Remove button
        remove_btn = tk.Button(button_frame, text="Remove", bg="#5F9EA0", fg="white",
                               font=("Arial", 12), width=10,
                               command=self.remove_record)
        remove_btn.pack(side="left", padx=10)

    def item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.clear_entries()
            self.accountant_id_entry.insert(0, values[0])
            self.password_entry.insert(0, values[1])
            self.name_entry.insert(0, values[2])
            self.contact_entry.insert(0, values[3])
            self.email_entry.insert(0, values[4])

    def create_record(self):
        accountant_id = self.accountant_id_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()

        if not all([accountant_id, password, name, contact, email]):
            messagebox.showerror("Error", "All fields are required!")
            return

        self.tree.insert("", "end", values=(accountant_id, password, name, contact, email))
        self.clear_entries()

    def update_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to update!")
            return

        accountant_id = self.accountant_id_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()

        if not all([accountant_id, password, name, contact, email]):
            messagebox.showerror("Error", "All fields are required!")
            return

        self.tree.item(selected_item, values=(accountant_id, password, name, contact, email))
        self.clear_entries()

    def remove_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a record to remove!")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to remove this record?"):
            self.tree.delete(selected_item)
            self.clear_entries()

    def clear_entries(self):
        self.accountant_id_entry.delete(0, "end")
        self.password_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        self.contact_entry.delete(0, "end")
        self.email_entry.delete(0, "end")

    def logout(self):
        if messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?"):
            self.root.destroy()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementSystem(root)
    root.mainloop()