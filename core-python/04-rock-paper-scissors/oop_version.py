"""
Day 4 - Rock Paper Scissors (OOP version)

A best-of-three Rock/Paper/Scissors game against the computer.
"""

import random


class RockPaperScissorsGame:
    """Plays a multi-round Rock/Paper/Scissors match against the computer."""

    CHOICES = ("rock", "paper", "scissors")
    BEATS = {"rock": "scissors", "paper": "rock", "scissors": "paper"}

    def __init__(self, rounds: int = 3) -> None:
        self.rounds = rounds
        self.user_score = 0
        self.pc_score = 0

    @staticmethod
    def show_rules() -> None:
        print("Rock beats Scissors")
        print("Scissors beats Paper")
        print("Paper beats Rock\n")

    def get_winner(self, user_choice: str, pc_choice: str) -> str:
        if user_choice == pc_choice:
            return "draw"
        if self.BEATS[user_choice] == pc_choice:
            return "user"
        return "pc"

    def _get_user_choice(self) -> str:
        choice = input("Enter your choice (rock, paper, scissors): ").lower()
        while choice not in self.CHOICES:
            print("Invalid choice!")
            choice = input("Enter your choice (rock, paper, scissors): ").lower()
        return choice

    def play_round(self, round_number: int) -> None:
        print(f"\nRound {round_number}")
        user_choice = self._get_user_choice()
        pc_choice = random.choice(self.CHOICES)
        print(f"PC chose: {pc_choice}")

        winner = self.get_winner(user_choice, pc_choice)
        if winner == "draw":
            print("Draw!")
        elif winner == "user":
            print("You win this round!")
            self.user_score += 1
        else:
            print("PC wins this round!")
            self.pc_score += 1

        print(f"Score => You: {self.user_score} | PC: {self.pc_score}")

    def play_match(self) -> None:
        self.show_rules()
        for round_number in range(1, self.rounds + 1):
            self.play_round(round_number)

        print("\nFinal Result")
        if self.user_score > self.pc_score:
            print("You Win The Match!")
        elif self.pc_score > self.user_score:
            print("PC Wins The Match!")
        else:
            print("The Match Is A Draw!")


if __name__ == "__main__":
    game = RockPaperScissorsGame(rounds=3)
    game.play_match()
