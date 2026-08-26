# Todo CLI app - OOP version.

import json
import os


class Task:
    """A single todo item."""

    def __init__(self, description: str, done: bool = False) -> None:
        self.description = description
        self.done = done

    def toggle(self) -> None:
        self.done = not self.done

    def to_dict(self) -> dict:
        return {"task": self.description, "done": self.done}

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        return cls(description=data["task"], done=data.get("done", False))

    def __str__(self) -> str:
        status = "✔" if self.done else "❌"
        return f"{status} {self.description}"


class TaskManager:
    """Handles loading, saving, and mutating the task list."""

    def __init__(self, file_path: str = "tasks.json") -> None:
        self.file_path = file_path
        self.tasks: list[Task] = self._load()

    def _load(self) -> list[Task]:
        """Load tasks from disk. Falls back to an empty list if the
        file is missing, empty, corrupted, or not shaped as expected."""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return [Task.from_dict(item) for item in data]
                print("Warning: tasks.json had unexpected content, starting fresh ❗")
                return []
        except (OSError, json.JSONDecodeError, KeyError):
            print("Warning: tasks.json was empty or corrupted, starting fresh ❗")
            return []

    def save(self) -> bool:
        try:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([t.to_dict() for t in self.tasks], file, ensure_ascii=False, indent=2)
            return True
        except OSError:
            print("Error: could not save tasks to disk ❌")
            return False

    def add(self, description: str) -> Task:
        task = Task(description)
        self.tasks.append(task)
        self.save()
        return task

    def delete(self, index: int) -> Task:
        """index is 0-based. Raises IndexError if out of range."""
        task = self.tasks.pop(index)
        self.save()
        return task

    def toggle(self, index: int) -> Task:
        """index is 0-based. Raises IndexError if out of range."""
        task = self.tasks[index]
        task.toggle()
        self.save()
        return task

    def is_valid_index(self, index: int) -> bool:
        return 0 <= index < len(self.tasks)


class TodoCLI:
    """Command-line interface wrapping a TaskManager."""

    MENU = (
        "\n1) Add task",
        "2) View tasks",
        "3) Delete task",
        "4) Exit",
        "5) Toggle task (done/undone)",
    )

    def __init__(self, manager: TaskManager) -> None:
        self.manager = manager
        self.actions = {
            "1": self.add_task,
            "2": self.view_tasks,
            "3": self.delete_task,
            "5": self.toggle_task,
        }

    def run(self) -> None:
        while True:
            self._print_menu()
            choice = input("Enter your choice: ").strip()

            if choice == "4":
                print("Goodbye 👋")
                break

            action = self.actions.get(choice)
            if action is None:
                print("Invalid choice ❌")
                continue

            action()

    def _print_menu(self) -> None:
        for line in self.MENU:
            print(line)

    def _print_task_list(self) -> None:
        for i, task in enumerate(self.manager.tasks, start=1):
            print(f"{i}. {task}")

    def _prompt_task_index(self, prompt: str) -> int | None:
        try:
            choice = int(input(prompt))
        except ValueError:
            print("Please enter a valid number ❗")
            return None

        index = choice - 1
        if self.manager.is_valid_index(index):
            return index

        print("Invalid task number ❌")
        return None

    def add_task(self) -> None:
        description = input("Enter your new task: ").strip()
        if not description:
            print("Task cannot be empty ❗")
            return
        self.manager.add(description)
        print("Task added successfully ✔")

    def view_tasks(self) -> None:
        if not self.manager.tasks:
            print("No tasks yet ❗")
            return
        self._print_task_list()

    def delete_task(self) -> None:
        if not self.manager.tasks:
            print("No tasks to delete ❗")
            return
        self._print_task_list()
        index = self._prompt_task_index("Enter task number to delete: ")
        if index is None:
            return
        removed = self.manager.delete(index)
        print(f"Deleted: {removed.description} ✔")

    def toggle_task(self) -> None:
        if not self.manager.tasks:
            print("No tasks to update ❗")
            return
        self._print_task_list()
        index = self._prompt_task_index("Enter task number to toggle: ")
        if index is None:
            return
        self.manager.toggle(index)
        print("Task updated ✔")


def main() -> None:
    manager = TaskManager()
    cli = TodoCLI(manager)
    cli.run()


if __name__ == "__main__":
    main()
