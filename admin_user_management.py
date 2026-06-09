from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class ParentManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Kindergarten User Management")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        # Setup database
        self.setup_database()

        # Create main interface
        self.create_main_interface()

    def setup_database(self):
        self.conn = sqlite3.connect('kindergarten.db')
        self.cursor = self.conn.cursor()

        # Drop existing tables if they exist
        self.cursor.execute('DROP TABLE IF EXISTS parents')
        self.cursor.execute('DROP TABLE IF EXISTS children')

        # Create parent table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS parents (
            ParentID VARCHAR(10) PRIMARY KEY,
            Password VARCHAR(50),
            ParentName VARCHAR(50),
            NumChildren INTEGER,
            Contact VARCHAR(15),
            Email VARCHAR(50)
        )''')

        # Create children table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS children (
            ChildID VARCHAR(10) PRIMARY KEY,
            ParentID VARCHAR(10),
            ChildName VARCHAR(50),
            FOREIGN KEY (ParentID) REFERENCES parents(ParentID)
        )''')

        self.conn.commit()

    def create_main_interface(self):
        # Top Navigation Bar
        nav_frame = Frame(self.root, bg="#f0f0f0")
        nav_frame.pack(fill=X)

        # Navigation buttons
        home_btn = Button(nav_frame, text="Home", font=("Arial", 12), bg="#CD853F", fg="white", bd=2)
        home_btn.pack(side=LEFT, padx=10, pady=5)

        parent_btn = Button(nav_frame, text="Parent", font=("Arial", 12), bg='#f0f0f0', fg="black", bd=2, width=30)
        parent_btn.place(relx=0.4, rely=0, anchor='n')

        accountant_btn = Button(nav_frame, text="Accountant", font=("Arial", 12), bg='#d3d3d3', fg="black", bd=2,
                                width=30)
        accountant_btn.place(relx=0.6, rely=0, anchor='n')

        logout_btn = Button(nav_frame, text="Logout", font=("Arial", 12), bg="#CD853F", fg="white", bd=2,
                            command=self.logout)
        logout_btn.pack(side=RIGHT, padx=10, pady=5)

        # Title
        title_label = Label(self.root, text="USER MANAGEMENT", font=("Arial", 20, "bold"), fg="#E67E22")
        title_label.pack(pady=20)

        # Main Content Frame
        content_frame = Frame(self.root, bg="#f0f0f0")
        content_frame.pack(fill=BOTH, expand=True, padx=20)

        # Left Frame for Input Fields
        input_frame = Frame(content_frame, bg="#f0f0f0")
        input_frame.pack(side=LEFT, fill=Y, padx=(0, 20))

        # Input Fields
        self.entries = {}

        # Parent ID Field
        Label(input_frame, text="Parent ID", font=("Arial", 11), bg="#f0f0f0").pack(anchor=W)
        self.entries["ParentID"] = Entry(input_frame, width=38)
        self.entries["ParentID"].pack(pady=(0, 5))

        # Password Field with Show/Hide Toggle
        Label(input_frame, text="Password", font=("Arial", 11), bg="#f0f0f0").pack(anchor=W)
        password_frame = Frame(input_frame, bg="#f0f0f0")
        password_frame.pack(fill=X, pady=(0, 5))

        self.entries["Password"] = Entry(password_frame, width=35, show="*")
        self.entries["Password"].pack(side=LEFT)

        self.password_visible = False
        self.toggle_btn = Button(password_frame, text="👁", command=self.toggle_password,
                                 bg="#f0f0f0", bd=0, font=("Arial", 10))
        self.toggle_btn.pack(side=LEFT, padx=(5, 0))

        # Other fields
        remaining_fields = [
            ("Name", "ParentName"),
            ("No. of children", "NumChildren"),
            ("Child ID", "ChildID"),
            ("Child Name", "ChildName"),
            ("Contact", "Contact"),
            ("Email", "Email")
        ]

        for label_text, key in remaining_fields:
            Label(input_frame, text=label_text, font=("Arial", 11), bg="#f0f0f0").pack(anchor=W)

            if key == "NumChildren":
                self.entries[key] = ttk.Combobox(input_frame, values=[1, 2], width=35, state='readonly')
            else:
                self.entries[key] = Entry(input_frame, width=38)
            self.entries[key].pack(pady=(0, 5))

        # Add space before buttons
        Frame(input_frame, height=20, bg="#f0f0f0").pack()

        # Buttons Frame
        btn_frame = Frame(input_frame, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        # Button style
        button_style = {
            "font": ("Arial", 11, "bold"),
            "width": 8,
            "bg": '#5f9ea0',
            "fg": "white",
            "bd": 1,
            "relief": "raised",
            "padx": 15,
            "pady": 5
        }

        # Action Buttons
        create_btn = Button(btn_frame, text="Create", command=lambda: self.handle_action("Create"), **button_style)
        create_btn.pack(side=LEFT, padx=10)

        update_btn = Button(btn_frame, text="Update", command=lambda: self.handle_action("Update"), **button_style)
        update_btn.pack(side=LEFT, padx=10)

        remove_btn = Button(btn_frame, text="Remove", command=lambda: self.handle_action("Remove"), **button_style)
        remove_btn.pack(side=LEFT, padx=10)

        # Right Frame for Table
        table_frame = Frame(content_frame)
        table_frame.pack(side=LEFT, fill=BOTH, expand=True)

        # Only the table structure needs to be modified
        columns = ("Parent ID", "Password", "Name", "No. of children", "Child ID", "Child Name", "Contact", "Email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)

        # Configure columns
        column_widths = {
            "Parent ID": 100,
            "Password": 100,
            "Name": 150,
            "No. of children": 100,
            "Child ID": 100,
            "Child Name": 150,
            "Contact": 100,
            "Email": 150
        }

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 150))

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient=VERTICAL, command=self.tree.yview)
        y_scroll.pack(side=RIGHT, fill=Y)

        x_scroll = ttk.Scrollbar(table_frame, orient=HORIZONTAL, command=self.tree.xview)
        x_scroll.pack(side=BOTTOM, fill=X)

        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)
        self.tree.pack(fill=BOTH, expand=True)

        # Bind select event
        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

        # Load initial data
        self.refresh_table()

        # Configure Treeview style
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def handle_action(self, action):
        if action == "Create":
            self.add_parent()
        elif action == "Update":
            self.edit_parent()
        elif action == "Remove":
            self.delete_parent()

    def toggle_password(self):
        self.password_visible = not self.password_visible
        self.entries["Password"].config(show="" if self.password_visible else "*")

    def refresh_table(self):
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            # Join parents and children tables to display all children
            self.cursor.execute("""
                SELECT p.ParentID, p.Password, p.ParentName, p.NumChildren, 
                       c.ChildID, c.ChildName, p.Contact, p.Email 
                FROM parents p
                LEFT JOIN children c ON p.ParentID = c.ParentID
                ORDER BY p.ParentID, c.ChildID
            """)

            for row in self.cursor.fetchall():
                self.tree.insert('', 'end', values=row)
        except sqlite3.OperationalError as e:
            messagebox.showerror("Database Error", f"Error refreshing table: {str(e)}")
            self.setup_database()

    def add_parent(self):
        # Get values from entries
        values = {k: v.get() for k, v in self.entries.items()}

        # Validate input
        if not all(values.values()):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            # Check if parent already exists
            self.cursor.execute("SELECT ParentID FROM parents WHERE ParentID = ?", (values['ParentID'],))
            existing_parent = self.cursor.fetchone()

            if existing_parent:
                # Parent exists, validate number of children
                self.cursor.execute("SELECT COUNT(*) FROM children WHERE ParentID = ?", (values['ParentID'],))
                current_children = self.cursor.fetchone()[0]
                max_children = int(values['NumChildren'])

                if current_children >= max_children:
                    messagebox.showerror("Error",
                                         f"Maximum number of children ({max_children}) already reached for this parent!")
                    return

                # Add only the child information
                self.cursor.execute("""
                    INSERT INTO children (ChildID, ParentID, ChildName)
                    VALUES (?, ?, ?)
                """, (values['ChildID'], values['ParentID'], values['ChildName']))
            else:
                # Insert new parent record
                self.cursor.execute("""
                    INSERT INTO parents (ParentID, Password, ParentName, NumChildren, Contact, Email)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (values['ParentID'], values['Password'], values['ParentName'],
                      values['NumChildren'], values['Contact'], values['Email']))

                # Insert child record
                self.cursor.execute("""
                    INSERT INTO children (ChildID, ParentID, ChildName)
                    VALUES (?, ?, ?)
                """, (values['ChildID'], values['ParentID'], values['ChildName']))

            self.conn.commit()
            self.refresh_table()

            # Clear only child-related entries
            self.entries['ChildID'].delete(0, END)
            self.entries['ChildName'].delete(0, END)

            messagebox.showinfo("Success", "Record added successfully!")

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Child ID already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def edit_parent(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a record to edit!")
            return

        values = {k: v.get() for k, v in self.entries.items()}

        try:
            # Update parent information
            self.cursor.execute("""
                UPDATE parents 
                SET Password=?, ParentName=?, NumChildren=?, Contact=?, Email=?
                WHERE ParentID=?
            """, (values['Password'], values['ParentName'], values['NumChildren'],
                  values['Contact'], values['Email'], values['ParentID']))

            # Update child information
            self.cursor.execute("""
                UPDATE children 
                SET ChildName=?
                WHERE ChildID=? AND ParentID=?
            """, (values['ChildName'], values['ChildID'], values['ParentID']))

            self.conn.commit()
            self.refresh_table()
            messagebox.showinfo("Success", "Information updated successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def delete_parent(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a record to delete!")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            try:
                values = self.tree.item(selected[0])['values']
                parent_id = values[0]
                child_id = values[4]  # Child ID is at index 4

                # Delete specific child
                if child_id:
                    self.cursor.execute("DELETE FROM children WHERE ChildID=? AND ParentID=?",
                                        (child_id, parent_id))

                    # Check if parent has any remaining children
                    self.cursor.execute("SELECT COUNT(*) FROM children WHERE ParentID=?", (parent_id,))
                    remaining_children = self.cursor.fetchone()[0]

                    # If no children remain, delete parent
                    if remaining_children == 0:
                        self.cursor.execute("DELETE FROM parents WHERE ParentID=?", (parent_id,))

                self.conn.commit()
                self.refresh_table()
                messagebox.showinfo("Success", "Record deleted successfully!")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def item_selected(self, event=None):
        selected = self.tree.selection()
        if not selected:
            return

        # Get selected item values
        values = self.tree.item(selected[0])['values']
        if not values:
            return

        # Clear current entries
        for entry in self.entries.values():
            if hasattr(entry, 'delete'):
                entry.delete(0, END)
            elif hasattr(entry, 'set'):
                entry.set('')

        # Fill entries with selected values
        fields = ["ParentID", "Password", "ParentName", "NumChildren", "ChildID", "ChildName", "Contact", "Email"]
        for field, value in zip(fields, values):
            if field in self.entries:
                if value is not None:  # Only set if value exists
                    if hasattr(self.entries[field], 'set'):
                        self.entries[field].set(str(value))
                    else:
                        self.entries[field].insert(0, str(value))

    def logout(self):
        if messagebox.askyesno("Logout Confirmation", "Are you sure you want to logout?"):
            self.root.destroy()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()



def main():
    root = Tk()
    app = ParentManagement(root)
    root.mainloop()


if __name__ == "__main__":
    main()