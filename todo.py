from datetime import datetime
import os

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        GREEN = ''
        RED = ''
        YELLOW = ''
    class Style:
        RESET_ALL = ''

TASKS_FILE = "tasks.txt"

class Task:
    def __init__(self, title, status=False, priority="Medium", due_date=None):
        self.title = title
        self.status = status
        self.priority = priority
        self.due_date = due_date

    def __str__(self):
        status_str = Fore.GREEN + "✓" if self.status else Fore.RED + "✗"
        due = f" | Due: {self.due_date}" if self.due_date else ""
        return f"{status_str} {self.title} [Priority: {self.priority}]{due}" + Style.RESET_ALL

    def to_line(self):
        return f"{self.title}|{int(self.status)}|{self.priority}|{self.due_date if self.due_date else ''}\n"

    @staticmethod
    def from_line(line):
        parts = line.strip().split("|")
        title = parts[0]
        status = bool(int(parts[1]))
        priority = parts[2]
        due_date = parts[3] if parts[3] else None
        return Task(title, status, priority, due_date)

class TodoList:
    def __init__(self):
        self.tasks = []
        self.load_from_file()

    def add_task(self, title, priority="Medium", due_date=None):
        self.tasks.append(Task(title, False, priority, due_date))
        self.save_to_file()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            del self.tasks[index]
            self.save_to_file()

    def mark_done(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].status = True
            self.save_to_file()

    def view_tasks(self):
        if not self.tasks:
            print(Fore.YELLOW + "\nNo tasks yet!\n")
            return
        print("\nYour Tasks:")
        for idx, task in enumerate(self.tasks):
            print(f"{idx+1}. {task}")
        print(Style.RESET_ALL)

    def save_to_file(self):
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            for task in self.tasks:
                f.write(task.to_line())

    def load_from_file(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                self.tasks = [Task.from_line(line) for line in lines]

def main():
    todo = TodoList()

    print(Fore.YELLOW + """
    *************************
        📝 To-Do List App 📝
    *************************
    """ + Style.RESET_ALL)

    while True:
        print("\nMenu:")
        print("1. View tasks")
        print("2. Add task")
        print("3. Mark task as done")
        print("4. Remove task")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")

        if choice == "1":
            todo.view_tasks()
        elif choice == "2":
            title = input("Task title: ")
            priority = input("Priority (Low/Medium/High): ") or "Medium"
            due_date = input("Due date (YYYY-MM-DD) or leave blank: ") or None
            if due_date:
                try:
                    datetime.strptime(due_date, "%Y-%m-%d")
                except ValueError:
                    print(Fore.RED + "Invalid date format. Skipping due date." + Style.RESET_ALL)
                    due_date = None
            todo.add_task(title, priority, due_date)
            print(Fore.GREEN + "Task added successfully!" + Style.RESET_ALL)
        elif choice == "3":
            todo.view_tasks()
            idx = input("Task number to mark as done: ")
            if idx.isdigit():
                todo.mark_done(int(idx)-1)
                print(Fore.GREEN + "Task marked as done!" + Style.RESET_ALL)
        elif choice == "4":
            todo.view_tasks()
            idx = input("Task number to remove: ")
            if idx.isdigit():
                todo.remove_task(int(idx)-1)
                print(Fore.GREEN + "Task removed!" + Style.RESET_ALL)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice, please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()