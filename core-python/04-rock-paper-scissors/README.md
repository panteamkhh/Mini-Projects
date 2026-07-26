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

## How to run
```bash
python main.py
```

## How to test
```bash
pytest test_main.py
```
