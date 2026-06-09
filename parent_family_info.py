from tkinter import *
from tkinter import ttk
import sqlite3
from PIL import Image, ImageTk

class FamilyInformation:
    def __init__(self, root):
        self.root = root
        self.root.title("Family Information")
        self.root.state('zoomed')
        self.root.configure(bg='white')

        # Setup database
        self.setup_database()

        # Create main container
        self.main_frame = Frame(self.root, bg='white')
        self.main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        # Navigation bar
        self.setup_navigation()

        # Header
        Label(self.main_frame,
              text="FAMILY INFORMATION",
              font=('Arial', 24, 'bold'),
              bg='white',
              fg='#5F9EA0').pack(pady=20)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Create tabs
        self.create_tabs()

        # Footer
        self.setup_footer()

    def setup_navigation(self):
        nav_frame = Frame(self.main_frame, bg='white')
        nav_frame.pack(fill=X, pady=(0, 20))

        # Home Button
        Button(nav_frame,
               text="Home",
               bg='#5F9EA0',
               fg='white',
               font=('Arial', 12, 'bold'),
               width=10,
               command=self.go_home).pack(side=LEFT, padx=5)

        # Logout Button
        Button(nav_frame,
               text="Logout",
               bg='#5F9EA0',
               fg='white',
               font=('Arial', 12, 'bold'),
               width=10,
               command=self.logout).pack(side=RIGHT, padx=5)

    def create_tabs(self):
        # Parent Profile Tab
        self.parent_frame = Frame(self.notebook, bg='white')
        self.notebook.add(self.parent_frame, text="Parent Profile")
        self.create_parent_profile()

        # Child Profile Tab
        self.child_frame = Frame(self.notebook, bg='white')
        self.notebook.add(self.child_frame, text="Child Profile")
        self.create_child_profile()

    def create_parent_profile(self):
        form_frame = Frame(self.parent_frame, bg='white')
        form_frame.pack(padx=50, pady=20)

        # Parent Details Entry Fields
        entries = [
            ("Parent ID", "parent_id"),
            ("Name", "name"),
            ("Contact", "contact"),
            ("Email", "email")
        ]

        for label_text, attr_name in entries:
            row_frame = Frame(form_frame, bg='white')
            row_frame.pack(fill=X, pady=5)

            label = Label(row_frame,
                         text=label_text,
                         font=('Arial', 12, 'bold'),
                         bg='white',
                         width=15,
                         anchor='w')
            label.pack(side=LEFT, padx=(0, 10))

            entry = Entry(row_frame,
                         font=('Arial', 11),
                         width=40,
                         state='readonly')
            entry.pack(side=LEFT, expand=True, fill=X)
            setattr(self, f"{attr_name}_entry", entry)

        # Load parent data
        self.load_parent_data()

    def create_child_profile(self):
        form_frame = Frame(self.child_frame, bg='white')
        form_frame.pack(padx=50, pady=20)

        # Student Selection
        select_frame = Frame(form_frame, bg='white')
        select_frame.pack(fill=X, pady=10)

        Label(select_frame,
              text="Select Student ID:",
              font=('Arial', 12, 'bold'),
              bg='white').pack(side=LEFT, padx=5)

        self.student_id_var = StringVar()
        self.student_combo = ttk.Combobox(select_frame,
                                         textvariable=self.student_id_var,
                                         state='readonly',
                                         font=('Arial', 11))
        self.student_combo.pack(side=LEFT, padx=5)
        self.student_combo.bind('<<ComboboxSelected>>', self.load_student_details)

        # Child Details
        entries = [
            ("Name", "student_name"),
            ("Class", "class"),
            ("Current Month's Fee", "current_fee"),
            ("Outstanding Fee", "outstanding_fee"),
            ("Payment Status", "payment_status")
        ]

        for label_text, attr_name in entries:
            row_frame = Frame(form_frame, bg='white')
            row_frame.pack(fill=X, pady=5)

            label = Label(row_frame,
                         text=label_text,
                         font=('Arial', 12, 'bold'),
                         bg='white',
                         width=15,
                         anchor='w')
            label.pack(side=LEFT, padx=(0, 10))

            entry = Entry(row_frame,
                         font=('Arial', 11),
                         width=40,
                         state='readonly')
            entry.pack(side=LEFT, expand=True, fill=X)
            setattr(self, f"{attr_name}_entry", entry)

        # Load student list
        self.load_student_list()

    def setup_footer(self):
        try:
            image = Image.open("kindergartenParent.jpg")
            desired_width = 1200
            desired_height = 270
            image = image.resize((desired_width, desired_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            footer_label = Label(self.main_frame, image=photo, bg='white')
            footer_label.image = photo
            footer_label.pack(side=BOTTOM, pady=(20, 0))
        except Exception as e:
            print(f"Could not load image: {e}")

    def setup_database(self):
        self.conn = sqlite3.connect('school_management.db')
        self.cursor = self.conn.cursor()

    def load_parent_data(self):
        self.cursor.execute("""
            SELECT ParentID, ParentName, ParentContact, ParentEmail 
            FROM parents 
            WHERE ParentID = ?""", ('P001',))

        result = self.cursor.fetchone()
        if result:
            entries = [self.parent_id_entry, self.name_entry,
                      self.contact_entry, self.email_entry]
            for entry, value in zip(entries, result):
                self.update_entry(entry, value)

    def load_student_list(self):
        self.cursor.execute("""
            SELECT StudentID, StudentName 
            FROM students 
            WHERE ParentID = ?""", ('P001',))

        students = self.cursor.fetchall()
        self.student_combo['values'] = [student[0] for student in students]

        if students:
            self.student_combo.set(self.student_combo['values'][0])
            self.load_student_details(None)

    def load_student_details(self, event):
        if self.student_id_var.get():
            student_id = self.student_id_var.get()

            self.cursor.execute("""
                SELECT s.StudentName, s.StudentClass,
                       f.Amount as CurrentFee,
                       COALESCE(SUM(CASE WHEN f.PaymentStatus = 'Pending' 
                                   THEN f.Amount ELSE 0 END), 0) as OutstandingFee,
                       f.PaymentStatus
                FROM students s
                LEFT JOIN Fee f ON s.StudentID = f.StudentID
                WHERE s.StudentID = ?
                GROUP BY s.StudentID""", (student_id,))

            result = self.cursor.fetchone()
            if result:
                entries = [self.student_name_entry, self.class_entry,
                          self.current_fee_entry, self.outstanding_fee_entry,
                          self.payment_status_entry]
                for entry, value in zip(entries, result):
                    if 'fee' in entry._name.lower():
                        value = f"RM {value:.2f}"
                    self.update_entry(entry, value)

    def update_entry(self, entry, value):
        entry.config(state='normal')
        entry.delete(0, END)
        entry.insert(0, str(value))
        entry.config(state='readonly')

    def go_home(self):
        pass  # Implement home navigation

    def logout(self):
        self.root.quit()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

if __name__ == "__main__":
    root = Tk()
    app = FamilyInformation(root)
    root.mainloop()