from tkinter import *
from tkinter import ttk, messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk
from datetime import datetime


class FeePayment:
    def __init__(self, root, parent_id=None):
        self.root = root
        self.root.title("Fee Payment")
        self.root.state('zoomed')
        self.parent_id = parent_id or 'P001'  # Default parent ID if none provided

        # Setup database
        self.setup_database()

        # Main frame
        self.main_frame = Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=BOTH, expand=True)

        # Header
        header = Frame(self.main_frame, bg="#5F9EA0", height=100)
        header.pack(fill=X, padx=20, pady=20)

        Label(header,
              text="Fee Payment",
              font=("Arial", 24, "bold"),
              bg="#5F9EA0",
              fg="white").pack(pady=20)

        # Create payment form
        self.create_payment_form()

    def setup_database(self):
        self.conn = sqlite3.connect('kindergarten_management.db')
        self.cursor = self.conn.cursor()

        # Create Fee table if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS Fee (
            FeeID CHAR(5) PRIMARY KEY,
            StudentID CHAR(5),
            Amount DECIMAL(10,2),
            PaymentDate DATE,
            PaymentMethod VARCHAR(20),
            PaymentStatus VARCHAR(20),
            PaymentProof BLOB,
            FOREIGN KEY (StudentID) REFERENCES students(StudentID)
        )''')

        self.conn.commit()

    def create_payment_form(self):
        # Payment form frame
        form_frame = LabelFrame(self.main_frame, text="Payment Details", font=("Arial", 12, "bold"))
        form_frame.pack(padx=20, pady=10, fill=BOTH, expand=True)

        # Student Selection
        select_frame = Frame(form_frame)
        select_frame.pack(fill=X, padx=10, pady=5)

        Label(select_frame, text="Select Student:", font=("Arial", 11)).pack(side=LEFT)
        self.student_var = StringVar()
        self.student_combo = ttk.Combobox(select_frame, textvariable=self.student_var, state='readonly', width=40)
        self.student_combo.pack(side=LEFT, padx=5)
        self.student_combo.bind('<<ComboboxSelected>>', self.update_fee_details)

        # Fee Details Frame
        fee_frame = Frame(form_frame)
        fee_frame.pack(fill=X, padx=10, pady=10)

        # Total Fee
        Label(fee_frame, text="Total Fee (RM):", font=("Arial", 11)).grid(row=0, column=0, padx=5, pady=5)
        self.fee_label = Label(fee_frame, text="0.00", font=("Arial", 11))
        self.fee_label.grid(row=0, column=1, padx=5, pady=5)

        # Payment Method
        Label(fee_frame, text="Payment Method:", font=("Arial", 11)).grid(row=1, column=0, padx=5, pady=5)
        self.payment_method = StringVar()
        ttk.Radiobutton(fee_frame, text="Bank Transfer", variable=self.payment_method,
                        value="bank", command=self.show_payment_details).grid(row=1, column=1, padx=5, pady=5)
        ttk.Radiobutton(fee_frame, text="QR Payment", variable=self.payment_method,
                        value="qr", command=self.show_payment_details).grid(row=1, column=2, padx=5, pady=5)

        # Payment Details Frame
        self.payment_details_frame = Frame(form_frame)
        self.payment_details_frame.pack(fill=X, padx=10, pady=10)

        # Upload Proof Frame
        upload_frame = Frame(form_frame)
        upload_frame.pack(fill=X, padx=10, pady=10)

        Label(upload_frame, text="Upload Payment Proof:", font=("Arial", 11)).pack(side=LEFT)
        Button(upload_frame, text="Choose File", command=self.upload_proof,
               bg="#5F9EA0", fg="white", font=("Arial", 10)).pack(side=LEFT, padx=5)

        # Submit Button
        Button(form_frame, text="Submit Payment", command=self.submit_payment,
               bg="#5F9EA0", fg="white", font=("Arial", 11)).pack(pady=20)

        # Load student list
        self.load_students()

    def load_students(self):
        self.cursor.execute("""
            SELECT s.StudentID, s.StudentName 
            FROM students s
            WHERE s.ParentID = ?""", (self.parent_id,))

        students = self.cursor.fetchall()
        self.student_combo['values'] = [f"{student[0]} - {student[1]}" for student in students]

    def update_fee_details(self, event):
        if self.student_var.get():
            student_id = self.student_var.get().split(' - ')[0]

            # For demo purposes, set a fixed fee amount
            # In a real system, this would be fetched from a fee structure table
            self.fee_label.config(text="500.00")

    def show_payment_details(self):
        # Clear previous content
        for widget in self.payment_details_frame.winfo_children():
            widget.destroy()

        if not self.payment_method.get():
            return

        # Show content based on payment method
        if self.payment_method.get() == "bank":
            # Show bank details
            Label(self.payment_details_frame, text="Bank Details:", font=("Arial", 11, "bold")).pack(anchor=W)
            Label(self.payment_details_frame, text="Bank: CIMB").pack(anchor=W)
            Label(self.payment_details_frame, text="Account No: 1234567890").pack(anchor=W)
            Label(self.payment_details_frame, text="Account Name: NUR AISYAH FITRIYAH BINTI ANUAR").pack(anchor=W)

        if self.payment_method.get() == "qr":
            # Show QR code
            Label(self.payment_details_frame, text="Scan QR Code:", font=("Arial", 11, "bold")).pack()
            try:
                qr_img = Image.open('qr_code.png')
                qr_img = qr_img.resize((300, 300))
                self.qr_photo = ImageTk.PhotoImage(qr_img)
                qr_label = Label(self.payment_details_frame, image=self.qr_photo)
                qr_label.pack(pady=10)

                Label(self.payment_details_frame,
                      text=f"Amount to Pay: RM {self.fee_label['text']}",
                      font=("Arial", 11)).pack(pady=5)
            except Exception as e:
                print(f"Error loading QR image: {e}")

    def upload_proof(self):
        filename = filedialog.askopenfilename(
            title="Select Payment Proof",
            filetypes=(("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*"))
        )
        if filename:
            self.proof_file = filename
            messagebox.showinfo("Success", "File uploaded successfully!")

    def submit_payment(self):
        if not self.student_var.get():
            messagebox.showerror("Error", "Please select a student!")
            return

        if not self.payment_method.get():
            messagebox.showerror("Error", "Please select a payment method!")
            return

        student_id = self.student_var.get().split(' - ')[0]
        amount = float(self.fee_label['text'])

        try:
            # Generate new FeeID
            self.cursor.execute("SELECT MAX(FeeID) FROM Fee")
            last_id = self.cursor.fetchone()[0]
            if last_id:
                fee_id = f"F{str(int(last_id[1:]) + 1).zfill(3)}"
            else:
                fee_id = "F001"

            # Convert image to binary if uploaded
            payment_proof = None
            if hasattr(self, 'proof_file'):
                with open(self.proof_file, 'rb') as file:
                    payment_proof = file.read()

            # Insert payment record
            self.cursor.execute('''
                INSERT INTO Fee (FeeID, StudentID, Amount, PaymentDate, PaymentMethod, 
                               PaymentStatus, PaymentProof)
                VALUES (?, ?, ?, DATE('now'), ?, 'Pending Approval', ?)
            ''', (fee_id, student_id, amount, self.payment_method.get(), payment_proof))

            self.conn.commit()
            messagebox.showinfo("Success",
                                "Payment submitted successfully! Please wait for approval.")

            # Clear form
            self.student_var.set('')
            self.payment_method.set('')
            if hasattr(self, 'proof_file'):
                delattr(self, 'proof_file')

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.conn.rollback()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


def main():
    root = Tk()
    app = FeePayment(root)
    root.mainloop()


if __name__ == "__main__":
    main()