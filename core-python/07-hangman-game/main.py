"""
Day 7 - Hangman Game (OOP version)

Classic Hangman: guess the hidden word one letter at a time before
running out of attempts.
"""

import random


STAGES = [
    """
     -----
     |   |
         |
         |
         |
         |
    """,
    """
     -----
     |   |
     O   |
         |
         |
         |
    """,
    """
     -----
     |   |
     O   |
     |   |
         |
         |
    """,
    """
     -----
     |   |
     O   |
    /|   |
         |
         |
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
         |
         |
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
    /    |
         |
    """,
    """
     -----
     |   |
     O   |
    /|\\  |
    / \\  |
         |
    """,
]

WORD_LIST = ["python", "hangman", "developer", "keyboard", "function", "variable"]


class HangmanGame:
    """Manages state and logic for a single game of Hangman."""

    def __init__(self, word_list: list[str] = None, max_attempts: int = 6) -> None:
        self.word_list = word_list or WORD_LIST
        self.word = random.choice(self.word_list)
        self.max_attempts = max_attempts
        self.wrong_guesses = 0
        self.guessed_letters: set[str] = set()

    @property
    def display_word(self) -> str:
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self.word)

    @property
    def is_won(self) -> bool:
        return all(letter in self.guessed_letters for letter in self.word)

    @property
    def is_lost(self) -> bool:
        return self.wrong_guesses >= self.max_attempts

    def guess(self, letter: str) -> bool:
        """Register a guess. Returns True if the letter is in the word."""
        letter = letter.lower()
        self.guessed_letters.add(letter)

        if letter in self.word:
            return True

        self.wrong_guesses += 1
        return False

    def play(self) -> None:
        print("Welcome to Hangman!")

        while not self.is_won and not self.is_lost:
            print(STAGES[self.wrong_guesses])
            print(self.display_word)

            letter = input("Guess a letter: ").lower()
            if len(letter) != 1 or not letter.isalpha():
                print("Please enter a single letter.")
                continue

            if letter in self.guessed_letters:
                print("You already guessed that letter.")
                continue

            if not self.guess(letter):
                print("Wrong guess!")

        print(STAGES[self.wrong_guesses])
        if self.is_won:
            print(f"You win! The word was '{self.word}'.")
        else:
            print(f"You lose! The word was '{self.word}'.")


if __name__ == "__main__":
    game = HangmanGame()
    game.play()
