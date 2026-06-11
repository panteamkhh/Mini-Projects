import random

# Main function that runs the game
def play_game():

    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)

    # Ask the user to enter a guess
    user_guess = int(input("Guess a number between 1 and 100: "))

    # Check the user's guess 
    if user_guess == secret_number:
        print("Congratulations! You guessed correctly.")
    elif user_guess > secret_number:
        print("Too high!")    
    else:
        print("Too low!")

# Start the game
play_game()