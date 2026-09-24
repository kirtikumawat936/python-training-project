import json
import os

# The file where your data will be permanently saved
DATA_FILE = "attendance_data.json"

def load_data():
    """Loads student data from the JSON file. If it doesn't exist, returns an empty dictionary."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {}

def save_data(data):
    """Saves the current student data back to the JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_student(data):
    student_id = input("Enter Student ID: ").strip()
    if student_id in data:
        print("❌ Student ID already exists!")
        return
    
    name = input("Enter Student Name: ").strip()
    if not name:
        print("❌ Name cannot be empty!")
        return

    # Initialize a new student record
    data[student_id] = {
        "name": name,
        "days_present": 0,
        "total_days": 0
    }
    save_data(data)
    print(f"✅ Student '{name}' added successfully!")

def mark_attendance(data):
    student_id = input("Enter Student ID to mark attendance: ").strip()
    if student_id not in data:
        print("❌ Student not found!")
        return

    status = input("Is the student Present? (y/n): ").strip().lower()
    if status == 'y':
        data[student_id]["days_present"] += 1
    
    # Regardless of present or absent, total school days tracked goes up
    data[student_id]["total_days"] += 1
    
    save_data(data)
    print("✅ Attendance updated!")

def show_attendance(data):
    if not data:
        print("📋 No student records found.")
        return

    print("\n--- Attendance Records ---")
    for student_id, info in data.items():
        name = info["name"]
        present = info["days_present"]
        total = info["total_days"]
        
        # Prevent division by zero if attendance hasn't been taken yet
        if total > 0:
            percentage = (present / total) * 100
        else:
            percentage = 0.0

        # Eligibility check logic from your original code snippet
        eligibility = "Eligible" if percentage >= 75 else "Not Eligible"

        print(f"ID: {student_id} | Name: {name} | Attended: {present}/{total} | {percentage:.1f}% | Status: {eligibility}")

def main():
    # Load any existing data right when the program opens
    student_data = load_data()

    while True:
        print("\n===== Student Attendance Management System =====")
        print("1. Add Student")
        print("2. Mark Attendance")
        print("3. Show Attendance")
        print("4. Search Student")
        print("5. Exit")
        
        # Error handling blocks unauthorized or broken typing
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("❌ Invalid input! Please enter a number between 1 and 5.")
            continue  # Re-starts the loop from the top without crashing

        if choice == 1:
            add_student(student_data)
        elif choice == 2:
            mark_attendance(student_data)
        elif choice == 3:
            show_attendance(student_data)
        elif choice == 4:
            # You can build a quick search loop inside here
            search_id = input("Enter Student ID to search: ").strip()
            if search_id in student_data:
                print(f"Found: {student_data[search_id]['name']}")
            else:
                print("❌ Student not found.")
        elif choice == 5:
            print("👋 Exiting program. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please pick a number from 1 to 5.")

if __name__ == "__main__":
    main()        

