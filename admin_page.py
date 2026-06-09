import tkinter as tk
from tkinter import ttk, Toplevel
from PIL import Image, ImageTk
import os

class AdminPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.state('zoomed')

        # Configure the main background
        self.root.configure(bg="white")

        # Create main container
        self.main_container = tk.Frame(self.root, bg="white")
        self.main_container.pack(expand=True, fill="both")

        # Load icons and store them as instance attributes
        self.user_icon = self.load_icon(".venv/Images/User Management-icon.png", (150, 100))
        self.bell_icon = self.load_icon(".venv/Images/Accountant Reminder-icon.png", (150, 100))
        self.activity_icon = self.load_icon(".venv/Images/System Activity Review-icon.png", (150, 100))

        self.init_dashboard()

    def init_dashboard(self):
        # Create a frame for vertical centering
        center_frame = tk.Frame(self.main_container, bg="white")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # User Management Section
        user_frame = tk.Frame(center_frame, bg="white", cursor="hand2")
        user_frame.pack(pady=20)
        self.create_button_with_icon(user_frame, self.user_icon, "USER MANAGEMENT", self.open_user_management)

        # Separator after User Management
        separator1 = tk.Frame(center_frame, height=20, width=3000, bg="#16A085")
        separator1.pack(pady=20)

        # Accountant Reminder Section
        accountant_frame = tk.Frame(center_frame, bg="white", cursor="hand2")
        accountant_frame.pack(pady=20)
        self.create_button_with_icon(accountant_frame, self.bell_icon, "ACCOUNTANT REMINDER", self.open_notifications)

        # Separator after Accountant Reminder
        separator2 = tk.Frame(center_frame, height=20, width=3000, bg="#16A085")
        separator2.pack(pady=20)

        # System Activity Review Section
        activity_frame = tk.Frame(center_frame, bg="white", cursor="hand2")
        activity_frame.pack(pady=20)
        self.create_button_with_icon(activity_frame, self.activity_icon, "SYSTEM ACTIVITY REVIEW", self.open_activity_review)

        # Separator after System Activity Review
        separator3 = tk.Frame(center_frame, height=20, width=3000, bg="#16A085")
        separator3.pack(pady=20)

    def load_icon(self, filename, size):
        try:
            image = Image.open(filename)
            image = image.resize(size, Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(image)
            return photo_image
        except FileNotFoundError:
            print(f"Error: Image file '{filename}' not found.")
            return None
        except Exception as e:
            print(f"Error loading image '{filename}': {e}")
            return None

    def create_button_with_icon(self, parent, icon, text, command):
        button_frame = tk.Frame(parent, bg="white")
        button_frame.pack(fill="x")

        if icon:  # Check if icon loaded successfully
            icon_label = tk.Label(button_frame, image=icon, bg="white")
            icon_label.image = icon  # Keep a reference!
            icon_label.pack(side="left", padx=10)

        label = tk.Label(
            button_frame,
            text=text,
            font=("Arial", 40, "bold"),
            fg="#E67E22",
            bg="white",
            cursor="hand2"
        )
        label.pack(side="left", padx=20)

        # Bind events
        for widget in [button_frame, label]:
            widget.bind("<Button-1>", lambda e: command())
            widget.bind("<Enter>", lambda e: self.on_enter(parent))
            widget.bind("<Leave>", lambda e: self.on_leave(parent))

        if icon:  # Also bind events to icon_label if it exists
            icon_label.bind("<Button-1>", lambda e: command())
            icon_label.bind("<Enter>", lambda e: self.on_enter(parent))
            icon_label.bind("<Leave>", lambda e: self.on_leave(parent))

    def on_enter(self, frame):
        """Handle mouse enter event"""
        for widget in frame.winfo_children():
            if isinstance(widget, (tk.Frame, tk.Label, tk.Canvas)):
                widget.configure(bg="#f0f0f0")
            for subwidget in widget.winfo_children():
                if isinstance(subwidget, (tk.Label, tk.Canvas)):
                    subwidget.configure(bg="#f0f0f0")

    def on_leave(self, frame):
        """Handle mouse leave event"""
        for widget in frame.winfo_children():
            if isinstance(widget, (tk.Frame, tk.Label, tk.Canvas)):
                widget.configure(bg="white")
            for subwidget in widget.winfo_children():
                if isinstance(subwidget, (tk.Label, tk.Canvas)):
                    subwidget.configure(bg="white")

    def open_user_management(self):
        """Open User Management window"""
        user_window = Toplevel(self.root)
        user_window.title("User Management")
        user_window.state('zoomed')
        try:
            from admin_user_management import UserManagement
            UserManagement(user_window)
        except ImportError:
            tk.Label(user_window, text="User Management module not found", font=("Arial", 14)).pack(pady=20)

    def open_activity_review(self):
        """Open System Activity Review window"""
        activity_window = Toplevel(self.root)
        activity_window.title("System Activity Review")
        activity_window.state('zoomed')
        try:
            from admin_system_activity_review import SystemActivityReview
            SystemActivityReview(activity_window)
        except ImportError:
            tk.Label(activity_window, text="System Activity Review module not found", font=("Arial", 14)).pack(pady=20)

    def open_notifications(self):
        """Open Notifications window"""
        notif_window = Toplevel(self.root)
        notif_window.title("Send Notification")
        notif_window.state('zoomed')
        try:
            from admin_sending_notification_to_accountant import NotificationSystem
            NotificationSystem(notif_window)
        except ImportError:
            tk.Label(notif_window, text="Notification System module not found", font=("Arial", 14)).pack(pady=20)

def main():
    root = tk.Tk()
    app = AdminPage(root)
    root.mainloop()

if __name__ == "__main__":
    main()