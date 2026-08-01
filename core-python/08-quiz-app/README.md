# Day 8 - Quiz App

A multiple-choice quiz that loads questions from `questions.json` and
tracks the player's score across all questions.

## What I learned
- Separating question **data** (JSON file) from question **logic**
  (`Question` class) so new questions can be added without touching code
- Building a small quiz "engine" (`QuizApp`) that can run any question set

## How to run
```bash
python main.py
```

## How to test
```bash
pytest test_main.py
```
