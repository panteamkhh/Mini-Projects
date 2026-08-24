import random

class GuessNumberGame:

    def __init__(self, min_num=1, max_num=100, max_attempts=None):
        # Set the game settings
        self.min_num = min_num
        self.max_num = max_num
        self.max_attempts = max_attempts

        # Generate the secret number
        self.secret_number = random.randint(min_num, max_num)

        # Count the player's attempts
        self.attempts = 0

    def _get_guess(self):
        # Ask the user for a number
        while True:
            raw = input(
                f"Guess a number between {self.min_num} and {self.max_num}: "
            )

            try:
                # Convert the input to an integer
                return int(raw)

            except ValueError:
                # Handle invalid input
                print("Please enter a valid number.")

    def give_hint(self, guess):
        # Compare the guess with the secret number
        if guess == self.secret_number:
            return "correct"
        
        if guess > self.secret_number:
            return "too high"
        else:
            return "too low"

    def play(self):
        # Start the game
        print("Welcome to Guess the Number!")

        # Keep playing until the player wins or runs out of attempts
        while True:
            guess = self._get_guess()
            self.attempts += 1

            # Calculate remaining attempts
            attempts_left = self.max_attempts - self.attempts

            # Show remaining attempts
            print(f"Attempts left: {attempts_left}")

            # Check the player's guess
            result = self.give_hint(guess)

            # Stop the game if the guess is correct
            if result == "correct":
                print(
                    f"Congratulations! You guessed it in "
                    f"{self.attempts} attempt(s)."
                )
                break

            # Show a hint
            print("Too high!" if result == "too high" else "Too low!")

            # Stop the game if the player reaches the attempt limit
            if self.attempts >= self.max_attempts:
                print(f"Out of attempts! The number was {self.secret_number}.")
                break


# Create a game object and start the game
if __name__ == "__main__":
    game = GuessNumberGame(max_attempts=3)
    game.play()