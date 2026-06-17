import random

# Available choices in the game
choices = ["rock", "paper", "scissors"]

# Score tracking
user_score = 0
pc_score = 0

# Main game loop (runs until user exits)
while True:
    # Get user input
    user_choice = input("Enter your choice: rock, paper, scissors ")

    # Exit condition
    if user_choice == "exit":
        break

    # Validate input
    if user_choice not in choices:
        print("Invalid choice")
        continue
   
    # Computer random choice
    pc_choice = random.choice(choices)

    # Draw condition
    if user_choice == pc_choice:
        print("Draw")

    # User win condition
    elif (
        (user_choice == "rock" and pc_choice =="scissors") or
        (user_choice == "paper" and pc_choice =="rock") or
        (user_choice == "scissors" and pc_choice =="paper")
           ):
        print("you win the game")
        user_score += 1

    # User lose condition
    else:
        print("you lose the game")
        pc_score += 1

    # Display score
    print(f"Score => You: {user_score} | Computer: {pc_score}")

    # End of game
    print("Game Over")
    print(f"Final Score => You: {user_score} | Computer: {pc_score}")
