# Day 4 - Rock Paper Scissors

A best-of-3 Rock/Paper/Scissors match against the computer, with rules
displayed up front and a running score.

## What I learned
- Encoding win/lose rules as a lookup dict (`BEATS`) instead of a long
  chain of `if/elif` conditions
- Structuring a multi-round game inside a class with clear responsibilities
  (`play_round`, `get_winner`, `play_match`)

## Features

- Play against the computer
- Three-round match system
- Score tracking
- Input validation
- Final winner announcement

## Concepts Used

- Variables
- Lists
- Loops
- Conditionals
- Functions
- Random Module  

## Project structure
- `main.py` – simple procedural version (functions only, no class)
- `oop_version.py` – object-oriented version (`RockPaperScissorsGame` class)
- `test_main.py` – unit tests for the winner logic (uses `oop_version.py`)

## How to run
```bash
python main.py          # simple version
python oop_version.py   # OOP version
```

## How to test
```bash
pytest test_main.py
```
