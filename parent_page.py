from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class ParentPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Parent Dashboard")
        self.root.state('zoomed')

        # Database connection
        self.setup_database()

        # Main frame (gray background)
        self.main_frame = Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=BOTH, expand=True)

        # Header with cyan color
        self.create_header()

        # Button container 
        self.create_buttons()

    def setup_database(self):
        self.conn = sqlite3.connect('school_management.db')
        self.cursor = self.conn.cursor()

    def create_header(self):
        header = Frame(self.main_frame, bg="#5F9EA0", height=100)
        header.pack(fill=X, padx=20, pady=20)

        # Title
        title = Label(header,
                     text="Parent Dashboard",
                     font=("Arial", 24, "bold"),
                     bg="#5F9EA0",
                     fg="white")
        title.pack(side=LEFT, padx=20, pady=20)

        # Logout button
        logout_btn = Button(header,
                          text="Logout",
                          command=self.root.destroy,
                          font=("Arial", 12),
                          bg="white")
        logout_btn.pack(side=RIGHT, padx=20, pady=20)

    def create_buttons(self):
        # Center the buttons
        btn_frame = Frame(self.main_frame, bg="#f0f0f0")
        btn_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        try:
            # 1. Family Information Button
            profile_img = Image.open('profile.png')  # You'll need this icon
            profile_img = profile_img.resize((50, 50))
            self.profile_photo = ImageTk.PhotoImage(profile_img)

            profile_btn = Button(btn_frame,
                               text="Family Information",
                               image=self.profile_photo,
                               compound=TOP,
                               font=("Arial", 12),
                               width=200,
                               height=150,
                               command=self.open_family_info)
            profile_btn.pack(pady=10)

            # 2. Fee Payment Button
            payment_img = Image.open('payment.png')  # You'll need this icon
            payment_img = payment_img.resize((50, 50))
            self.payment_photo = ImageTk.PhotoImage(payment_img)

            payment_btn = Button(btn_frame,
                               text="Fee Payment",
                               image=self.payment_photo,
                               compound=TOP,
                               font=("Arial", 12),
                               width=200,
                               height=150,
                               command=self.open_fee_payment)
            payment_btn.pack(pady=10)

            # 3. Notifications Button
            notif_img = Image.open('notification.png')  # You'll need this icon
            notif_img = notif_img.resize((50, 50))
            self.notif_photo = ImageTk.PhotoImage(notif_img)

            notif_btn = Button(btn_frame,
                             text="Notifications",
                             image=self.notif_photo,
                             compound=TOP,
                             font=("Arial", 12),
                             width=200,
                             height=150,
                             command=self.open_notifications)
            notif_btn.pack(pady=10)

        except Exception as e:
            print(f"Error loading images: {e}")

    def open_family_info(self):
        family_window = Toplevel(self.root)
        family_window.title("Family Information")
        family_window.state('zoomed')
        
        from parent_family_info import FamilyInformation
        FamilyInformation(family_window)

    def open_fee_payment(self):
        payment_window = Toplevel(self.root)
        payment_window.title("Fee Payment")
        payment_window.state('zoomed')
        
        from parent_fee_payment import FeePayment
        FeePayment(payment_window)

    def open_notifications(self):
        notif_window = Toplevel(self.root)
        notif_window.title("Notifications")
        notif_window.state('zoomed')
        
        from parent_notifications import ParentNotifications
        ParentNotifications(notif_window)

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    root = Tk()
    app = ParentPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()