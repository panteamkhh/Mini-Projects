"""
Day 8 - Quiz App (OOP version)

A multiple-choice quiz that loads questions from a JSON file and
reports the final score.
"""

import json
import os


class Question:
    """A single multiple-choice question."""

    def __init__(self, text: str, options: list[str], answer: int) -> None:
        self.text = text
        self.options = options
        self.answer = answer  # index of the correct option

    def is_correct(self, choice_index: int) -> bool:
        return choice_index == self.answer

    def display(self) -> None:
        print(self.text)
        for i, option in enumerate(self.options, start=1):
            print(f"  {i}. {option}")


class QuizApp:
    """Loads questions and runs an interactive quiz session."""

    def __init__(self, questions_file: str = "questions.json") -> None:
        self.questions_file = questions_file
        self.questions: list[Question] = self._load_questions()
        self.score = 0

    def _load_questions(self) -> list[Question]:
        if not os.path.exists(self.questions_file):
            return []
        with open(self.questions_file, "r") as file:
            data = json.load(file)
        return [Question(q["text"], q["options"], q["answer"]) for q in data]

    def _get_choice(self, num_options: int) -> int:
        while True:
            try:
                choice = int(input("Your answer (number): ")) - 1
                if 0 <= choice < num_options:
                    return choice
            except ValueError:
                pass
            print("Please enter a valid option number.")

    def run(self) -> None:
        if not self.questions:
            print("No questions found.")
            return

        print(f"Quiz started! {len(self.questions)} questions.\n")

        for i, question in enumerate(self.questions, start=1):
            print(f"\nQuestion {i}:")
            question.display()
            choice = self._get_choice(len(question.options))

            if question.is_correct(choice):
                print("Correct! ✔")
                self.score += 1
            else:
                correct_option = question.options[question.answer]
                print(f"Wrong ❌ (correct answer: {correct_option})")

        print(f"\nFinal score: {self.score}/{len(self.questions)}")


if __name__ == "__main__":
    app = QuizApp()
    app.run()
