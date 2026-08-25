# Todo CLI app - improved procedural version.


import json
import os

FILE_NAME = "tasks.json"


def load_tasks() -> list[dict]:
    """Load tasks from disk. Falls back to an empty list if the file
    doesn't exist, is empty/corrupted, or doesn't contain a list."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            print("Warning: tasks.json had unexpected content, starting fresh ❗")
            return []
    except (OSError, json.JSONDecodeError):
        print("Warning: tasks.json was empty or corrupted, starting fresh ❗")
        return []


def save_tasks(tasks: list[dict]) -> bool:
    """Persist tasks to disk. Returns True on success, False on failure."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
        return True
    except OSError:
        print("Error: could not save tasks to disk ❌")
        return False


def print_task_list(tasks: list[dict]) -> None:
    """Print a numbered list of all tasks with their status."""
    for i, task in enumerate(tasks, start=1):
        status = "✔" if task["done"] else "❌"
        print(f"{i}. {status} {task['task']}")


def prompt_task_index(tasks: list[dict], prompt: str) -> int | None:
    """Ask the user to pick a task number. Returns a valid 0-based
    index, or None if the input was invalid/out of range."""
    try:
        choice = int(input(prompt))
    except ValueError:
        print("Please enter a valid number ❗")
        return None

    if 1 <= choice <= len(tasks):
        return choice - 1

    print("Invalid task number ❌")
    return None


def add_task(tasks: list[dict]) -> None:
    description = input("Enter your new task: ").strip()
    if not description:
        print("Task cannot be empty ❗")
        return
    tasks.append({"task": description, "done": False})
    if save_tasks(tasks):
        print("Task added successfully ✔")


def view_tasks(tasks: list[dict]) -> None:
    if not tasks:
        print("No tasks yet ❗")
        return
    print_task_list(tasks)


def delete_task(tasks: list[dict]) -> None:
    if not tasks:
        print("No tasks to delete ❗")
        return
    print_task_list(tasks)
    index = prompt_task_index(tasks, "Enter task number to delete: ")
    if index is None:
        return
    removed = tasks.pop(index)
    if save_tasks(tasks):
        print(f"Deleted: {removed['task']} ✔")


def toggle_task(tasks: list[dict]) -> None:
    if not tasks:
        print("No tasks to update ❗")
        return
    print_task_list(tasks)
    index = prompt_task_index(tasks, "Enter task number to toggle: ")
    if index is None:
        return
    tasks[index]["done"] = not tasks[index]["done"]
    if save_tasks(tasks):
        print("Task updated ✔")


def print_menu() -> None:
    print("\n1) Add task")
    print("2) View tasks")
    print("3) Delete task")
    print("4) Exit")
    print("5) Toggle task (done/undone)")


def main() -> None:
    tasks = load_tasks()

    actions = {
        "1": add_task,
        "2": view_tasks,
        "3": delete_task,
        "5": toggle_task,
    }

    while True:
        print_menu()
        user_choice = input("Enter your choice: ").strip()

        if user_choice == "4":
            print("Goodbye 👋")
            break

        action = actions.get(user_choice)
        if action is None:
            print("Invalid choice ❌")
            continue

        action(tasks)


if __name__ == "__main__":
    main()