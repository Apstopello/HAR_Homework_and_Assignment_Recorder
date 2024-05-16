import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# Set the custom theme colors
root_color = "#FC46AA"
frame_color = "#F25278"
button_color = "#FC94AF"

# Database setup and functions
def create_database():
    # Connect to SQLite database and create 'assignments' table
    conn = sqlite3.connect('assignments.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS assignments")  # Drop the existing table
    cursor.execute('''CREATE TABLE assignments
                      (id INTEGER PRIMARY KEY,
                       subject TEXT,
                       project_name TEXT,
                       due_date TEXT,
                       priority INTEGER,
                       progress INTEGER)''')  # Recreate the table with the correct schema
    conn.commit()
    conn.close()

def add_assignment(subject, project_name, due_date, priority):
    # Add a new assignment to the database
    try:
        datetime.strptime(due_date, '%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Use MM-DD format.")
        return

    if int(priority) not in range(1, 6):
        messagebox.showerror("Error", "Priority must be between 1 and 5.")
        return

    conn = sqlite3.connect('assignments.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO assignments (subject, project_name, due_date, priority, progress) VALUES (?, ?, ?, ?, ?)",
                   (subject, project_name, due_date, priority, 0))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Assignment added.")

def view_assignments():
    # Retrieve all assignments from the database and return them
    conn = sqlite3.connect('assignments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assignments ORDER BY priority ASC, due_date")
    assignments = cursor.fetchall()
    conn.close()
    return assignments

def update_progress(assignment_id, progress):
    # Update the progress of an assignment
    conn = sqlite3.connect('assignments.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE assignments SET progress = ? WHERE id = ?", (progress, assignment_id))
    conn.commit()
    conn.close()

def remove_assignment(assignment_id):
    # Remove an assignment from the database
    conn = sqlite3.connect('assignments.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM assignments WHERE id = ?", (assignment_id,))
    conn.commit()
    conn.close()

def move_to_finished():
    # Move completed assignments to a separate table or perform any other necessary actions
    conn = sqlite3.connect('assignments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM assignments WHERE progress = 100")
    finished_ids = cursor.fetchall()
    for assignment_id in finished_ids:
        cursor.execute("INSERT INTO finished_projects SELECT * FROM assignments WHERE id = ?", (assignment_id[0],))
        cursor.execute("DELETE FROM assignments WHERE id = ?", (assignment_id[0],))
    conn.commit()
    conn.close()

# GUI setup and functions
class HomeworkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HARHARHAR: Homework and Assignment Recorder")
        
        # Apply custom theme colors
        self.style = ttk.Style()
        self.style.configure("Root.TFrame", background=root_color)
        self.style.configure("TFrame", background=frame_color)
        self.style.configure("TButton", background=button_color)
        self.style.map("TButton", background=[('active', button_color)])

        self.create_widgets()

    def create_widgets(self):
        # Add, Update, Remove Assignment frames in a single row
        self.operation_frame = ttk.Frame(self.root, style="Root.TFrame")
        self.operation_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Add Assignment
        self.add_frame = ttk.LabelFrame(self.operation_frame, text="Add Assignment", style="TFrame")
        self.add_frame.grid(row=0, column=0, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Subject:").grid(row=0, column=0, padx=5, pady=5)
        self.subject_entry = ttk.Combobox(self.add_frame, values=["MAPEH", "Math", "Science", "English", "Filipino", "ESP", "ICT", "Research", "Araling Panlipunan"], state="readonly")
        self.subject_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Project Name:").grid(row=1, column=0, padx=5, pady=5)
        self.project_name_entry = ttk.Entry(self.add_frame)
        self.project_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Due Date (MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.due_date_entry = ttk.Entry(self.add_frame)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.add_frame, text="Priority (1-5):").grid(row=3, column=0, padx=5, pady=5)
        self.priority_entry = ttk.Entry(self.add_frame)
        self.priority_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.add_frame, text="Add Assignment", command=self.add_assignment_handler, style="TButton")
        self.add_button.grid(row=4, columnspan=2, pady=5)

        # Update Progress
        self.update_frame = ttk.LabelFrame(self.operation_frame, text="Update Assignment", style="TFrame")
        self.update_frame.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.update_frame, text="Assignment ID:").grid(row=0, column=0, padx=5, pady=5)
        self.update_id_entry = ttk.Entry(self.update_frame)
        self.update_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.update_frame, text="Progress (0-100):").grid(row=1, column=0, padx=5, pady=5)
        self.update_progress_entry = ttk.Entry(self.update_frame)
        self.update_progress_entry.grid(row=1, column=1, padx=5, pady=5)

        self.update_button = ttk.Button(self.update_frame, text="Update Progress", command=self.update_progress_handler, style="TButton")
        self.update_button.grid(row=2, columnspan=2, pady=5)

        # Remove Assignment
        self.remove_frame = ttk.LabelFrame(self.operation_frame, text="Remove Assignment", style="TFrame")
        self.remove_frame.grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(self.remove_frame, text="Assignment ID:").grid(row=0, column=0, padx=5, pady=5)
        self.remove_id_entry = ttk.Entry(self.remove_frame)
        self.remove_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.remove_button = ttk.Button(self.remove_frame, text="Remove Assignment", command=self.remove_assignment_handler, style="TButton")
        self.remove_button.grid(row=1, columnspan=2, pady=5)

        # View Assignments
        self.view_frame = ttk.LabelFrame(self.root, text="Assignments", style="TFrame")
        self.view_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.tree = ttk.Treeview(self.view_frame, columns=("ID", "Subject", "Project Name", "Due Date", "Priority", "Progress"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Subject", text="Subject")
        self.tree.heading("Project Name", text="Project Name")
        self.tree.heading("Due Date", text="Due Date")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Progress", text="Progress")

        self.tree.grid(row=0, column=0, padx=5, pady=5)

        self.refresh_button = ttk.Button(self.view_frame, text="Refresh", command=self.view_assignments, style="TButton")
        self.refresh_button.grid(row=1, column=0, pady=5)

        self.view_assignments()  # Call view_assignments to populate the Treeview

    def add_assignment_handler(self):
        # Get data from entry fields, validate, and add assignment
        subject = self.subject_entry.get()
        project_name = self.project_name_entry.get()
        due_date = self.due_date_entry.get()
        priority = self.priority_entry.get()

        if subject and project_name and due_date and priority:
            if not priority.isdigit():
                messagebox.showerror("Error", "Priority must be a number.")
                return

            add_assignment(subject, project_name, due_date, int(priority))
            self.subject_entry.set('')
            self.project_name_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            self.view_assignments()  # Refresh the assignments view
        else:
            messagebox.showerror("Error", "All fields are required.")

    def update_progress_handler(self):
        # Get assignment ID and progress, validate, and update progress
        assignment_id = self.update_id_entry.get()
        progress = self.update_progress_entry.get()

        if assignment_id and progress:
            if not assignment_id.isdigit() or not progress.isdigit():
                messagebox.showerror("Error", "Assignment ID and Progress must be numbers.")
                return

            if int(progress) > 100 or int(progress) < 0:
                messagebox.showerror("Error", "Progress must be between 0 and 100.")
            else:
                update_progress(int(assignment_id), int(progress))
                messagebox.showinfo("Success", "Progress updated.")
                self.update_id_entry.delete(0, tk.END)
                self.update_progress_entry.delete(0, tk.END)
                self.view_assignments()  # Refresh the assignments view
        else:
            messagebox.showerror("Error", "All fields are required.")

    def remove_assignment_handler(self):
        # Get assignment ID, validate, and remove assignment
        assignment_id = self.remove_id_entry.get()

        if assignment_id:
            if not assignment_id.isdigit():
                messagebox.showerror("Error", "Assignment ID must be a number.")
                return

            remove_assignment(int(assignment_id))
            messagebox.showinfo("Success", "Assignment removed.")
            self.remove_id_entry.delete(0, tk.END)
            self.view_assignments()
        else:
            messagebox.showerror("Error", "Assignment ID is required.")

    def view_assignments(self):
        # Refresh the Treeview with current assignments
        for i in self.tree.get_children():
            self.tree.delete(i)

        assignments = view_assignments()
        for a in assignments:
            if a[4] == 1:  # Check if the priority is 1 (index 3)
                self.tree.insert("", "end", values=(a[0], a[1], a[2], a[3], a[4], a[5]), tags=("priority1",))
            else:
                self.tree.insert("", "end", values=(a[0], a[1], a[2], a[3], a[4], a[5]))
        
        self.tree.tag_configure("priority1", font=("Arial", 10, "bold"))


# Run the application
if __name__ == "__main__":
    create_database()
    move_to_finished()  # Move finished projects to the finished table
    root = tk.Tk()
    root.configure(background="#FC46AA")  # Set the background color of the root window
    app = HomeworkApp(root)
    root.mainloop()