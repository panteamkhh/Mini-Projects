import random


class GuessNumberGame:

    def __init__(self, min_num=1, max_num=100, max_attempts=None):
        self.min_num = min_num
        self.max_num = max_num
        self.max_attempts = max_attempts
        self.secret_number = random.randint(min_num, max_num)
        self.attempts = 0

    def _get_guess(self):
        """Prompt the user until a valid integer is entered."""
        while True:
            raw = input(
                f"Guess a number between {self.min_num} and {self.max_num}: "
            )

            try:
                return int(raw)

            except ValueError:
                print("Please enter a valid whole number.")

    def give_hint(self, guess):
        """Return a hint string comparing the guess to the secret number."""
        if guess == self.secret_number:
            return "correct"

        return "too high" if guess > self.secret_number else "too low"

    def play(self):
        """Run the game loop until the player guesses correctly."""
        print("Welcome to Guess the Number!")

        while True:
            guess = self._get_guess()
            self.attempts += 1

            result = self.give_hint(guess)

            if result == "correct":
                print(
                    f"Congratulations! You guessed it in "
                    f"{self.attempts} attempt(s)."
                )
                break

            print("Too high!" if result == "too high" else "Too low!")

            if self.max_attempts and self.attempts >= self.max_attempts:
                print(f"Out of attempts! The number was {self.secret_number}.")
                break


if __name__ == "__main__":
    game = GuessNumberGame(max_attempts=10)
    game.play()