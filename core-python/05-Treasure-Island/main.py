# Treasure Island Game 🏝️
# Your mission is to find the treasure using the correct choices.

print("""
🏝️ ==================================
         TREASURE ISLAND
================================== 🏝️

💰 Your mission is to find the treasure.
""")

# Step 1: Choose direction
choice1 = input(
    "🛤️ You're at a crossroad.\n"
    "👉 Type 'left' or 'right': "
).lower()

if choice1 == "left":

    # Step 2: Swim or wait
    choice2 = input(
        "\n🌊 You've come to a lake.\n"
        "🏝️ There is an island in the middle.\n"
        "👉 Type 'wait' or 'swim': "
    ).lower()

    if choice2 == "wait":

        # Step 3: Choose a door
        choice3 = input(
            "\n🏠 You arrive at the island unharmed.\n"
            "🚪 There are 3 doors: Red, Yellow, Blue.\n"
            "👉 Which color do you choose? "
        ).lower()

        # Check the door color
        if choice3 == "yellow":
            print("\n🎉 Congratulations!")
            print("💰 You found the treasure!")
            print("🏆 YOU WIN!")

        elif choice3 == "red":
            print("\n🔥 It's a room full of fire.")
            print("💀 Game Over.")

        elif choice3 == "blue":
            print("\n🐊 You enter a room of beasts.")
            print("💀 Game Over.")

        else:
            print("\n🚪 That door doesn't exist.")
            print("💀 Game Over.")

    else:
        # If player chooses to swim
        print("\n🌊 You got attacked by a trout.")
        print("💀 Game Over.")

else:
    # If player chooses right instead of left
    print("\n🕳️ You fell into a hole.")
    print("💀 Game Over.")