# Treasure Island Game 🏝️
# Your mission is to find the treasure using the correct choices.

print("Welcome to Treasure Island.")
print("Your mission is to find the treasure.")

# Step 1: Choose direction
choice1 = input("You're at a crossroad. Where do you want to go? Type 'left' or 'right': ").lower()

if choice1 == "left":
    # Step 2: Swim or wait
    choice2 = input("You've come to a lake. There is an island in the middle of the lake. "
                    "Type 'wait' to wait for a boat or 'swim' to swim across: ").lower()

    if choice2 == "wait":
        # Step 3: Choose a door
        choice3 = input("You arrive at the island unharmed. "
                        "There is a house with 3 doors: one red, one yellow, and one blue. "
                        "Which color do you choose? ").lower()

        # Check the door color
        if choice3 == "yellow":
            print("🎉 You found the treasure! You Win!")
        elif choice3 == "red":
            print("🔥 It's a room full of fire. Game Over.")
        elif choice3 == "blue":
            print("🐊 You enter a room of beasts. Game Over.")
        else:
            print("🚪 That door doesn't exist. Game Over.")

    else:
        # If player chooses to swim
        print("🌊 You got attacked by a trout. Game Over.")

else:
    # If player chooses right instead of left
    print("💀 You fell into a hole. Game Over.")
