import csv
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

DATA_FILE = "attendance_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Attendance Management System")
        self.root.geometry("650x500") # Made slightly taller for extra features
        
        self.student_data = load_data()

        # --- LEFT PANEL: Inputs & Controls ---
        input_frame = tk.LabelFrame(root, text=" Manage Students ", padx=10, pady=10)
        input_frame.place(x=20, y=20, width=260, height=450)

        tk.Label(input_frame, text="Student ID:").pack(anchor="w", pady=2)
        self.id_entry = tk.Entry(input_frame)
        self.id_entry.pack(fill="x", pady=5)

        tk.Label(input_frame, text="Student Name:").pack(anchor="w", pady=2)
        self.name_entry = tk.Entry(input_frame)
        self.name_entry.pack(fill="x", pady=5)

        # Core Action Buttons
        tk.Button(input_frame, text="➕ Add Student", bg="#4CAF50", fg="white", command=self.add_student).pack(fill="x", pady=5)
        tk.Button(input_frame, text="✅ Mark Present", bg="#2196F3", fg="white", command=lambda: self.mark_attendance(True)).pack(fill="x", pady=5)
        tk.Button(input_frame, text="❌ Mark Absent", bg="#F44336", fg="white", command=lambda: self.mark_attendance(False)).pack(fill="x", pady=5)
        tk.Button(input_frame, text="🗑️ Delete Student", bg="#E91E63", fg="white", command=self.delete_student).pack(fill="x", pady=5)
        
        # New Feature Buttons
        tk.Button(input_frame, text="📊 Export to CSV", bg="#FF9800", fg="white", command=self.export_to_csv).pack(fill="x", pady=5)
        tk.Button(input_frame, text="⚠️ Clear Database", bg="#9E9E9E", fg="white", command=self.clear_database).pack(fill="x", pady=5)

        # --- RIGHT PANEL: Database View ---
        view_frame = tk.LabelFrame(root, text=" Attendance Database ", padx=10, pady=10)
        view_frame.place(x=300, y=20, width=330, height=450)

        # Table Display
        columns = ("id", "name", "percentage")
        self.tree = ttk.Treeview(view_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("percentage", text="Attendance")
        
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=150, anchor="w")
        self.tree.column("percentage", width=90, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.refresh_table()

    def add_student(self):
        s_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()

        if not s_id or not name:
            messagebox.showwarning("Input Error", "Please fill in both ID and Name fields.")
            return

        if s_id in self.student_data:
            messagebox.showerror("Error", "Student ID already exists!")
            return

        self.student_data[s_id] = {"name": name, "days_present": 0, "total_days": 0}
        save_data(self.student_data)
        self.refresh_table()
        
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        messagebox.showinfo("Success", f"Student '{name}' added successfully!")

    def mark_attendance(self, is_present):
        s_id = self.id_entry.get().strip()
        if not s_id or s_id not in self.student_data:
            messagebox.showerror("Error", "Please enter a valid, existing Student ID.")
            return

        if is_present:
            self.student_data[s_id]["days_present"] += 1
        self.student_data[s_id]["total_days"] += 1

        save_data(self.student_data)
        self.refresh_table()
        messagebox.showinfo("Updated", "Attendance marked successfully!")

    def delete_student(self):
        s_id = self.id_entry.get().strip()
        if not s_id:
            messagebox.showwarning("Input Error", "Please enter the Student ID you want to delete.")
            return

        if s_id in self.student_data:
            student_name = self.student_data[s_id]["name"]
            del self.student_data[s_id]
            
            save_data(self.student_data)
            self.refresh_table()
            
            self.id_entry.delete(0, tk.END)
            self.name_entry.delete(0, tk.END)
            messagebox.showinfo("Deleted", f"Student '{student_name}' has been successfully removed.")
        else:
            messagebox.showerror("Error", "Student ID not found in the database.")

    # NEW: Logic to create an Excel-readable spreadsheet report
    def export_to_csv(self):
        if not self.student_data:
            messagebox.showwarning("Export Warning", "There is no student data to export.")
            return
            
        report_file = "attendance_report.csv"
        try:
            with open(report_file, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                # Header layout
                writer.writerow(["Student ID", "Student Name", "Days Present", "Total Days", "Attendance Percentage", "Status"])
                
                # Write rows dynamically
                for s_id, info in self.student_data.items():
                    total = info["total_days"]
                    present = info["days_present"]
                    pct = (present / total * 100) if total > 0 else 0.0
                    status = "Eligible" if pct >= 75 else "Not Eligible"
                    
                    writer.writerow([s_id, info["name"], present, total, f"{pct:.1f}%", status])
                    
            messagebox.showinfo("Export Complete", f"Successfully saved sheet file as: '{report_file}'")
        except Exception as e:
            messagebox.showerror("Export Error", f"Could not save file: {str(e)}")

    # NEW: Logic to wipe everything safely after confirmation popup
    def clear_database(self):
        if not self.student_data:
            messagebox.showinfo("Info", "Database is already empty.")
            return
            
        confirm = messagebox.askyesno("Confirm Action", "⚠️ Are you absolutely sure you want to completely erase the entire database? This cannot be undone.")
        if confirm:
            self.student_data.clear()
            save_data(self.student_data)
            self.refresh_table()
            messagebox.showinfo("Database Cleared", "All student accounts and histories have been permanently deleted.")

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for s_id, info in self.student_data.items():
            total = info["total_days"]
            present = info["days_present"]
            pct = (present / total * 100) if total > 0 else 0.0
            
            self.tree.insert("", tk.END, values=(s_id, info["name"], f"{pct:.1f}%"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()