# Day 7 - Hangman Game

Classic Hangman with ASCII-art stages, a hidden word, and a limited
number of wrong guesses.

## What I learned
- Modeling game state (guessed letters, wrong guesses, win/lose) as
  properties on a class instead of loose global variables
- Using `set` for guessed letters to avoid duplicate-guess bugs
- Writing tests for game logic independent of `input()`/`print()`

## How to run
```bash
python main.py
```

## How to test
```bash
pytest test_main.py
```
