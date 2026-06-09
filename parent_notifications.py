from tkinter import *
from tkinter import ttk
import sqlite3
from datetime import datetime

class ParentNotifications:
    def __init__(self, root):
        self.root = root
        self.root.title("Notifications")
        self.root.state('zoomed')
        
        # Setup database
        self.setup_database()
        
        # Main frame
        self.main_frame = Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=BOTH, expand=True)
        
        # Header
        header = Frame(self.main_frame, bg="#5F9EA0", height=100)
        header.pack(fill=X, padx=20, pady=20)
        
        Label(header,
              text="Notifications",
              font=("Arial", 24, "bold"),
              bg="#5F9EA0",
              fg="white").pack(pady=20)

        # Create notification area
        self.create_notification_area()

    def setup_database(self):
        self.conn = sqlite3.connect('school_management.db')
        self.cursor = self.conn.cursor()

        # Create table if it doesn't exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS accountant_messages (
                NotificationID INTEGER PRIMARY KEY,
                Message TEXT,
                DateSent DATETIME,
                ReceiverID TEXT,
                ReadStatus INTEGER DEFAULT 0
            )
        """)
        self.conn.commit()

    def create_notification_area(self):
        # Create split view
        paned_window = ttk.PanedWindow(self.main_frame, orient=HORIZONTAL)
        paned_window.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Left frame - Notification list
        left_frame = Frame(paned_window)
        paned_window.add(left_frame, weight=1)

        # Create notification list
        self.create_notification_list(left_frame)

        # Right frame - Notification details
        right_frame = Frame(paned_window)
        paned_window.add(right_frame, weight=2)

        # Create notification details view
        self.create_notification_details(right_frame)

    def create_notification_list(self, parent):
        # Notification list container
        Label(parent, text="Notifications", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Create listbox for notifications
        self.notif_list = Listbox(parent, width=50, font=("Arial", 11))
        self.notif_list.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.notif_list.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.notif_list.configure(yscrollcommand=scrollbar.set)
        
        # Bind selection event
        self.notif_list.bind('<<ListboxSelect>>', self.show_notification_details)
        
        # Load notifications
        self.load_notifications()

    def create_notification_details(self, parent):
        # Details frame
        details_frame = LabelFrame(parent, text="Notification Details", font=("Arial", 12, "bold"))
        details_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)

        # Message display
        self.message_text = Text(details_frame, wrap=WORD, font=("Arial", 11), padx=10, pady=10)
        self.message_text.pack(fill=BOTH, expand=True, padx=5, pady=5)
        self.message_text.config(state=DISABLED)  # Make it read-only

    def load_notifications(self):
        # Clear existing items
        self.notif_list.delete(0, END)

        # First, let's check what columns actually exist in the table
        try:
            self.cursor.execute("PRAGMA table_info(accountant_messages)")
            columns = self.cursor.fetchall()
            print("Available columns:", [col[1] for col in columns])
        except Exception as e:
            print(f"Error checking table structure: {e}")

        # Then modify the query based on actual column names
        try:
            self.cursor.execute("""
                SELECT NotificationID, Message, DateSent  -- Changed from NotificationsID to NotificationID
                FROM accountant_messages
                WHERE ReceiverID = ?
                ORDER BY DateSent DESC""", ('P001',))

            notifications = self.cursor.fetchall()
            for notif in notifications:
                display_text = f"{notif[2]} - {notif[1][:50]}..."
                self.notif_list.insert(END, display_text)
                self.notif_list.itemconfig(END, {'notif_id': notif[0]})
        except Exception as e:
            print(f"Error loading notifications: {e}")

    def show_notification_details(self, event):
        selection = self.notif_list.curselection()

        if selection:
            index = selection[0]
            notif_id = self.notif_list.itemcget(index, 'notif_id')

            self.cursor.execute("""
                SELECT Message, DateSent 
                FROM accountant_messages 
                WHERE NotificationID = ?""", (notif_id,))  # Changed from NotificationsID to NotificationID

            notif = self.cursor.fetchone()
            if notif:
                self.message_text.config(state=NORMAL)
                self.message_text.delete(1.0, END)
                self.message_text.insert(END, f"Date: {notif[1]}\n\n")
                self.message_text.insert(END, f"Message:\n{notif[0]}")
                self.message_text.config(state=DISABLED)

    def mark_as_read(self, notif_id):
        try:
            self.cursor.execute("""
                UPDATE accountant_messages 
                SET ReadStatus = 1 
                WHERE NotificationsID = ?""", (notif_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error marking notification as read: {e}")

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = Tk()
    app = ParentNotifications(root)
    root.mainloop()

if __name__ == "__main__":
    main()