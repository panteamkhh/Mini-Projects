# Day 1 - Guess the Number Game

A command-line number guessing game. The program picks a random number
and the player tries to guess it, receiving "too high" / "too low" hints
after each guess.

## What I learned
- Basic control flow (`while`, `if/elif/else`)
- Handling invalid input with `try/except`
- Structuring simple game logic inside a class (`GuessNumberGame`)

## How to run
```bash
python main.py
```

## How to test
```bash
pytest test_main.py
```

## Example
```
Guess a number between 1 and 100: 50
Too high!
Guess a number between 1 and 100: 25
Too low!
Guess a number between 1 and 100: 37
Congratulations! You guessed it in 3 attempt(s).
```
