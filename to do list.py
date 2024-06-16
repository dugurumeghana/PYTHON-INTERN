import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from datetime import datetime

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")

        self.conn = sqlite3.connect('todo.db')
        self.create_table()

        self.create_widgets()
        self.load_tasks()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                priority INTEGER,
                completed BOOLEAN,
                category TEXT,
                due_date TEXT
            )
        ''')
        self.conn.commit()

    def create_widgets(self):
        self.task_entry = tk.Entry(self.root, width=50)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.add_button = tk.Button(self.root, text="Add Task", command=self.add_task, width=15)
        self.add_button.grid(row=0, column=2, padx=10, pady=10)

        self.tasks_listbox = tk.Listbox(self.root, width=70, height=15)
        self.tasks_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        self.delete_button = tk.Button(self.root, text="Delete Task", command=self.delete_task, width=15)
        self.delete_button.grid(row=2, column=0, padx=10, pady=10)

        self.update_button = tk.Button(self.root, text="Update Task", command=self.update_task, width=15)
        self.update_button.grid(row=2, column=1, padx=10, pady=10)

        self.complete_button = tk.Button(self.root, text="Mark as Complete", command=self.mark_as_complete, width=15)
        self.complete_button.grid(row=2, column=2, padx=10, pady=10)

        self.filter_button = tk.Button(self.root, text="Filter Tasks", command=self.filter_tasks, width=15)
        self.filter_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def load_tasks(self):
        self.tasks_listbox.delete(0, tk.END)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, task, priority, completed, category, due_date FROM tasks")
        tasks = cursor.fetchall()
        for task in tasks:
            self.tasks_listbox.insert(tk.END, f"{task[0]} - {task[1]} - Priority: {task[2]} - {'Completed' if task[3] else 'Pending'} - Category: {task[4]} - Due: {task[5]}")

    def add_task(self):
        task = self.task_entry.get()
        if not task:
            messagebox.showwarning("Input Error", "Please enter a task.")
            return

        priority = simpledialog.askinteger("Input", "Enter task priority (1-5):")
        category = simpledialog.askstring("Input", "Enter task category:")
        due_date = simpledialog.askstring("Input", "Enter due date (YYYY-MM-DD):")

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO tasks (task, priority, completed, category, due_date) VALUES (?, ?, ?, ?, ?)",
                       (task, priority, False, category, due_date))
        self.conn.commit()
        self.load_tasks()

    def delete_task(self):
        selected_task = self.tasks_listbox.get(tk.ACTIVE)
        if not selected_task:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return

        task_id = selected_task.split(' - ')[0]
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        self.conn.commit()
        self.load_tasks()

    def update_task(self):
        selected_task = self.tasks_listbox.get(tk.ACTIVE)
        if not selected_task:
            messagebox.showwarning("Selection Error", "Please select a task to update.")
            return

        task_id = selected_task.split(' - ')[0]
        new_task = simpledialog.askstring("Input", "Enter new task description:")
        new_priority = simpledialog.askinteger("Input", "Enter new task priority (1-5):")
        new_category = simpledialog.askstring("Input", "Enter new task category:")
        new_due_date = simpledialog.askstring("Input", "Enter new due date (YYYY-MM-DD):")

        cursor = self.conn.cursor()
        cursor.execute("UPDATE tasks SET task=?, priority=?, category=?, due_date=? WHERE id=?",
                       (new_task, new_priority, new_category, new_due_date, task_id))
        self.conn.commit()
        self.load_tasks()

    def mark_as_complete(self):
        selected_task = self.tasks_listbox.get(tk.ACTIVE)
        if not selected_task:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")
            return

        task_id = selected_task.split(' - ')[0]
        cursor = self.conn.cursor()
        cursor.execute("UPDATE tasks SET completed=? WHERE id=?", (True, task_id))
        self.conn.commit()
        self.load_tasks()

    def filter_tasks(self):
        filter_criteria = simpledialog.askstring("Input", "Enter filter criteria (category or due date):")
        self.tasks_listbox.delete(0, tk.END)
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, task, priority, completed, category, due_date FROM tasks WHERE category=? OR due_date=?", (filter_criteria, filter_criteria))
        tasks = cursor.fetchall()
        for task in tasks:
            self.tasks_listbox.insert(tk.END, f"{task[0]} - {task[1]} - Priority: {task[2]} - {'Completed' if task[3] else 'Pending'} - Category: {task[4]} - Due: {task[5]}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()

