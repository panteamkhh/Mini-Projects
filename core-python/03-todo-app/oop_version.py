"""
Day 3 - Todo App (OOP version)

A command-line to-do list manager with JSON persistence.
"""

import json
import os


class Task:
    """A single to-do item."""

    def __init__(self, description: str, done: bool = False) -> None:
        self.description = description
        self.done = done

    def to_dict(self) -> dict:
        return {"task": self.description, "done": self.done}

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(description=data["task"], done=data.get("done", False))

    def __str__(self) -> str:
        status = "✔" if self.done else "❌"
        return f"{status} {self.description}"


class TodoApp:
    """Manages a list of Task objects with JSON persistence and a CLI menu."""

    def __init__(self, file_name: str = "tasks.json") -> None:
        self.file_name = file_name
        self.tasks: list[Task] = self._load()

    def _load(self) -> list[Task]:
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                return [Task.from_dict(item) for item in json.load(file)]
        return []

    def save(self) -> None:
        with open(self.file_name, "w") as file:
            json.dump([task.to_dict() for task in self.tasks], file)

    def add_task(self, description: str) -> None:
        self.tasks.append(Task(description))
        self.save()

    def delete_task(self, index: int) -> Task | None:
        if 0 <= index < len(self.tasks):
            removed = self.tasks.pop(index)
            self.save()
            return removed
        return None

    def toggle_task(self, index: int) -> bool:
        if 0 <= index < len(self.tasks):
            self.tasks[index].done = not self.tasks[index].done
            self.save()
            return True
        return False

    def list_tasks(self) -> None:
        if not self.tasks:
            print("No tasks yet ❗")
            return
        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}. {task}")

    def run(self) -> None:
        while True:
            print("\n1) Add task")
            print("2) View tasks")
            print("3) Delete task")
            print("4) Exit")
            print("5) Toggle task (done/undone)")

            choice = input("Enter your choice: ")

            if choice == "1":
                description = input("Enter your new task: ")
                self.add_task(description)
                print("Task added successfully ✔")

            elif choice == "2":
                self.list_tasks()

            elif choice == "3":
                self.list_tasks()
                try:
                    index = int(input("Enter task number to delete: ")) - 1
                    removed = self.delete_task(index)
                    print(f"Deleted: {removed.description} ✔" if removed else "Invalid task number ❌")
                except ValueError:
                    print("Please enter a valid number ❗")

            elif choice == "5":
                self.list_tasks()
                try:
                    index = int(input("Enter task number to toggle: ")) - 1
                    print("Task updated ✔" if self.toggle_task(index) else "Invalid task number ❌")
                except ValueError:
                    print("Please enter a valid number ❗")

            elif choice == "4":
                print("Goodbye 👋")
                break

            else:
                print("Invalid choice ❌")


if __name__ == "__main__":
    app = TodoApp()
    app.run()
