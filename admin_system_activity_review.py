from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime


class SystemActivityReview:
    def __init__(self, root):
        self.root = root
        self.root.title("System Activity Review")
        self.root.state('zoomed')

        # Setup database
        self.setup_database()

        # Create main frame
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=BOTH, expand=True)

        # Header frame
        header_frame = Frame(main_frame, bg="#f0f0f0", height=100)
        header_frame.pack(fill=X, padx=20, pady=20)

        # Title
        Label(header_frame,
              text="System Activity Review",
              font=("Arial", 24, "bold"),
              bg="#f0f0f0",
              fg="#E67E22").pack(side=LEFT, padx=430, pady=20)

        # Buttons frame
        button_frame = Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=X, padx=0)

        # Activity buttons
        Button(button_frame,
               text="See All Activity",
               command=self.show_all_activities,
               font=("Arial", 12),
               bg="#5F9EA0",
               fg="white",
               width=30).pack(side=LEFT, padx=300, pady=0)

        Button(button_frame,
               text="Filter Activity",
               command=self.filter_activities,
               font=("Arial", 12),
               bg="#5F9EA0",
               fg="white",
               width=30).pack(side=LEFT, padx=150, pady=0)

        # Create treeview
        self.create_activity_tree(main_frame)

    def setup_database(self):
        self.conn = sqlite3.connect('school_management.db')
        self.cursor = self.conn.cursor()

        # Create activity logs table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS activity_logs (
            LogID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID TEXT NOT NULL,
            Username TEXT NOT NULL,
            Action TEXT NOT NULL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        self.conn.commit()

    def create_activity_tree(self, parent):
        # Create frame for treeview
        tree_frame = Frame(parent)
        tree_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Create treeview
        self.tree = ttk.Treeview(tree_frame, columns=("User ID", "Name", "Last Activity", "Last Login"),
                                 show="headings")

        # Configure columns
        for col in ("User ID", "Name", "Last Activity", "Last Login"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        # Add scrollbars
        y_scroll = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        x_scroll = ttk.Scrollbar(tree_frame, orient=HORIZONTAL, command=self.tree.xview)

        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        # Pack scrollbars and tree
        y_scroll.pack(side=RIGHT, fill=Y)
        x_scroll.pack(side=BOTTOM, fill=X)
        self.tree.pack(fill=BOTH, expand=True)

        # Load initial data
        self.show_all_activities()

    def show_all_activities(self):
        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Fetch all activities
        self.cursor.execute('''
            SELECT UserID, Username, Action, MAX(Timestamp) 
            FROM activity_logs 
            GROUP BY UserID 
            ORDER BY Timestamp DESC
        ''')

        for row in self.cursor.fetchall():
            self.tree.insert('', 'end', values=row)

    def filter_activities(self):
        # Create filter window
        filter_window = Toplevel(self.root)
        filter_window.title("Filter Activities")
        filter_window.geometry("400x300")

        # Filter options
        Label(filter_window, text="Filter by:", font=("Arial", 12, "bold")).pack(pady=10)

        # User type filter
        Label(filter_window, text="User Type:").pack()
        user_type = ttk.Combobox(filter_window, values=["All", "Accountant", "Parent"])
        user_type.set("All")
        user_type.pack(pady=5)

        # Activity type filter
        Label(filter_window, text="Activity Type:").pack()
        activity_type = ttk.Combobox(filter_window, values=["All", "Login", "Logout", "Payment", "Fee Update"])
        activity_type.set("All")
        activity_type.pack(pady=5)

        # Apply filter button
        Button(filter_window,
               text="Apply Filter",
               command=lambda: self.apply_filter(user_type.get(), activity_type.get(), filter_window),
               bg="#5F9EA0",
               fg="white").pack(pady=20)

    def apply_filter(self, user_type, activity_type, window):
        # Build query based on filters
        query = "SELECT UserID, Username, Action, MAX(Timestamp) FROM activity_logs"
        conditions = []

        if user_type != "All":
            conditions.append(f"UserID LIKE '{user_type[:3].upper()}%'")

        if activity_type != "All":
            conditions.append(f"Action = '{activity_type}'")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY UserID ORDER BY Timestamp DESC"

        # Clear current items
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Execute filtered query
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            self.tree.insert('', 'end', values=row)

        window.destroy()

    def log_activity(self, user_id, username, action):
        """Log user activity - call this method from other parts of the application"""
        self.cursor.execute('''
            INSERT INTO activity_logs (UserID, Username, Action) 
            VALUES (?, ?, ?)
        ''', (user_id, username, action))
        self.conn.commit()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()