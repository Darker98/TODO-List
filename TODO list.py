import sqlite3
import datetime as dt

class Todo:
    def __init__(self):
        # Initialize connection do database
        self.connection = sqlite3.connect('todo.db')
        self.cur = self.connection.cursor()
        self.create_table()
        
    def create_table(self):
        # Make sure table exists
        self.cur.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY,
                                task STRING NOT NULL,
                                date DATE NOT NULL);''')

    # Create new task    
    def add_task(self, task, date):
        self.cur.execute("INSERT INTO tasks (task, date) VALUES (?,?)", (task, date))
        self.connection.commit()
    
    # Find a particular task
    def find_task(self, key):
        self.cur.execute(f"SELECT * FROM tasks WHERE id = ?", (key,))
        row = self.cur.fetchone()
        
        if (row): 
            return row
        
        return None
    
    # Display all tasks
    def show_tasks(self):
        self.cur.execute("SELECT * FROM tasks")
        for record in self.cur:
            print(record)

    # Update a particular task
    # TODO: Define custom exception for incorrect function call
    def update_task(self, key, task = "", date = -1):
        if (task != "" and date != -1):
            self.cur.execute("UPDATE tasks SET task = ?, date = ? WHERE id = ?", (task, date, key,))
        elif (task != ""):
            self.cur.execute("UPDATE tasks SET task = ? WHERE id = ?", (task, key,))
        elif (date != -1):
            self.cur.execute("UPDATE tasks SET date = ? WHERE id = ?", (date, key,))
        else:
            raise BaseException
        
        self.connection.commit()

    # Delete a particular task
    def delete_task(self, key):
        self.cur.execute(f"DELETE FROM tasks WHERE id = ?", (key,))
        self.connection.commit()

    # Delete all tasks
    def delete_all(self):
        self.cur.execute("DELETE FROM tasks")
        self.connection.commit()


db = Todo()
db.add_task("Drink water", dt.date(2024, 12, 2))
db.show_tasks()
print("----------------")
db.update_task(1, "Updated task")
db.show_tasks()
db.delete_all()
print("---------------")
db.show_tasks()