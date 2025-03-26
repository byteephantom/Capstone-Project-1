import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
import pandas as pd
import os
from datetime import datetime
from tkinter import *
from fpdf import FPDF

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


# Export to Excel
def export_to_excel():
    df = pd.read_csv(CSV_FILE)
    export_path = os.path.join(BASE_DIR, "attendance.xlsx")
    df.to_excel(export_path, index=False)
    messagebox.showinfo("Export Successful", f"Data exported to {export_path}")

# Export to PDF
def export_to_pdf():
    try:
        df = pd.read_csv(CSV_FILE)
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=12)  # Fixed: Use core font

        # Title (fixed parameters)
        pdf.cell(200, 10, text="Attendance Records", new_x="LMARGIN", new_y="NEXT", align='C')
        pdf.ln(10)

        # Headers
        for col in df.columns:
            pdf.cell(40, 10, text=str(col), border=1)
        pdf.ln()

        # Data rows
        for _, row in df.iterrows():
            for col in df.columns:
                pdf.cell(40, 10, text=str(row[col]), border=1)
            pdf.ln()

        pdf_path = os.path.join(BASE_DIR, "attendance.pdf")
        pdf.output(pdf_path)
        messagebox.showinfo("Export Successful", f"Data exported to {pdf_path}")
    except Exception as e:
        messagebox.showerror("PDF Export Error", f"Failed to export PDF: {str(e)}")

# Creating the main application window
window = tk.Tk()
window.title("Attendance Logger")
window.geometry("500x350")  # Window size
window.configure(bg="white")

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


# Buttons to submit , view and delete records and export as well

#Submit
submit_button = tk.Button(frame, text="Submit", command=get_entries)
submit_button.grid(row=5, column=1, padx=5, pady=15, sticky="ew")

# View
view_button = tk.Button(frame, text="View Attendance", command=view_attendance)
view_button.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

# Delete
delete_button = tk.Button(frame, text="Delete Attendance", command=delete_attendance)
delete_button.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

# Export Menu Button
export_menu_button = tk.Menubutton(frame, text="Export Data", relief=tk.RAISED)
export_menu_button.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

# Create the dropdown menu(with option pdf and excel)
export_menu = tk.Menu(export_menu_button, tearoff=0)
export_menu.add_command(label="As PDF", command=export_to_pdf)
export_menu.add_command(label="As Excel Sheet", command=export_to_excel)

# Attach the menu to the button
export_menu_button.config(menu=export_menu)

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

# Dark Mode
def toggle_dark_mode():
    if window.cget("bg") == "white":
        window.configure(bg="#2E2E2E")
        frame.configure(bg="#2E2E2E")
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button) or isinstance(widget, tk.Radiobutton):
                widget.configure(bg="#2E2E2E", fg="white")
        dark_mode_button.configure(text="Light Mode", bg="#444", fg="white")
    else:
        window.configure(bg="white")
        frame.configure(bg="white")
        for widget in frame.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button) or isinstance(widget, tk.Radiobutton):
                widget.configure(bg="white", fg="black")
        dark_mode_button.configure(text="Dark Mode", bg="lightgray", fg="black")

# Dark mode toggle button
dark_mode_button = tk.Button(window, text="Dark Mode", command=toggle_dark_mode, bg="lightgray", fg="black")
dark_mode_button.pack(pady=5)

# Initialize csv and start the Tkinter main loop
initialize_csv()
window.mainloop()
