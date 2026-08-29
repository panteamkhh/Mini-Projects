import random

# Display game rules
def show_rules():
    print("Rock beats Scissors")
    print("Scissors beats Paper")
    print("Paper beats Rock")
    print()


# Determine the winner of a round
def get_winner(user_choice, pc_choice):

    # Check for a draw
    if user_choice == pc_choice:
        return "draw"

    # Check if the user wins
    elif (
        (user_choice == "rock" and pc_choice == "scissors")
        or (user_choice == "paper" and pc_choice == "rock")
        or (user_choice == "scissors" and pc_choice == "paper")
    ):
        return "user"

    # Otherwise, the PC wins
    return "pc"


def get_user_choice(choices):
    user_choice = input("Enter your choice (rock, paper, scissors): ").lower()
    while user_choice not in choices:
        print("Invalid choice!")
        user_choice = input("Enter your choice (rock, paper, scissors): ").lower()
    return user_choice


def play_match(rounds=3):
    choices = ["rock", "paper", "scissors"]
    user_score = 0
    pc_score = 0

    show_rules()

    # Play exactly `rounds` rounds
    for round_number in range(1, rounds + 1):

        # Display current round
        print(f"\nRound {round_number}")

        # Get user input
        user_choice = get_user_choice(choices)

        # Generate PC choice
        pc_choice = random.choice(choices)
        print(f"PC chose: {pc_choice}")

        # Determine round winner
        winner = get_winner(user_choice, pc_choice)

        # Handle draw result
        if winner == "draw":
            print("Draw!")

        # Handle user win
        elif winner == "user":
            print("You win this round!")
            user_score += 1

        # Handle PC win
        else:
            print("PC wins this round!")
            pc_score += 1

        # Display current score
        print(f"Score => You: {user_score} | PC: {pc_score}")

    # Display final result
    print("\nFinal Result")

    if user_score > pc_score:
        print("You Win The Match!")
    elif pc_score > user_score:
        print("PC Wins The Match!")
    else:
        print("The Match Is A Draw!")


if __name__ == "__main__":
    play_match(rounds=3)
