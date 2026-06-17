import json

# File to store tasks permanently
FILE_NAME = "tasks.json"

# Load tasks from file if exists
try:
    with open(FILE_NAME, "r") as file:
        tasks = json.load(file)
except FileNotFoundError:
    tasks = []


# Save tasks to file
def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file)


while True:

    # Menu
    print("\n1) Add task")
    print("2) View tasks")
    print("3) Delete task")
    print("4) Exit")
    print("5) Toggle task (done/undone)")

    # User input
    user_choice = input("Enter your choice: ")

    # -------------------
    # Add task
    # -------------------
    if user_choice == "1":
        task = input("Enter your new task: ")
        tasks.append({"task": task, "done": False})
        save_tasks()
        print("Task added successfully ✔")

    # -------------------
    # View tasks
    # -------------------
    elif user_choice == "2":
        if len(tasks) == 0:
            print("No tasks yet ❗")
        else:
            for i, task in enumerate(tasks, start=1):
                status = "✔" if task["done"] else "❌"
                print(f"{i}. {status} {task['task']}")

    # -------------------
    # Delete task
    # -------------------
    elif user_choice == "3":
        if len(tasks) == 0:
            print("No tasks to delete ❗")
        else:
            for i, task in enumerate(tasks, start=1):
                status = "✔" if task["done"] else "❌"
                print(f"{i}. {status} {task['task']}")

            try:
                user_input = int(input("Enter task number to delete: "))

                if 1 <= user_input <= len(tasks):
                    removed = tasks.pop(user_input - 1)
                    save_tasks()
                    print(f"Deleted: {removed['task']} ✔")
                else:
                    print("Invalid task number ❌")

            except:
                print("Please enter a valid number ❗")

    # -------------------
    # Toggle task
    # -------------------
    elif user_choice == "5":
        if len(tasks) == 0:
            print("No tasks to update ❗")
        else:
            for i, task in enumerate(tasks, start=1):
                status = "✔" if task["done"] else "❌"
                print(f"{i}. {status} {task['task']}")

            try:
                user_input = int(input("Enter task number to toggle: "))

                if 1 <= user_input <= len(tasks):
                    task = tasks[user_input - 1]
                    task["done"] = not task["done"]
                    save_tasks()
                    print("Task updated ✔")
                else:
                    print("Invalid task number ❌")

            except:
                print("Please enter a valid number ❗")

    # -------------------
    # Exit
    # -------------------
    elif user_choice == "4":
        print("Goodbye 👋")
        break

    # Invalid input
    else:
        print("Invalid choice ❌")