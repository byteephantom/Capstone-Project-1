import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import pandas as pd
import os
from datetime import datetime

# Define the path to the CSV file where attendance records will be stored
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "attendance.csv")

# Function to initialize csv file if it doesn't exist
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=["Student_ID", "Name", "Semester", "Date", "Status"])
        df.to_csv(CSV_FILE, index=False)

# To fetch the user input and save attendance
def get_entries():
    student_id = roll_entry.get()  
    first_name = e1.get()
    last_name = e2.get()
    semester = semester_var.get()
    status = status_var.get()
    save_attendance(student_id, first_name, last_name, semester, status)

# Saving attendance data to CSV file
def save_attendance(student_id, first_name, last_name, semester, status):
    date = datetime.today().strftime('%Y-%m-%d') # current date
    #  status = "Present" or "Absent"
    df = pd.read_csv(CSV_FILE)

    # Check if attendance for the student on the same day already exists
    duplicate = df[(df["Student_ID"] == student_id) & (df["Date"] == date)]
    if not duplicate.empty:
        return
    
    #attemdance entry
    new_entry = pd.DataFrame([{ 
        "Student_ID": student_id, 
        "Name": f"{first_name} {last_name}", 
        "Semester": int(semester), 
        "Date": date, 
        "Status": status
    }])

    # New entry and saving data
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

    messagebox.showinfo("Success", "Attendance marked successfully!")


# To display attendance records
def view_attendance():
    for row in tree.get_children():
        tree.delete(row)
    df = pd.read_csv(CSV_FILE)
    # Converting Semester to integer, replacing NaN with 0 (or another placeholder if needed
    df["Semester"] = pd.to_numeric(df["Semester"], errors="coerce").fillna(0).astype(int)

    # Inserting row into the table
    for _, row in df.iterrows():
        tree.insert("", tk.END, values=(
            row["Student_ID"], row["Name"], row["Semester"], row["Date"], row["Status"]
        ))


# To delete records based in Roll No.
def delete_attendance():
    student_id = simpledialog.askstring("Delete Attendance", "Enter Roll Number to delete:")
    
    if not student_id:
        return  # If user cancels or enters nothing, do nothing.

    df = pd.read_csv(CSV_FILE)

    # Check if the roll number exists
    if student_id not in df["Student_ID"].astype(str).values:
        messagebox.showerror("Error", "Roll Number not found!")
        return

    # Confirm before deleting
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete all records for Roll Number {student_id}?")
    
    if confirm:
        df = df[df["Student_ID"].astype(str) != student_id]  # Remove all records of the given roll number
        df.to_csv(CSV_FILE, index=False)
        messagebox.showinfo("Success", f"All records of Roll Number {student_id} have been deleted.")

    # student_id = roll_entry.get()
    # df = pd.read_csv(CSV_FILE)
    # df = df[df["Student_ID"] != student_id]
    # df.to_csv(CSV_FILE, index=False)


# Creating the main application window
window = tk.Tk()
window.title("Attendance Logger")
window.geometry("500x350")  # Window size
window.configure(bg="light blue")

frame = tk.Frame(window, bg="white")
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Ui Element for entering attendance details
tk.Label(frame, text="Roll Number:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
roll_entry = tk.Entry(frame)
roll_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

tk.Label(frame, text="First Name:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
e1 = tk.Entry(frame)
e1.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

tk.Label(frame, text='Last Name:').grid(row=2, column=0, padx=5, pady=5, sticky="e")
e2 = tk.Entry(frame)
e2.grid(row=2, column=1, padx=5, pady=5, sticky="ew")


# Semester selection
tk.Label(frame, text="Semester:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
semester_var = tk.StringVar(value="1")
semester_dropdown = ttk.Combobox(frame, textvariable=semester_var, values=[str(i) for i in range(1, 9)], state="readonly", width=4)
semester_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

# Attendance Status Selection

tk.Label(frame, text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
status_var = tk.StringVar(value="Present")  # Default value

tk.Radiobutton(frame, text="Present", variable=status_var, value="Present").grid(row=4, column=1, sticky="w")
tk.Radiobutton(frame, text="Absent", variable=status_var, value="Absent").grid(row=4, column=2, sticky="w")


# Buttons to submit , view and delete records

#Submit
submit_button = tk.Button(frame, text="Submit", command=get_entries)
submit_button.grid(row=5, column=1, padx=5, pady=15, sticky="ew")

# View
view_button = tk.Button(frame, text="View Attendance", command=view_attendance)
view_button.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

# Delete
delete_button = tk.Button(frame, text="Delete Attendance", command=delete_attendance)
delete_button.grid(row=7, column=1, padx=5, pady=5, sticky="ew")


# Table to diaplay attendance records
tree_frame = tk.Frame(window)
tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

columns = ("ID", "Name", "Semester", "Date", "Status")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill=tk.BOTH, expand=True)

# Look Enhancement with Themes
style = ttk.Style()
style.theme_use("clam")

style.configure("Treeview", rowheight = 25, font=("Arial",10))
style.configure("Treeview.Heading", font=("Arial",12, "bold"))

# Initialize csv and start the Tkinter main loop
initialize_csv()
window.mainloop()


# 🎨 UI/UX Enhancements

# Improve Button Styling
    # Use style.configure() to make buttons more attractive.
    # Add hover effects to buttons.

# Use a Better Font & Padding
    # Set a clean, readable font for labels, entries, and buttons.
    # Increase padding to improve spacing.

# Improve Treeview (Attendance Table) Appearance
    # Add striped row colors (tag_configure()).
    # Increase column width and center-align text.

# Add a Dark Mode / Light Mode Toggle
    # Allow users to switch themes dynamically.

# Add Icons to Buttons
    # Use PhotoImage or Pillow to add small icons.