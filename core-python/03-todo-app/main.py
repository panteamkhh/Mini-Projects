# List to store tasks in memory
tasks = []


while True:

    # Display menu options
    print("\n1) Add task")
    print("2) View tasks")
    print("3) Delete task")
    print("4) Exit")

    # Get user input
    user_choice = input("Enter your choice: ")

    # Add a new task
    if user_choice == "1":
        task = input("Enter your new task : ")
        tasks.append({"task": task,"done": False})
        print("Task added successfully ✔")


    # Show all tasks
    elif user_choice == "2":
        if len(tasks) == 0:
            print("No tasks yet !")
        else:
            for i, task in enumerate(tasks, start=1):
              # Check task status    
                if task["done"] :
                    status = "✔"
                else:
                    status = "❌"
            print(f"{i}. {status} {task['task']}")

    # Delete a task
    elif user_choice == "3":
        if len(tasks) == 0:
            print("No tasks to delete !")
        else:
            for i, task in enumerate(tasks, start=1):
                print(i, task)

            try:
                user_input = int(input("Enter task number to delete: "))

                # Validate index
                if 1 <= user_input <= len(tasks):
                    removed = tasks.pop(user_input - 1)
                    print(f"Deleted: {removed} ")
                else:
                    print("Invalid task number ")

            except:
                print("Please enter a valid number !")

    # Exit program
    elif user_choice == "4":
        print("Goodbye ")
        break

    # Invalid input
    else:
        print("Invalid choice ")