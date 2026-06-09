from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from admin_page import AdminPage
from Homepage import AccountantDashboard
from parent_page import ParentPage
import hashlib
import sqlite3
import os


def login_page():
    def verify_login():
        username = username_entry.get()
        password = password_entry.get()

        # Check if it's admin login
        if username == "admin" and password == "admin":
            root.destroy()
            new_root = Tk()
            AdminPage(new_root)
            return

        # Hash the password for comparison
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Connect to database
        conn = sqlite3.connect('kindergarten_management.db')
        cursor = conn.cursor()

        # Create activity_logs table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS activity_logs (
            LogID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID TEXT NOT NULL,
            Username TEXT NOT NULL,
            Action TEXT NOT NULL,
            Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )''')
        conn.commit()

        try:
            # First check accountant credentials
            cursor.execute("""
                SELECT AccountantID, AccountantName 
                FROM accountants 
                WHERE AccountantID = ? AND AccountantPassword = ?
            """, (username, hashed_password))

            accountant = cursor.fetchone()

            if accountant:
                # Log successful accountant login
                cursor.execute("""
                    INSERT INTO activity_logs (UserID, Username, Action)
                    VALUES (?, ?, ?)
                """, (accountant[0], accountant[1], "Login"))
                conn.commit()

                # Close login window and open accountant dashboard
                root.destroy()
                new_root = Tk()
                AccountantDashboard(new_root, accountant[0])
                return

            # If not an accountant, check parent credentials
            cursor.execute("""
                SELECT ParentID, ParentName 
                FROM parents 
                WHERE ParentID = ? AND ParentPassword = ?
            """, (username, hashed_password))

            parent = cursor.fetchone()

            if parent:
                # Log successful parent login
                cursor.execute("""
                    INSERT INTO activity_logs (UserID, Username, Action)
                    VALUES (?, ?, ?)
                """, (parent[0], parent[1], "Parent Login"))
                conn.commit()

                # Close login window and open parent dashboard
                root.destroy()
                new_root = Tk()
                ParentPage(new_root)  # Open the parent dashboard
            else:
                messagebox.showerror("Error", "Invalid username or password.")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"An error occurred: {str(e)}")
        finally:
            conn.close()

    # Create the login window
    root = Tk()
    root.title("Login")
    root.state('zoomed')

    # Create main frame with white background
    main_frame = Frame(root, bg="white")
    main_frame.pack(fill=BOTH, expand=True)

    # Welcome text
    welcome_label = Label(main_frame,
                          text="WELCOME",
                          font=("Arial", 64, "bold"),
                          fg="#E67E22",
                          bg="white")
    welcome_label.pack(pady=(0, 10))

    # Subtitle
    subtitle_label = Label(main_frame,
                           text="Enter your credentials",
                           font=("Arial", 16),
                           bg="white")
    subtitle_label.pack(pady=(0, 40))

    # Create a frame for login elements
    login_frame = Frame(main_frame, bg="white")
    login_frame.pack(pady=20)

    # User ID field
    userid_label = Label(login_frame,
                         text="USER ID",
                         font=("Arial", 14),
                         bg="white")
    userid_label.grid(row=0, column=0, sticky='w', pady=10)

    username_entry = Entry(login_frame,
                           font=("Arial", 14),
                           width=30,
                           bd=2,
                           relief="groove")
    username_entry.grid(row=0, column=1, padx=30)

    # Password field
    password_label = Label(login_frame,
                           text="PASSWORD",
                           font=("Arial", 14),
                           bg="white")
    password_label.grid(row=1, column=0, sticky='w', pady=30)

    password_entry = Entry(login_frame,
                           show='*',
                           font=("Arial", 14),
                           width=30,
                           bd=2,
                           relief="groove")
    password_entry.grid(row=1, column=1, padx=30)

    # Login button
    login_button = Button(main_frame,
                          text="LOGIN",
                          command=verify_login,
                          font=("Arial", 14),
                          width=15,
                          bg="#5F9EA0",
                          fg="white",
                          relief="flat")
    login_button.pack(pady=0)

    # Create a frame for the images
    image_frame = Frame(main_frame, bg="white")
    image_frame.pack(side=BOTTOM, fill=X, pady=(0, 0))

    # Create a sub-frame to hold the two images horizontally
    images_container = Frame(image_frame, bg="white")
    images_container.pack()

    try:
        # Get the current directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, 'kindergartenLogIn.jpg')

        # Load and process the image once
        image = Image.open(image_path)

        # Image Size
        desired_width = 630
        desired_height = 275

        # Resize image to specific dimensions
        resized_image = image.resize((desired_width, desired_height), Image.Resampling.LANCZOS)

        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(resized_image)

        # Create and pack the first image label
        image_label1 = Label(images_container, image=photo, bg="white")
        image_label1.image = photo  # Keep a reference!
        image_label1.pack(side=LEFT, padx=10)

        # Create and pack the second image label (using the same photo)
        image_label2 = Label(images_container, image=photo, bg="white")
        image_label2.image = photo  # Keep a reference!
        image_label2.pack(side=LEFT, padx=5)

    except Exception as e:
        print(f"Error loading image: {e}")
        print(f"Current working directory: {os.getcwd()}")
        print(f"Files in directory: {os.listdir()}")

    root.mainloop()


if __name__ == "__main__":
    login_page()