import sqlite3

class Todo:
    
    def __init__(self):
        self.connection = sqlite3.connect(r'path\todo.db')
        self.cursor_ = self.connection.cursor()
        self.create_task_table()
        
    def create_task_table(self):
        self.cursor_.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY,
                                task STRING NOT NULL,
                                priority INTEGER NOT NULL);''')
        
    def add_task(self):
        task = input("Enter task name: ")
        if task.strip() == "":
            print("Error: Task can not be an empty string.")
            return
        if self.find_task(task) is not None:
            print("Error: Task already exists.")
            return
            
        priority = int(input("Enter task priority: "))
        if priority < 1:
            print("Error: Priority can not be less than 1.")
            return
        
        self.cursor_.execute("INSERT INTO tasks (task, priority) VALUES (?,?)", (task, priority))
        self.connection.commit()
    
    def find_task(self, task_name):
        self.cursor_.execute("SELECT * FROM tasks")
        
        for record in self.cursor_:
            if record[1] == task_name:
                return record
        
        return None
        
    def show_tasks(self):
        self.cursor_.execute("SELECT * FROM tasks")
        for record in self.cursor_:
            print(record)

    def delete_task(self, task_name):
        self.cursor_.execute(f"DELETE FROM tasks WHERE task == {task_name}")
        self.connection.commit()

db = Todo()
db.add_task()
print("---------")
print("TODO List")
print("---------")
db.show_tasks()
db.delete_task("Drink")