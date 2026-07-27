"""
Day 5 - Treasure Island (OOP version)

A simple branching text-adventure game. The player makes a series of
choices that lead either to treasure or to a "game over" ending.

Note: No source file was provided for Day 5 in the original upload,
so this version was written from scratch following the classic
"Treasure Island" text-adventure format used in beginner Python courses.
"""


class TreasureIslandGame:
    """A small choice-driven text adventure with branching endings."""

    def __init__(self) -> None:
        self.is_alive = True

    @staticmethod
    def _ask(prompt: str, valid_answers: tuple) -> str:
        answer = input(prompt).lower().strip()
        while answer not in valid_answers:
            print(f"Please choose one of: {', '.join(valid_answers)}")
            answer = input(prompt).lower().strip()
        return answer

    def intro(self) -> None:
        print("Welcome to Treasure Island.")
        print("Your mission is to find the treasure.\n")

    def choose_path(self) -> str:
        return self._ask(
            "You're at a crossroad. Where do you want to go? "
            "Type 'left' or 'right': ",
            ("left", "right"),
        )

    def cross_lake(self) -> str:
        return self._ask(
            "You've come to a lake. There is an island in the middle "
            "of the lake. Type 'wait' to wait for a boat, or 'swim' "
            "to swim across: ",
            ("wait", "swim"),
        )

    def choose_door(self) -> str:
        return self._ask(
            "You see three doors. One red, one yellow, one blue. "
            "Which colour do you choose? ",
            ("red", "yellow", "blue"),
        )

    def play(self) -> None:
        self.intro()

        path = self.choose_path()
        if path == "left":
            print("You fell into a hole. Game Over.")
            return

        crossing = self.cross_lake()
        if crossing == "swim":
            print("The lake is full of crocodiles. Game Over.")
            return

        print("You made it safely to the island.")
        door = self.choose_door()

        if door == "red":
            print("It's a room full of fire. Game Over.")
        elif door == "yellow":
            print("You found the treasure! You Win!")
        else:
            print("You got eaten by beasts. Game Over.")


if __name__ == "__main__":
    game = TreasureIslandGame()
    game.play()
