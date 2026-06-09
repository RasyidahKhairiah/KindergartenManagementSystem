from tkinter import *
from tkinter import ttk, messagebox
import sqlite3


class NotificationSystem:
    def __init__(self, root):
        self.root = root
        self.setup_database()
        self.create_interface()

    def setup_database(self):
        self.conn = sqlite3.connect('school_management.db')
        self.cursor = self.conn.cursor()

        # Create notification messages table
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accountant_messages (
            MessageID INTEGER PRIMARY KEY AUTOINCREMENT,
            Message TEXT NOT NULL,
            DateSent DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        self.conn.commit()

    def create_interface(self):
        # Main frame with header
        main_frame = Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=BOTH, expand=True)

        header = Frame(main_frame, bg="#f0f0f0")
        header.pack(fill=X, padx=20, pady=20)

        Label(header, text="Accountant Reminder", font=("Arial", 24, "bold"),
              fg="#E67E22").pack(pady=20)

        # Content frame for left and right sections
        content_frame = Frame(main_frame, bg="#f0f0f0")
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Left frame for input fields
        left_frame = Frame(content_frame, bg="white")
        left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        # Input fields section
        input_frame = Frame(left_frame, bg="white")
        input_frame.pack(padx=20, pady=20)

        # Labels and entries
        Label(input_frame, text="Accountant ID", bg="white").pack(anchor=W)
        self.accountant_id = Entry(input_frame, width=40)
        self.accountant_id.pack(pady=5)

        Label(input_frame, text="Name", bg="white").pack(anchor=W)
        self.name = Entry(input_frame, width=40)
        self.name.pack(pady=5)

        Label(input_frame, text="Email", bg="white").pack(anchor=W)
        self.email = Entry(input_frame, width=40)
        self.email.pack(pady=5)

        Label(input_frame, text="Message", bg="white").pack(anchor=W)
        self.message = Text(input_frame, width=30, height=4)
        self.message.pack(pady=5)

        # Buttons
        buttons_frame = Frame(input_frame, bg="white")
        buttons_frame.pack(pady=10)

        Button(buttons_frame, text="Create", command=self.create_message,
               bg="#5F9EA0", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(buttons_frame, text="Update", command=self.update_message,
               bg="#5F9EA0", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(buttons_frame, text="Remove", command=self.remove_message,
               bg="#5F9EA0", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(buttons_frame, text="Send", command=self.send_message,
               bg="#CD853F", fg="white", width=10).pack(side=LEFT, padx=5)
        Button(buttons_frame, text="Send All", command=self.send_all_messages,
               bg="#CD853F", fg="white", width=10).pack(side=LEFT, padx=5)

        # Message history
        Label(input_frame, text="Message History", bg="white",
              font=("Arial", 11, "bold")).pack(pady=10)
        self.create_message_tree(input_frame)

        # Right frame for accountant list
        right_frame = Frame(content_frame, bg="white")
        right_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        Label(right_frame, text="Accountant List", bg="white",
              font=("Arial", 11, "bold")).pack(pady=10)
        self.create_accountant_tree(right_frame)

    def create_message_tree(self, parent):
        cols = ("Message", "Date Sent")
        self.msg_tree = ttk.Treeview(parent, columns=cols, show="headings", height=6)

        for col in cols:
            self.msg_tree.heading(col, text=col)
            self.msg_tree.column(col, width=200)

        self.msg_tree.pack(fill=X, pady=5)
        self.msg_tree.bind('<<TreeviewSelect>>', self.message_selected)  # Add this line
        self.refresh_message_tree()

    def create_accountant_tree(self, parent):
        cols = ("ID", "Name", "Email")
        self.acc_tree = ttk.Treeview(parent, columns=cols, show="headings")

        for col in cols:
            self.acc_tree.heading(col, text=col)
            self.acc_tree.column(col, width=150)

        self.acc_tree.pack(fill=BOTH, expand=True)
        self.acc_tree.bind('<<TreeviewSelect>>', self.accountant_selected)

        self.load_accountants()

    def load_accountants(self):
        self.cursor.execute("SELECT AccountantID, AccountantName, AccountantEmail FROM accountants")
        for item in self.acc_tree.get_children():
            self.acc_tree.delete(item)

        for row in self.cursor.fetchall():
            self.acc_tree.insert('', 'end', values=row)

    def accountant_selected(self, event):
        selected = self.acc_tree.selection()
        if selected:
            values = self.acc_tree.item(selected[0])['values']
            self.accountant_id.delete(0, END)
            self.name.delete(0, END)
            self.email.delete(0, END)

            self.accountant_id.insert(0, values[0])
            self.name.insert(0, values[1])
            self.email.insert(0, values[2])

    def message_selected(self, event):
        selected = self.msg_tree.selection()
        if selected:
            values = self.msg_tree.item(selected[0])['values']
            # Clear existing message
            self.message.delete("1.0", END)
            # Insert selected message
            if values and values[0]:
                self.message.insert("1.0", values[0])

    def create_message(self):
        message = self.message.get("1.0", END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message", parent=self.root)
            return

        try:
            self.cursor.execute("INSERT INTO accountant_messages (Message) VALUES (?)",
                                (message,))
            self.conn.commit()
            self.refresh_message_tree()
            self.message.delete("1.0", END)
            messagebox.showinfo("Success", "Message created", parent=self.root)
            self.stay_on_page()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    def update_message(self):
        if not self.msg_tree.selection():
            messagebox.showerror("Error", "Select a message first", parent=self.root)
            return

        message = self.message.get("1.0", END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message", parent=self.root)
            return

        selected = self.msg_tree.selection()[0]
        values = self.msg_tree.item(selected)['values']

        try:
            self.cursor.execute("UPDATE accountant_messages SET Message=? WHERE Message=?",
                                (message, values[0]))
            self.conn.commit()
            self.refresh_message_tree()
            self.message.delete("1.0", END)
            messagebox.showinfo("Success", "Message updated", parent=self.root)
            self.stay_on_page()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    def remove_message(self):
        if not self.msg_tree.selection():
            messagebox.showerror("Error", "Select a message first", parent=self.root)
            return

        try:
            selected = self.msg_tree.selection()[0]
            values = self.msg_tree.item(selected)['values']

            self.cursor.execute("DELETE FROM accountant_messages WHERE Message=?", (values[0],))
            self.conn.commit()
            self.refresh_message_tree()
            self.message.delete("1.0", END)
            messagebox.showinfo("Success", "Message removed", parent=self.root)
            self.stay_on_page()
        except Exception as e:
            messagebox.showerror("Error", str(e), parent=self.root)

    def send_message(self):
        if not self.acc_tree.selection():
            messagebox.showerror("Error", "Select an accountant first", parent=self.root)
            return

        if not self.message.get("1.0", END).strip():
            messagebox.showerror("Error", "Please enter a message", parent=self.root)
            return

        messagebox.showinfo("Success", "Message sent to selected accountant", parent=self.root)
        self.stay_on_page()

    def send_all_messages(self):
        message = self.message.get("1.0", END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message", parent=self.root)
            return

        messagebox.showinfo("Success", "Message sent to all accountants", parent=self.root)
        self.message.delete("1.0", END)
        self.stay_on_page()

    def refresh_message_tree(self):
        for item in self.msg_tree.get_children():
            self.msg_tree.delete(item)

        self.cursor.execute("SELECT Message, DateSent FROM accountant_messages")
        for row in self.cursor.fetchall():
            self.msg_tree.insert('', 'end', values=row)

    def stay_on_page(self):
        self.root.update()
        self.root.deiconify()  # Ensures window stays visible
        self.root.lift()  # Brings window to front