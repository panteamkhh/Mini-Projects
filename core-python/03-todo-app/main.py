# List to store tasks in memory
tasks = []

while True:

    # Display menu options
    print("\n1) Add task")
    print("2) View tasks")
    print("3) Delete task")
    print("4) Exit")
    print("5) Toggle task (done/undone)")

    # Get user input
    user_choice = input("Enter your choice: ")

    # Stage 1: Add Task
    if user_choice == "1":
        task = input("Enter your new task: ")
        tasks.append({"task": task, "done": False})
        print("Task added successfully ✔")

    # Stage 2 + 3: View Tasks
    elif user_choice == "2":
        if len(tasks) == 0:
            print("No tasks yet ❗")
        else:
            for i, task in enumerate(tasks, start=1):
                if task["done"]:
                    status = "✔"
                else:
                    status = "❌"
                print(f"{i}. {status} {task['task']}")

    # Stage 2: Delete Task
    elif user_choice == "3":
        if len(tasks) == 0:
            print("No tasks to delete !")
        else:
            for i, task in enumerate(tasks, start=1):
                if task["done"]:
                    status = "✔"
                else:
                    status = "❌"
                print(f"{i}. {status} {task['task']}")

            try:
                user_input = int(input("Enter task number to delete: "))

                if 1 <= user_input <= len(tasks):
                    removed = tasks.pop(user_input - 1)
                    print(f"Deleted: {removed['task']} ✔")
                else:
                    print("Invalid task number ")

            except:
                print("Please enter a valid number ")

    # Stage 4: Toggle Done/Undone
    elif user_choice == "5":
        if len(tasks) == 0:
            print("No tasks to update ")
        else:
            for i, task in enumerate(tasks, start=1):
                if task["done"]:
                    status = "✔"
                else:
                    status = "❌"
                print(f"{i}. {status} {task['task']}")

            try:
                user_input = int(input("Enter task number to toggle: "))

                if 1 <= user_input <= len(tasks):
                    task = tasks[user_input - 1]
                    task["done"] = not task["done"]
                    print("Task updated ✔")
                else:
                    print("Invalid task number ")

            except:
                print("Please enter a valid number ")

    # Exit
    elif user_choice == "4":
        print("Goodbye ")
        break

    # Invalid input
    else:
        print("Invalid choice ")