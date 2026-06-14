
# List to store tasks in memory
tasks = []

while True:

    # Display menu options
    print("\n1) Add task")
    print("2) View tasks")
    print("3) Delete tasks")
    print("4) Exit")

    # Get user input
    user_choice = input("Enter your choice: ")
    
    for i, task in enumerate(tasks, start=1):
        print(i, task)

    # Add a new task
    if user_choice == "1":
        task = input("Enter new task: ")
        tasks.append(task)
        print("Task added!")

    # Show all tasks
    elif user_choice == "2":
        if len(tasks) == 0:
            print("No tasks yet!")
        else:
            print("\nYour Tasks:")
            for task in tasks:
                print("-", task)

    elif user_choice == "3":
        user_input = input("Enter your task that u want to delete: ")
        tasks.pop(index = user_input - 1)

    # Exit program
    elif user_choice == "4":
        break


    # Handle invalid input
    else:
        print("Invalid choice")