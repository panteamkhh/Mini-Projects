

# store tasks
tasks = []

while True:

    print( " 1) Add tasks")
    print (" 2) View tasks")
    print (" 3) Exit")

    user_choice = input(" Enter your choice : ")
    print(user_choice)

    if user_choice == "1" :
        task = input("Enter new task: ")
        tasks.append(task)
        print("Task added!")

    elif user_choice == "2":
        print (" 2) View tasks")
        for t in tasks:
            print("-", t)

    elif user_choice == "3":  
        print (" 3) Exit")
        break
    else :
        print (" Not Valid ")      
    