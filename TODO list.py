import sqlite3

class UpdateException(Exception):
    def __init__(self, message = "Called update_task() without any task or date to modify"):
        super().__init__(message)

class Todo:
    def __init__(self):
        # Initialize connection to database
        self.connection = sqlite3.connect('todo.db')
        self.cur = self.connection.cursor()
        self.create_table()
    
    # Make sure table exists
    def create_table(self):
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
    def update_task(self, key, task = "", date = -1):
        if (task != "" and date != -1):
            self.cur.execute("UPDATE tasks SET task = ?, date = ? WHERE id = ?", (task, date, key,))
        elif (task != ""):
            self.cur.execute("UPDATE tasks SET task = ? WHERE id = ?", (task, key,))
        elif (date != -1):
            self.cur.execute("UPDATE tasks SET date = ? WHERE id = ?", (date, key,))
        else:
            raise UpdateException()
        
        self.connection.commit()

    # Delete a particular task
    def delete_task(self, key):
        self.cur.execute(f"DELETE FROM tasks WHERE id = ?", (key,))
        self.connection.commit()

    # Delete all tasks
    def delete_all(self):
        self.cur.execute("DELETE FROM tasks")
        self.connection.commit()