import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


class UnifiedReminderSystem:
    def __init__(self, root, accountant_id, return_callback=None):
        self.root = root
        self.current_accountant_id = accountant_id
        self.return_callback = return_callback if return_callback else self.default_return
        self.root.configure(bg='#f0f0f0')

        # Set up database
        self.setup_database()

        # Create main interface
        self.setup_ui()

        # Load initial messages
        self.load_messages()

    def setup_database(self):
        self.conn = sqlite3.connect('kindergarten_management.db')
        self.cursor = self.conn.cursor()

    def setup_ui(self):
        # Main container
        self.main_container = tk.Frame(self.root, bg='#f0f0f0')
        self.main_container.pack(fill='both', expand=True)

        # Header
        header_frame = tk.Frame(self.main_container, bg='#5F9EA0')
        header_frame.pack(fill='x', padx=20, pady=20)

        # Display accountant name
        self.cursor.execute("SELECT AccountantName FROM accountants WHERE AccountantID = ?",
                            (self.current_accountant_id,))
        accountant_name = self.cursor.fetchone()[0]

        tk.Label(header_frame,
                 text=f"Welcome, {accountant_name}",
                 font=("Arial", 24, "bold"),
                 bg="#5F9EA0",
                 fg="white").pack(pady=10)

        tk.Label(header_frame,
                 text="Messages & Notifications",
                 font=("Arial", 20),
                 bg="#5F9EA0",
                 fg="white").pack(pady=10)

        # Content area
        content_frame = tk.Frame(self.main_container, bg='#f0f0f0')
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Messages section
        message_frame = tk.Frame(content_frame, bg='white')
        message_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Header with unread count
        header_container = tk.Frame(message_frame, bg='white')
        header_container.pack(fill='x', padx=10, pady=5)

        tk.Label(header_container,
                 text="Messages from Admin",
                 font=("Arial", 14, "bold"),
                 bg='white').pack(side='left')

        self.unread_label = tk.Label(header_container,
                                     text="Unread: 0",
                                     font=("Arial", 12),
                                     bg='white',
                                     fg='red')
        self.unread_label.pack(side='right')

        # Create messages treeview
        self.create_messages_tree(message_frame)

        # Buttons frame
        button_frame = tk.Frame(self.main_container, bg='#f0f0f0')
        button_frame.pack(fill='x', padx=20, pady=10)

        tk.Button(button_frame,
                  text="Mark as Read",
                  command=self.mark_selected_as_read,
                  bg='#5F9EA0',
                  fg='white',
                  font=('Arial', 10)).pack(side='left', padx=5)

        tk.Button(button_frame,
                  text="Return",
                  command=self.return_callback,
                  bg='#CD853F',
                  fg='white',
                  font=('Arial', 10)).pack(side='right', padx=5)

    def create_messages_tree(self, parent):
        # Create frame for treeview and scrollbar
        tree_frame = tk.Frame(parent)
        tree_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Create Treeview
        columns = ("Date", "Message", "Status")
        self.message_tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)

        # Configure columns
        self.message_tree.heading("Date", text="Date")
        self.message_tree.heading("Message", text="Message")
        self.message_tree.heading("Status", text="Status")

        self.message_tree.column("Date", width=150)
        self.message_tree.column("Message", width=500)
        self.message_tree.column("Status", width=100)

        # Add scrollbars
        y_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.message_tree.yview)
        x_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.message_tree.xview)

        self.message_tree.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

        # Grid layout
        self.message_tree.grid(row=0, column=0, sticky='nsew')
        y_scrollbar.grid(row=0, column=1, sticky='ns')
        x_scrollbar.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def load_messages(self):
        for item in self.message_tree.get_children():
            self.message_tree.delete(item)

        try:
            self.cursor.execute('''
                SELECT 
                    strftime('%Y-%m-%d %H:%M:%S', DateSent) as FormattedDate,
                    Message,
                    IsRead,
                    MessageID
                FROM unified_messages
                WHERE ReceiverID = ? 
                AND ReceiverType = 'accountant'
                ORDER BY DateSent DESC
            ''', (self.current_accountant_id,))

            messages = self.cursor.fetchall()
            unread_count = 0

            for date, message, is_read, message_id in messages:
                status = "Read" if is_read else "Unread"
                if not is_read:
                    unread_count += 1

                self.message_tree.insert('', 'end',
                    values=(date, message, status),
                    tags=(str(message_id), 'unread' if not is_read else 'read'))

            # Update unread count label
            self.unread_label.config(text=f"Unread: {unread_count}")

            # Configure tag appearances
            self.message_tree.tag_configure('unread', background='#FFE4E1')
            self.message_tree.tag_configure('read', background='white')

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load messages: {str(e)}")

    def mark_selected_as_read(self):
        selected_items = self.message_tree.selection()
        if not selected_items:
            messagebox.showinfo("Info", "Please select messages to mark as read")
            return

        try:
            for item in selected_items:
                # Get the message ID from the item's tags
                message_id = self.message_tree.item(item)['tags'][0]

                # Update the database
                self.cursor.execute('''
                    UPDATE unified_messages 
                    SET IsRead = 1 
                    WHERE MessageID = ? AND ReceiverID = ?
                ''', (message_id, self.current_accountant_id))

            self.conn.commit()
            self.load_messages()  # Refresh the display
            messagebox.showinfo("Success", "Selected messages marked as read")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to update message status: {str(e)}")

    def default_return(self):
        self.root.destroy()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = UnifiedReminderSystem(root)
    root.mainloop()