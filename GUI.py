import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
from datetime import datetime, timedelta
from tkcalendar import Calendar

class TaskManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TODO List")
        self.tasks = []
        self.create_widgets()

    def create_widgets(self):
        self.introduction_row = tk.Frame(self, bg="lightgrey", pady=5)
        self.introduction_row.pack(fill="x")

        intro_label = tk.Label(self.introduction_row, text="TODO List", font=("Helvetica", 16), bg="lightgrey")
        intro_label.pack(side="left", padx=10)

        self.add_button = tk.Button(self.introduction_row, text="+ Add Task", command=self.add_task, bg="blue", fg="white", relief="flat")
        self.add_button.pack(side="right", padx=10)

        self.tasks_frame = tk.Frame(self)
        self.tasks_frame.pack(padx=10, pady=10)

    def add_task(self):
        task_name = simpledialog.askstring("Add Task", "Enter Task Name:")
        if task_name:
            date = self.select_date()
            if date:
                task = {"name": task_name, "date": date}
                self.tasks.append(task)
                self.display_tasks()

    def display_tasks(self):
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()

        for i, task in enumerate(self.tasks):
            name = task["name"]
            date = task["date"]

            countdown = self.calculate_countdown(date)
            status_color = "red" if countdown == "Overdue" else "green"

            task_frame = tk.Frame(self.tasks_frame, bg=status_color, bd=1, relief="solid", padx=5, pady=5, borderwidth=2, highlightbackground="black", highlightthickness=1)
            task_frame.grid(row=i, column=0, sticky="ew")

            task_label = tk.Label(task_frame, text=f"{name} - Due: {date} ({countdown})", bg=status_color)
            task_label.pack(side="left")

            delete_button = tk.Button(task_frame, text="🗑️", command=lambda index=i: self.delete_task(index), bg="black", fg="white", relief="flat")
            delete_button.pack(side="right", padx=5)

            task_label.bind("<Double-1>", lambda event, index=i: self.edit_task(index))

    def delete_task(self, index):
        del self.tasks[index]
        self.display_tasks()

    def edit_task(self, index):
        task = self.tasks[index]
        new_name = simpledialog.askstring("Edit Task", "Enter new Task Name:", initialvalue=task["name"])
        if new_name:
            new_date = self.select_date(initial_date=task["date"])
            if new_date:
                self.tasks[index]["name"] = new_name
                self.tasks[index]["date"] = new_date
                self.display_tasks()

    def calculate_countdown(self, date_str):
        date = datetime.strptime(date_str, "%m/%d/%y")
        today = datetime.today()
        if date < today:
            return "Overdue"
        else:
            remaining = date - today
            return str(remaining).split('.')[0]

    def select_date(self, initial_date=None):
        top = tk.Toplevel(self)
        cal = Calendar(top, selectmode="day")
        cal.pack(padx=10, pady=10)

        if initial_date:
            cal.selection_set(datetime.strptime(initial_date, "%m/%d/%y"))

        def select_and_quit():
            selected_date = cal.get_date()
            top.destroy()
            return selected_date

        confirm_button = tk.Button(top, text="Select Date", command=select_and_quit)
        confirm_button.pack(pady=5)

        top.wait_window()
        return cal.get_date()

if __name__ == "__main__":
    app = TaskManager()
    app.mainloop()
