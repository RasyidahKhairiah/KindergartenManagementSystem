import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


class PaymentReviewSystem:
    def __init__(self, root, return_callback=None):
        self.root = root
        self.return_callback = return_callback
        self.root.title("Parent Payment Review System")
        self.root.state('zoomed')
        self.root.configure(bg='#f0f0f0')

        # Setup database connection
        self.conn = sqlite3.connect('kindergarten_management.db')
        self.cursor = self.conn.cursor()

        self.setup_main_frame()
        self.setup_navigation()
        self.setup_tabs()
        self.setup_title()
        self.create_treeview()
        self.setup_approval_buttons()
        self.current_view = "status"
        self.load_status_data()

    def setup_main_frame(self):
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    def setup_navigation(self):
        nav_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        nav_frame.pack(fill=tk.X, pady=(0, 20))

        tk.Button(nav_frame, text="Home", bg='#cd853f', fg='white',
                  font=('Arial', 12, 'bold'), width=10, command=self.go_home).pack(side=tk.LEFT)

        tk.Button(nav_frame, text="Logout", bg='#cd853f', fg='white',
                  font=('Arial', 12, 'bold'), width=10, command=self.logout).pack(side=tk.RIGHT)

    def setup_tabs(self):
        tab_container = tk.Frame(self.main_frame, bg='#f0f0f0')
        tab_container.pack(fill=tk.X)

        tab_frame = tk.Frame(tab_container, bg='#f0f0f0')
        tab_frame.pack(expand=True)

        self.status_btn = tk.Button(tab_frame, text="Status", bg='#f0f0f0', fg='black',
                                    font=('Arial', 12), width=20, command=self.switch_to_status)
        self.status_btn.pack(side=tk.LEFT)

        self.approval_btn = tk.Button(tab_frame, text="Approval", bg='#d3d3d3', fg='black',
                                      font=('Arial', 12), width=20, command=self.switch_to_approval)
        self.approval_btn.pack(side=tk.LEFT)

    def setup_title(self):
        tk.Label(self.main_frame, text="PARENT PAYMENT REVIEW",
                 font=('Arial', 24, 'bold'), bg='#f0f0f0', fg='#cd853f').pack(pady=20)

    def create_treeview(self):
        tree_frame = tk.Frame(self.main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        columns = ("Parent ID", "Parent Name", "Child ID", "Child Name",
                   "Total Fee Payment (RM)", "Fee ID", "Payment Status")

        self.tree = ttk.Treeview(tree_frame, columns=columns,
                                 show='headings', yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.tree.yview)

        # Configure columns
        column_widths = {'Parent ID': 100, 'Parent Name': 150, 'Child ID': 100,
                         'Child Name': 150, 'Total Fee Payment (RM)': 150,
                         'Fee ID': 100, 'Payment Status': 150}

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths[col])

        self.tree.pack(fill=tk.BOTH, expand=True)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        style.configure("Treeview", font=('Arial', 10), rowheight=25)

    def setup_approval_buttons(self):
        self.button_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.button_frame.pack(pady=20)

        tk.Button(self.button_frame, text="Approve", bg='#5f9ea0', fg='white',
                  font=('Arial', 12, 'bold'), width=15,
                  command=self.approve_payment).pack(side=tk.LEFT, padx=10)

        tk.Button(self.button_frame, text="Decline", bg='#5f9ea0', fg='white',
                  font=('Arial', 12, 'bold'), width=15,
                  command=self.decline_payment).pack(side=tk.LEFT, padx=10)

        self.button_frame.pack_forget()  # Initially hidden

    def load_status_data(self):
        self.clear_tree()
        try:
            self.cursor.execute("""
                SELECT 
                    p.ParentID, 
                    p.ParentName,
                    s.StudentID,
                    s.StudentName,
                    f.Amount,
                    f.FeeID,
                    f.PaymentStatus
                FROM Fee f
                JOIN students s ON f.StudentID = s.StudentID
                JOIN parents p ON s.ParentID = p.ParentID
                ORDER BY f.PaymentDate DESC
            """)
            data = self.cursor.fetchall()
            self.insert_data(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def load_approval_data(self):
        self.clear_tree()
        try:
            self.cursor.execute("""
                SELECT 
                    p.ParentID, 
                    p.ParentName,
                    s.StudentID,
                    s.StudentName,
                    f.Amount,
                    f.FeeID,
                    f.PaymentStatus
                FROM Fee f
                JOIN students s ON f.StudentID = s.StudentID
                JOIN parents p ON s.ParentID = p.ParentID
                WHERE f.PaymentStatus = 'Pending Approval'
                ORDER BY f.PaymentDate DESC
            """)
            data = self.cursor.fetchall()
            self.insert_data(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def insert_data(self, data):
        for item in data:
            self.tree.insert("", tk.END, values=item)

    def switch_to_status(self):
        if self.current_view != "status":
            self.status_btn.config(bg='#f0f0f0', relief=tk.SUNKEN)
            self.approval_btn.config(bg='#d3d3d3', relief=tk.RAISED)
            self.button_frame.pack_forget()
            self.load_status_data()
            self.current_view = "status"

    def switch_to_approval(self):
        if self.current_view != "approval":
            self.status_btn.config(bg='#d3d3d3', relief=tk.RAISED)
            self.approval_btn.config(bg='#f0f0f0', relief=tk.SUNKEN)
            self.button_frame.pack(pady=20)
            self.load_approval_data()
            self.current_view = "approval"

    def approve_payment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a payment to approve.")
            return

        try:
            for item in selected_item:
                fee_id = self.tree.item(item)['values'][5]  # FeeID is at index 5
                self.cursor.execute("""
                    UPDATE Fee 
                    SET PaymentStatus = 'Approved'
                    WHERE FeeID = ?
                """, (fee_id,))

            self.conn.commit()
            messagebox.showinfo("Success", "Payment has been approved!")

            # Refresh the view
            if self.current_view == "status":
                self.load_status_data()
            else:
                self.load_approval_data()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to approve payment: {str(e)}")
            self.conn.rollback()

    def decline_payment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a payment to decline.")
            return

        try:
            for item in selected_item:
                fee_id = self.tree.item(item)['values'][5]  # FeeID is at index 5
                self.cursor.execute("""
                    UPDATE Fee 
                    SET PaymentStatus = 'Declined'
                    WHERE FeeID = ?
                """, (fee_id,))

            self.conn.commit()
            messagebox.showinfo("Success", "Payment has been declined!")

            # Refresh the view
            if self.current_view == "status":
                self.load_status_data()
            else:
                self.load_approval_data()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to decline payment: {str(e)}")
            self.conn.rollback()

    def go_home(self):
        if self.return_callback:
            for widget in self.root.winfo_children():
                widget.destroy()
            self.return_callback()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.quit()

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()


def main():
    root = tk.Tk()
    app = PaymentReviewSystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()